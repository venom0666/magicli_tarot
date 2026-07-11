import os
import sys
import random
from google import genai
from dotenv import load_dotenv
from logic import parse_args, get_options, print_response, get_readings
from logic import select_reader, get_cards, sign_response
from api import interpret_tarot
from file_exports import save_to_file

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")


def main():
    """
    Run the MagicLI Tarot application.

    Parses command-line arguments, initializes the random number
    generator and Gemini client, generates a tarot reading, and
    optionally saves the result.
    """
    if not API_KEY:
        sys.exit("GEMINI_API_KEY environment variable not set.")
    args = parse_args()
    rng = random.Random(args.seed)
    reading_type, language = get_options(args)
    client = genai.Client(api_key=API_KEY)
    reader = select_reader(args, rng)
    cards = get_cards(reading_type["Meaning"], rng)
    response = interpret_tarot(client, cards, reading_type["Name"], reader, language)
    client.close()
    response = sign_response(response, reader, args) 
    save_to_file(reading_type["Name"], response, args, reader)
    print_response(response, args)


if __name__ == "__main__":
    main()
    