import os
import re
import logging
from tools.TIKA_extractor import TIKA_text_extract
from mongo_writer import write_to_mongodb
from tools.text_functions import remove_multiple_newlines, get_word_count, file_filter, path_filter

# Set path to the folder that contains the files
path = "/media/henk/LaCie/2025_MODAL/test_email_attach"

# Set database name
db_name = "MODAL_testdata"

# Generate collection name safely
collection_name = re.split(r"[/]+", path)[-1].replace(' ','_')

# Generate logging file path
log_dir = "log_files"
os.makedirs(log_dir, exist_ok=True)  # Ensure directory exists
logging_file = os.path.join(log_dir, f"{collection_name}_log.txt")

# Set up logging
logging.basicConfig(
    filename=logging_file,
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize counters
num_tot_files = 0
num_processed_files = 0
num_extract_texts = 0

try:
    for root, _, files in os.walk(path):
        for file in files:
            try:
                file_path = os.path.join(root, file)
                num_tot_files += 1
                print(f"Processing file {num_tot_files}: {file_path}")

                if file_filter(file) and path_filter(root):
                    num_processed_files += 1
                    tika = TIKA_text_extract(file_path)

                    if not tika or len(tika) < 6:
                        raise ValueError("Unexpected TIKA output structure")

                    mime_type, content, tika_parser, lang, creation_date, creator = (
                        tika[0], tika[1], tika[2][1:], tika[3], tika[4], tika[5]
                    )

                    if content and len(content) > 0:
                        num_extract_texts += 1

                    clean_content = remove_multiple_newlines(content)
                    word_count = get_word_count(content)

                    record_id = write_to_mongodb(
                        mime_type, file, tika_parser, clean_content, file_path, lang,
                        word_count, creation_date, creator, db_name, collection_name
                    )
                    print(f"{file} written to {record_id} in {db_name}")
                else:
                    print(f"{file} is ignored.")
            except Exception as e:
                logging.exception(f"Error processing file {file}: {e}")
                print(f"Error processing file {file}. Check log for details.")
except Exception as e:
    logging.exception(f"An error occurred while processing the folder: {e}")
    print("Critical error. Check log for details.")

print('Total files:', num_tot_files)
print('Processed files:', num_processed_files)
print('Extracted texts:', num_extract_texts)
