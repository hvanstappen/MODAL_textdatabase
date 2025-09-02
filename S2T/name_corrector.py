import re
import csv
from rapidfuzz import process, fuzz
from pymongo import MongoClient

# === CONFIG ===
CSV_FILENAME = "../tools/data/valid_people_list.csv"
MATCH_THRESHOLD = 80
MAX_WORDS = 5

# Connect to the MongoDB server
client = MongoClient("mongodb://localhost:27017/")  # Update URI as needed
db = client["MODAL_data"]  # Replace with your database name
collection = db["IN"]  # Replace with your collection name

def normalize_for_match(s):
    """Lowercase and remove spaces and punctuation for comparison."""
    return re.sub(r'[\W_]+', '', s).lower()

def load_correct_names(csv_file):
    correct_names = []
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                name = row[0].strip()
                normalized = normalize_for_match(name)
                correct_names.append((name, normalized))
    return correct_names

def generate_name_candidates(text, max_words=MAX_WORDS):
    tokens = list(re.finditer(r'\b\w[\w\.-]*\b', text))
    candidates = []

    for n in range(max_words, 0, -1):
        for i in range(len(tokens) - n + 1):
            span_tokens = tokens[i:i + n]
            start = span_tokens[0].start()
            end = span_tokens[-1].end()
            phrase = text[start:end]
            norm_phrase = normalize_for_match(phrase)
            candidates.append((start, end, phrase, norm_phrase))

    return candidates

def correct_names_in_text(text, correct_names, threshold=MATCH_THRESHOLD):
    candidates = generate_name_candidates(text)
    replacements = []

    for start, end, original_phrase, norm_phrase in candidates:
        match_data = process.extractOne(
            norm_phrase,
            [norm for (_, norm) in correct_names],
            scorer=fuzz.ratio
        )
        if match_data and match_data[1] >= threshold:
            matched_norm = match_data[0]
            match_original = next(name for (name, norm) in correct_names if norm == matched_norm)
            replacements.append((start, end, original_phrase, match_original, match_data[1]))

    # Sort to avoid overlapping replacements (best score & longest match first)
    replacements.sort(key=lambda x: (-x[4], -(x[1] - x[0])))

    used = set()
    final_replacements = []
    replacements_report = []
    seen_pairs = set()  # Track (original, corrected) to avoid duplicates

    for start, end, orig_phrase, replacement, score in replacements:
        if all(pos not in used for pos in range(start, end)):
            final_replacements.append((start, end, replacement))
            used.update(range(start, end))

            # Only add to report if we haven't seen this pair before
            pair_key = (orig_phrase, replacement)
            if pair_key not in seen_pairs:
                seen_pairs.add(pair_key)
                replacements_report.append({
                    "original": orig_phrase,
                    "corrected": replacement,
                    "match_score": score
                })

    # Apply replacements in reverse order
    corrected_text = text
    for start, end, replacement in sorted(final_replacements, reverse=True):
        corrected_text = corrected_text[:start] + replacement + corrected_text[end:]

    return corrected_text, replacements_report

# === MAIN ===
counter = 0
correct_names = load_correct_names(CSV_FILENAME)

for record in collection.find({'original_text': {'$exists': 0}}):
    counter += 1
    print(f'\nProcessing record {counter}')

    extracted_text = record.get("extracted_text")
    if counter == 3:  # testing limit
        break
    if not extracted_text:
        continue

    _id = record.get("_id")

    corrected_extracted_text, replacements = correct_names_in_text(extracted_text, correct_names)

    print(f"Corrected text: {corrected_extracted_text}")
    print(f"Replacements: {replacements}")

    if corrected_extracted_text != extracted_text:
        collection.update_one(
            {"_id": _id},
            {"$set": {
                "extracted_text": corrected_extracted_text,
                "original_text": extracted_text,
                "corrections": replacements  # now without duplicate reports
            }},
            upsert=True
        )
