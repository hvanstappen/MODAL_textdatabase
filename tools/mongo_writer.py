from pymongo import MongoClient
from tika import parser


def write_to_mongodb(file_mimetype, file, tika_parser, extracted_text, path, lang, word_count, creation_date, creator, db_name, collection_name, mongo_uri="mongodb://localhost:27017/"):
    """
    Extracts text from a file and writes it to a MongoDB collection.

    Args:
        file_path (str): The path to the file to extract text from.
        db_name (str): The name of the MongoDB database.
        collection_name (str): The name of the MongoDB collection.
        mongo_uri (str): The MongoDB connection URI. Defaults to localhost.
    """

    # Initialize MongoDB client
    client = MongoClient(mongo_uri)

    # Access the database and collection
    db = client[db_name]
    collection = db[collection_name]

    # Create a document to insert
    document = {
        "file_name": file,
        "file_path": path,
        "tika_parser": tika_parser,
        "file_mimetype": file_mimetype,
        "extracted_text": extracted_text,
        "creator": creator,
        "creation_date": creation_date,
        "language": lang,
        "word_count": word_count
    }

    # Insert the document into the collection
    result = collection.insert_one(document)
    # Return the MongoDB record ID
    return result.inserted_id

# Example usage:
# if __name__ == "__main__":
#     file_path = "example.pdf"  # Replace with the actual file path
#     db_name = "my_database"
#     collection_name = "extracted_texts"
#
#     # Call the function to write the extracted text to MongoDB
#     write_to_mongodb(extracted_text, file_path, db_name, collection_name)
