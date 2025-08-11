# MODAL_textdatabase

Document Processing and MongoDB Storage Script

## Overview
This script processes documents from a specified directory, extracts their text content using Apache Tika, and stores the processed information in MongoDB. It includes logging capabilities and handles various document types while maintaining processing statistics.

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
1. Ensure MongoDB is running before executing the script
2. Verify write permissions for the log directory
3. Monitor log files for any processing errors
4. Back up important data before processing large directories

## Limitations
- Requires sufficient disk space for log files
- Processing time depends on file sizes and quantity
- Memory usage scales with file size during processing