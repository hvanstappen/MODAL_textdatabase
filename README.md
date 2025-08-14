# MODAL_textdatabase
Document Processing and MongoDB storage script

This set of scripts was created as a deliverable for the [project MODAL](https://advn.be/nl/over-advn/projecten/modal-project).

The research project "Metadata and Access to Digital Archives Using Large Language Models," or MODAL for short, launched in the fall of 2024. MODAL's goal is to investigate the potential applications of generative artificial intelligence (GenAI) for the cultural heritage sector and to disseminate this knowledge within the sector.

This a part of a suite of scripts:

* scripts for text extraction and metadata storage (this repository)
* [scripts for enrichments](https://github.com/hvanstappen/MODAL_textdatabase)
* [scripts for browsing and retrieval of documents]()

## Overview
This script processes documents from a specified directory, extracts their text content using Apache Tika, and stores the processed information in MongoDB. It includes logging capabilities and handles various document types while maintaining processing statistics. It's designed to work with MongoDB for document storage and retrieval and relies on the Apache Tika toolset. 

Additional tools:
- create_embeddings.py is a script for generating and storing document embeddings using transformer models.
- add_email_correspondents : adds names of senders and recipients of email messages.
- add_estimated_creation_date : adds a 'best guess' for the file creation date.

## Prerequisites
- Python 3.x
- MongoDB instance running
- Required Python packages:
  - Apache Tika (via `tools.TIKA_extractor`)
  - pymongo (for MongoDB operations)
  - Additional custom modules:
    - `tools.text_functions`
    - `mongo_writer`

## Configuration
The script uses the following main configurations:

## Features
1. **Directory Processing**
   - Recursively walks through all files in the specified directory
   - Filters files based on custom criteria using `file_filter()` and `path_filter()`

2. **Text Extraction**
   - Uses Apache Tika for text extraction
   - Extracts metadata including:
     - MIME type
     - Content
     - Parser information
     - Language
     - Creation date
     - Creator information

3. **Text Processing**
   - Removes multiple newlines from extracted text
   - Calculates word count
   - Performs content validation

4. **Data Storage**
   - Stores processed documents in MongoDB
   - Collection name is automatically generated from the input path
   - Each document includes extracted text and metadata

5. **Logging and Error Handling**
   - Creates log files in a `log_files` directory
   - Logs errors with timestamps and stack traces
   - Handles exceptions at both file and directory levels

## Statistics Tracking
The script maintains three counters:
- `num_tot_files`: Total number of files found
- `num_processed_files`: Number of files that passed the filters
- `num_extract_texts`: Number of files with successfully extracted text

## Output
1. **Console Output**
   - Progress updates for each file
   - Error notifications
   - Final statistics

2. **Log Files**
   - Located in: `log_files/{collection_name}_log.txt`
   - Contains detailed error information
   - Format: `timestamp - level - message`

## Error Handling
- Individual file processing errors are logged without stopping the script
- Critical errors during directory processing are caught and logged
- All errors are written to the log file with full stack traces

## MongoDB Document Structure
Each processed document is stored with the following information:
- MIME type
- Original filename
- Tika parser information
- Cleaned content
- Original file path
- Language
- Word count
- Creation date
- Creator information

## Best Practices
1. Ensure MongoDB is running on localhost:27017
2. Verify write permissions for the log directory
3. Monitor log files for any processing errors
4. Back up important data before processing large directories

## Limitations
- Requires sufficient disk space for log files
- Processing time depends on file sizes and quantity
- Memory usage scales with file size during processing
  
============================================================
# Document Embedding Generator

## Overview
This script generates and stores document embeddings using transformer models. It's designed to work with MongoDB for document storage and retrieval.

## Features
- Multi-lingual document support
- Text preprocessing (stopwords and numbers removal)
- MongoDB integration for document storage
- Progress tracking for long-running processes
- Support for batch document processing

## Prerequisites
### System Requirements
- Python 3.x
- MongoDB Server (running on localhost:27017)
- Sufficient RAM to handle document embeddings


## Usage
1. Ensure your MongoDB collection contains documents with:
   - `extracted_text` field containing the document text
   - `language` field specifying the document language
   - `word_count` field with the number of words

2. Run the embedding generator
e.g. python create_embeddings.py


## Processing Flow
1. Documents are filtered (minimum 10 words required)
2. Text is cleaned by removing:
   - Language-specific stopwords
   - Numerical values
3. Embeddings are generated using SentenceTransformer
4. Results are stored back in MongoDB

## Performance Considerations
- Processing time depends on:
  - Document length
  - Number of documents
  - Available computational resources
- Embeddings increase document storage size significantly


