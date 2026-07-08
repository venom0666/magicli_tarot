import os
import random
from google import genai
from dotenv import load_dotenv
from logic import parse_args, get_options, print_response
from logic import save_to_md, select_model, get_cards, sign_response
from api import interpret_tarot

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")


def main():
    args = parse_args()
    rng = random.Random(args.seed)
    reading_type, language = get_options(args)
    client = genai.Client(api_key=API_KEY)
    model = select_model(args.model, rng)
    cards = get_cards(reading_type["Meaning"], rng)
    response = interpret_tarot(client, cards, reading_type["Name"], model, language)
    client.close()
    response = sign_response(response, model, args)
    print_response(response)
    save_to_md(reading_type["Name"], response, args)


if __name__ == "__main__":
    main()
    