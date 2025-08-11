import os
from datetime import datetime
from pymongo import MongoClient

# Connect to the MongoDB server
client = MongoClient("mongodb://localhost:27017/")  # Update URI as needed
db = client["MODAL_testdata"]  # Replace with  database name
collection = db["LH_UitgeverijVrijdag"]  # Replace with  collection name

def get_file_creation_date(file_path):
    print(f'\nProcessing path {file_path}')
    try:
        # Get file creation time in seconds since the epoch
        file_creation_time = os.path.getctime(file_path)
        return datetime.utcfromtimestamp(file_creation_time).strftime("%Y-%m-%dT%H:%M:%SZ")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error retrieving file creation date for {file_path}: {e}")
    return None

counter = 0
for record in collection.find():
    counter += 1
    print(f'\nProcessing record {counter}')
    file_path = record.get("file_path")
    _id = record.get("_id")
    creation_date = record.get("creation_date")

    #get file creation date
    if file_path:
        file_creation_date = get_file_creation_date(file_path)
    else:
        file_creation_date = None

    # determine est file creation date
    estimated_creation_date = None
    if creation_date:
        estimated_creation_date = creation_date
        print(f'creation_date     : {creation_date}')
        print(f'file_creation_date: {file_creation_date}')
    elif file_creation_date:
        estimated_creation_date = file_creation_date
        print(f'file_creation_date: {file_creation_date}')

    # write to Mongodb
    update_fields = {}
    if file_creation_date:
        update_fields["file_creation_date"] = file_creation_date
    if estimated_creation_date:
        update_fields["estimated_creation_date"] = estimated_creation_date

    if update_fields:
        try:
            collection.update_one({"_id": _id}, {"$set": update_fields})
        except Exception as e:
            print(f"Error updating record with _id %s: %s", {_id}, {e})
