from tika import parser, language, detector


def TIKA_text_extract(file_path):
    """
    Extracts text from a file using Apache Tika.

    Args:
        file_path (str): The path to the file to extract text from.

    Returns:
        str: Extracted text content, or an error message if extraction fails.
    """
    try:
        # Parse the file
        parsed = parser.from_file(file_path, serverEndpoint='http://localhost:9998/', requestOptions={'timeout': 300})

        # Extract text content
        text = parsed.get('content', '')
        metadata = parsed.get('metadata', {})
        # print(metadata)

        text_language = language.from_buffer(text)
        # print("language: ",text_language)

        file_mimetype = detector.from_file(file_path)

        # word_count = metadata.get('meta:word-count', 0)
        creation_date = metadata.get('dcterms:created', '')
        print(creation_date)
        creator = metadata.get('dc:creator', '')

        tika_parser = metadata.get('X-TIKA:Parsed-By-Full-Set', 'Unknown')

        # if not text.strip():
        # if not text:
        #     return "none"

        return file_mimetype, text, tika_parser, text_language, creation_date, creator
    except Exception as e:
        print(f"An error occurred: {e}")
        return "None"

def tika_extract_correspondents(file_path):
    def ensure_list(value):
        if isinstance(value, list):
            return value
        elif isinstance(value, str):
            return value.split(";") if value else []
        return []

    """
    Extracts text from a file using Apache Tika.

    Args:
        file_path (str): The path to the file to extract text from.

    Returns:
        str: Extracted text content, or an error message if extraction fails.
    """
    try:
        # Parse the file
        parsed = parser.from_file(file_path, serverEndpoint='http://localhost:9998/', requestOptions={'timeout': 300})

        # Extract email metadata
        metadata = parsed.get('metadata', {})
        # print(metadata)
        # print("=============================")

        sender_email_string = metadata.get('Message:From-Email', '')
        sender_email = ensure_list(sender_email_string)
        # print(f"sender_email: {sender_email}")
        sender_name_string = metadata.get('Message:From-Name', '')
        sender_name = ensure_list(sender_name_string)
        # print(f"sender_name: {sender_name}")
        recipient_email_string = metadata.get('Message:To-Email', '')
        recipient_email = ensure_list(recipient_email_string)
        # print(f"recipient_email: {recipient_email}")
        recipient_name_string = metadata.get('Message-To', '')
        recipient_name = ensure_list(recipient_name_string)
        # print(f"recipient_name: {recipient_name}")
        cc_name_string = metadata.get('Message-Cc', '')
        cc_name = ensure_list(cc_name_string)
        # print(f"cc_name: {cc_name}")

        return sender_email, sender_name, recipient_email, recipient_name, cc_name
    except Exception as e:
        print(f"An error occurred: {e}")
        return "None"


# Example usage:
# file_path = "/media/henk/LaCie/2025_MODAL/LH/HH_71_Kristien_Hemmerechts/_Fwd_Fwd_Open_brief_aan_de_bestuursverantwoordelijke_van_Antwerpen_en_de_media_.msg"
# file_path = "/media/henk/LaCie/2025_MODAL/ADVN/UNPO_nextcloud/05_archive_longterm/03_members/MEMBERS + REGIONS/Ethiopia (general)/ETHIOPIA CONFERENCE II - April 2015/Dossier - Ethiopia - Post meetings conference/Ana Gomes - Full Resolution Email.eml"
# #
# print(TIKA_text_extract_from_msg(file_path))
