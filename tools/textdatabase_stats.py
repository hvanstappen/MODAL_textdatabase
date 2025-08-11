import csv
from pymongo import MongoClient
from collections import defaultdict

def summarize_mime_types():
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")  # Update with your connection details if needed
    db = client["MODAL_sourcedata"]
    collection_name = "ADVN_VEA260_VUJO"
    collection = db[collection_name]

    # Initialize summary dictionary
    summary = defaultdict(lambda: {
        "total_files": 0,
        "total_words": 0,
        "files_with_zero_words": 0,
        "languages": set()
    })

    # Process each record in the collection
    for record in collection.find():
        mime_type = record.get("file_mimetype", "unknown")
        word_count = record.get("word_count", 0)
        language = record.get("language", None)

        # Update summary for this MIME type
        summary[mime_type]["total_files"] += 1
        summary[mime_type]["total_words"] += word_count
        if word_count == 0:
            summary[mime_type]["files_with_zero_words"] += 1
        if language:
            summary[mime_type]["languages"].add(language)

    print(f'total files: {summary[mime_type]["total_files"]}')
    print(f'total_words: {summary[mime_type]["total_words"]}')

    # Prepare CSV output  /home/henk/DATABLE/1_Projecten/2024_MODAL/3_Data/TIKA_statistics
    csv_filename = f"/home/henk/DATABLE/1_Projecten/2024_MODAL/3_Data/TIKA_statistics/{collection_name}_summary.csv"
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        # Write header
        csv_writer.writerow(["MIME Type", "Total Files", "Total Words", "Files with Zero Words", "Number of Languages", "List of Languages"])

        # Write data for each MIME type
        total_files = 0
        total_words = 0
        total_zero_word_files = 0
        total_languages = set()

        for mime_type, stats in summary.items():
            num_languages = len(stats["languages"])
            language_list = ", ".join(sorted(stats["languages"]))
            csv_writer.writerow([
                mime_type,
                stats["total_files"],
                stats["total_words"],
                stats["files_with_zero_words"],
                num_languages,
                language_list
            ])
            total_files += stats["total_files"]
            total_words += stats["total_words"]
            total_zero_word_files += stats["files_with_zero_words"]
            total_languages.update(stats["languages"])

        # Write totals row
        csv_writer.writerow([
            "Total",
            total_files,
            total_words,
            total_zero_word_files,
            len(total_languages),
            ", ".join(sorted(total_languages))
        ])

    print(f"Summary written to {csv_filename}")

if __name__ == "__main__":
    summarize_mime_types()
