from langdetect import detect
import re
import nltk
from nltk.corpus import stopwords



def get_word_count(text):
    """
    Counts the number of words in the given text.
    """
    return len(text.split()) if text else 0

def file_filter(filename):
    return not filename.startswith('.') and not filename.endswith(('.exe', '.EXE','.css','.db', '.php', '.dd', '.js', '.json', '.tar', '.zip', '.gz', '.jpg', 'png', '.jpeg', '.tif', '.tiff', '.JPG', '.PNG', '.JPEG', '.TIF', '.TIFF', 'Tiff', '.tar', '.dll', '.DLL', '.cab', '.CAB', '.gz', '.GZ', '.mov', '.MOV', '.mp3', '.MP3', '.avi', '.mp4', '.MP4','.AVI','.cr2', '.CR2', '.psd', '.PSD'))

def file_filter_include(filename):
    return not filename.startswith('.') and filename.endswith(('.jpg', 'png', '.jpeg', '.tif', '.tiff' '.JPG', '.PNG', '.JPEG', '.TIF', '.TIFF'))

def path_filter(path):
    filters = ('brunnhilde', 'siegfried', 'metadata')  # Add as many strings as needed
    return not any(filter_str in path for filter_str in filters)

def detect_lang(text):
    return detect(text) if text else "und"

def remove_multiple_newlines(text):
    """
        Removes >2 consecutive newlines from a text file and replaces them with a single newline.
    """
    try:
        cleaned_text = re.sub(r'[\n|\r]{3,}', '\n\n', text)
    except:
        cleaned_text = None
    return(cleaned_text)

# Check if stopwords are downloaded
try:
    stopwords.words("english")  # Check English stopwords as indicator
except LookupError:
    nltk.download("stopwords")  # Download stopwords only if not available

def remove_stopwords(text, language):
    """
    Removes stopwords from the given text.

    :param text: A string containing words separated by commas (e.g., "[word1, word2, word3]").
    :param language: The language for stopwords, defaults to "dutch".
    :return: A string with stopwords removed.
    """

    lang_map = {
        "en": "english",
        "nl": "dutch",
        "de": "german",
        "fr": "french",
        "es": "spanish",
        "it": "italian",
    }

    # Default to "dutch" if language isn't found in lang_map
    language = lang_map.get(language.lower(), "dutch")

    # Get the stopwords for the specified language
    stopwords_set = set(stopwords.words(language))

    # Split words by any whitespace or commas if brackets not provided
    words = text.replace("[", "").replace("]", "").replace(",", " ").split()
    # print("words",words)

    # Filter out stopwords and return the cleaned string
    cleaned_words = [
        word.strip() for word in words if word.strip().lower() not in stopwords_set
    ]

    return " ".join(cleaned_words)

def remove_numbers(text):
    return re.sub(r" \d+ ", " ", text)
