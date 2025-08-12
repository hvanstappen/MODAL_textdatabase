# This Python script is meant to add or update estimated creation dates in a MongoDB collection, based on file metadata and existing record fields.
# The script connects to a MongoDB collection, looks at each record, and tries to get the file creation date from the file system  (using the file_path stored in MongoDB).
# If the record already has a creation_date, it uses that. # If not, it uses the file’s actual creation date.
# Then the script determines the best guess for the creation date, and writes it back to MongoDB.
# - "file_creation_date" → the actual file system creation date.
# - "estimated_creation_date" → the best guess (either creation_date or file_creation_date).

import os
from datetime import datetime
from pymongo import MongoClient

# SET DB COLLECTION:
database_name = "MODAL_data" # Replace with database name
collection_name = "collection_name" # Replace with collection name

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client[database_name]
collection = db[collection_name]


def get_file_creation_date(file_path):
    """
    Get the creation date of a file in ISO 8601 format.

    Args:
        file_path (str): Path to the file

    Returns:
        str: File creation date in ISO 8601 format (YYYY-MM-DDThh:mm:ssZ) if successful
        None: If file not found or error occurs
    """
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

# loop through records
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
