import os
import pymongo
from tools.text_functions import detect_lang
from tools.text_functions import get_word_count
from bson import ObjectId

# MongoDB connection details
MONGO_URI = "mongodb://localhost:27017/"  # Change if needed
DB_NAME = "MODAL_data"  # Change to your actual database name
COLLECTION_NAME = "collection_name"  # Change to your actual collection name

# Folder containing transcriptions
TRANSCRIPT_FOLDER = "/path/to/transcripts/" # set the name of the folder with transcripts
AUDIO_PARSER = "openai/whisper-medium" # set the name of the audio parser used

def update_mongodb():
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    for filename in os.listdir(TRANSCRIPT_FOLDER):
        if filename.endswith(".txt"):
            print(f"\nProcessing: {filename}")
            audio_filename = filename.replace(".txt", ".WAV") # TODO get original audio filename extension
            print(f"Audio file: {audio_filename}")
            transcript_path = os.path.join(TRANSCRIPT_FOLDER, filename)
            print(f"Transcript path: {transcript_path}")

            with open(transcript_path, "r", encoding="utf-8") as f:
                extracted_text = f.read().strip()

            word_count = get_word_count(extracted_text)
            language = detect_lang(extracted_text)

            result = collection.find_one({"file_name": audio_filename})
            if result:
                collection.update_one(
                    {"_id": ObjectId(result["_id"])},
                    {"$set": {
                        "extracted_text": extracted_text,
                        "word_count": word_count,
                        "audio_parser": AUDIO_PARSER,
                        "language": language
                    }}
                )
                print(f"Updated: {audio_filename}")
            else:
                print(f"No matching record found for: {audio_filename}")

    client.close()


if __name__ == "__main__":
    update_mongodb()
