import os
from datetime import datetime
from pymongo import MongoClient
import re
from tools.TIKA_extractor import tika_extract_correspondents

# SET DB COLLECTION:
database_name = "MODAL_data" # Replace with database name
collection_name = "collection_name" # Replace with collection name

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client[database_name]
collection = db[collection_name]

# Use filters to find records with file_path containing ".eml" or ".msg"
query_filter = {
    "$or": [
        {"file_path": {"$regex": re.compile(r".*eml")}},
        {"file_path": {"$regex": re.compile(r".*msg")}},
        {"file_path": {"$regex": re.compile(r".*mbox")}}
    ]
}

counter = 0
for record in collection.find(query_filter):
    counter += 1
    print(f'\nProcessing record {counter}')
    file_path = record.get("file_path")
    _id = record.get("_id")
    creation_date = record.get("creation_date")

    try:
        sender_email, sender_name, recipient_email, recipient_name, cc_name = tika_extract_correspondents(file_path)
        update_fields = {
            "sender_email": sender_email,
            "sender_name": sender_name,
            "recipient_email": recipient_email,
            "recipient_name": recipient_name,
            "cc_name": cc_name
        }

        # Update the database record with the extracted email correspondents
        collection.update_one({"_id": _id}, {"$set": update_fields})
        print(f"Updated record {_id} with email correspondents")

    except Exception as e:
        print(f"Error processing email {file_path}: {e}")