import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from pymongo import MongoClient
from tools.text_functions import get_word_count, detect_lang
import logging

# A separate script to process audio files after processing with TIKA and upload to MongoDB
# Note: this is kept as a separate process due to the long processing time - only apply when required

db_name = "MODAL_data"
collection_name = "collection_name"

lang = "nl" # Change to the audio language

def transcribe_audio(audio_file_path, pipe):
    result = pipe(audio_file_path)
    detected_text = result["text"]
    return detected_text, pipe.model.name_or_path

def fetch_audio_records():
    """
    Fetches all records from a MongoDB collection where the 'file_mimetype' starts with 'audio'.
    Returns:
        list: A list of matching records.
    """
    # Connect to the MongoDB client
    client = MongoClient("mongodb://localhost:27017/")

    # Specify the database and collection
    db = client[db_name]
    collection = db[collection_name]

    # Query to find records where 'file_mimetype' starts with 'audio'
    query = {"file_mimetype": {"$regex": "^audio"}} # Change this based on your needs

    # Fetch all matching records
    records = list(collection.find(query))

    # Close the MongoDB connection
    client.close()

    return records

def update_record_with_transcription(record_id, audio_text):
    """
    Updates a MongoDB record with the transcribed audio text.

    Parameters:
        record_id: The ID of the record to update.
        audio_text (str): The transcribed text to add.
    """
    # Connect to the MongoDB client
    client = MongoClient("mongodb://localhost:27017/")

    # Specify the database and collection
    db = client[db_name]
    collection = db[collection_name]

    # Update the record with the transcribed text
    # collection.update_one({"_id": record_id}, {"$set": {"extracted_text": audio_text}})
    collection.update_one(
        {"_id": record_id},
        {"$set": {"extracted_text": audio_text, "language": language, "word_count": word_count, "audio_parser": model_id}}
    )

    # Close the MongoDB connection
    client.close()

audio_records = fetch_audio_records()

# load model
model_id = "openai/whisper-medium"
#model_id = "openai/whisper-large-v3"

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch.float32, low_cpu_mem_usage=True, use_safetensors=True
)
model.to("cpu")

device = "cpu"
torch_dtype = torch.float32

processor = AutoProcessor.from_pretrained(model_id)
pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    chunk_length_s=12,  # Adjust this based on your needs
    stride_length_s=4,
    batch_size=4,
    torch_dtype=torch_dtype,
    device=device,
    return_timestamps=True
)

logging.basicConfig(level=logging.INFO)

for record in audio_records:
    try:
        audio_file_path = record['file_path']
        logging.info(f"Processing {audio_file_path}")
        transcription = transcribe_audio(audio_file_path, pipe)
        print(transcription)
        if transcription[0]:
            audio_text, model_id = transcription
            print(audio_text)
            language = detect_lang(audio_text)
            word_count = get_word_count(audio_text)
            update_record_with_transcription(record["_id"], audio_text)
            logging.info(f"Updated record {record['_id']} successfully.")
        else:
            logging.warning(f"Skipping {audio_file_path} due to transcription failure.")
    except Exception as e:
        logging.error(f"Error processing record {record['_id']}: {e}")
