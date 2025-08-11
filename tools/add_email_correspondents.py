import os
from datetime import datetime
from pymongo import MongoClient
import re  # Import the 're' module to use regular expressions
from TIKA_extractor import tika_extract_correspondents

# Connect to the MongoDB server
client = MongoClient("mongodb://localhost:27017/")  # Update URI as needed
db = client["MODAL_testdata"]  # Replace with database name
collection = db["LH_UitgeverijVrijdag"]  # Replace with collection name

# Use filters to find records with file_path containing ".eml" or ".msg"
counter = 0
query_filter = {
    "$or": [
        {"file_path": {"$regex": re.compile(r".*eml")}},
        {"file_path": {"$regex": re.compile(r".*msg")}},
        {"file_path": {"$regex": re.compile(r".*mbox")}}
    ]
}

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
        print(update_fields)

        # Uncomment the next lines to enable updates in the database
        collection.update_one({"_id": _id}, {"$set": update_fields})
        print(f"Updated record {_id} with email correspondents")

    except Exception as e:
        print(f"Error processing email {file_path}: {e}")