from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
from tools.text_functions import remove_stopwords, remove_numbers
from bson import ObjectId

# This script creates embeddings for documents in a MongoDB collection

# Load the multilingual sentence transformer model
model_name = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
model = SentenceTransformer(model_name)

# SET DB COLLECTION:
database_name = "MODAL_data" # Replace with database name
collection_name = "collection_name" # Replace with collection name

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client[database_name]
collection = db[collection_name]

print("Loading documents...")
documents = collection.find({"word_count": {"$gte": 10}}, {"extracted_text": 1, "language": 1}) # find all text documents with word count >= 10

# Extract text and IDs correctly
docs = []
doc_ids = []
print("removing stopwords and numbers...")
for doc in documents:
    if "extracted_text" in doc:
        cleaned_text = remove_stopwords(doc["extracted_text"], doc["language"])  # remove stopwords
        cleaned_text = remove_numbers(cleaned_text) # remove numbers
        docs.append(cleaned_text)
        doc_id = str(doc["_id"])  # Ensure ID is a string
        doc_ids.append(doc_id)

num_docs = len(docs)
num_embeddings = 0
print(f"Number of documents: {num_docs}")

# Generate embeddings for the text and topics
for text, doc_id in zip(docs, doc_ids):
    text_embedding = model.encode(text)

    # Convert NumPy array to list for BSON compatibility
    text_embedding_as_list = text_embedding.tolist()

    # Prepare enrichment object (if it's needed later)
    embedding_data = {
        "embedding_model_used": model_name,
        "text_embeddings": text_embedding_as_list
    }

    # Update MongoDB document
    collection.update_one(
        {"_id": ObjectId(doc_id) if len(doc_id) == 24 else doc_id},  # Ensure ObjectId format if required
        {"$push": {"embeddings": embedding_data}}  # Use the converted list
    )

    num_embeddings += 1
    print(f"{doc_id} docs embedded ({num_embeddings}/{num_docs})")


