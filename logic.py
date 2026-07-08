import sys
import argparse
import datetime
from tarot import readings, tarot_deck
from api import models


def get_readings():
    return list(sorted(readings.keys()))


def print_menu(reading_types):
    print("\nSelect the Tarot Reading Type:")
    for i, reading in enumerate(reading_types, start=1):
        print(f"{i:2} - {readings[reading]['Name']}")
    print(f"{len(readings) + 1} - Custom")
    print(" Q - Quit\n")


def get_type():
    print_menu(get_readings())
    while True:
        choice = input("Choice: ").upper()
        if choice == "Q":
            sys.exit()
        else:
            try:
                choice = int(choice)
            except ValueError:
                print("Invalid choice")
                continue
            if choice < 1 or choice > len(readings)+1:
                print("Invalid choice")
                continue
            return choice-1


def create_custom():
    definitions = []
    name = input("New Spread Name: ").strip().title()
    while True:
        try:
            num_cards = int(input("Number of Cards: "))
        except (TypeError, ValueError):
            print("Invalid Choice")
            continue
        if num_cards < 1:
            print("Invalid Choice")
            continue
        else:
            break

    for card_number in range(num_cards):
        definitions.append(input(f"Meaning for Card {card_number+1}: ").strip().title())
    return {"Name": name, "Meaning": definitions}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Magicli-tarot brings the Power of Python and AI, to create insightful tarot readings delivering them to the comfort of your own CLI."
    )

    parser.add_argument(
        "-t", "--type",
        choices=sorted(readings.keys()),
        help="Tarot spread type"
    )

    parser.add_argument(
        "-l", "--lang",
        default=None,
        help="Output language (default: English)"
    )

    parser.add_argument(
        "--model",
        choices=models,
        help="Model to interpret readings"
    )

    parser.add_argument(
        "--seed",
        type=int,
        help="Random seed"
    )

    parser.add_argument(
        "--sign",
        action="store_true",
        help="Automatically add signature from response"
    )

    parser.add_argument(
        "--nosign",
        action="store_true",
        help="Automatically remove signature from response"
    )

    parser.add_argument(
        "--save",
        action="store_true",
        help="Automatically save to .md file"
    )

    parser.add_argument(
        "--nosave",
        action="store_true",
        help="Automatically don't save to .md file"
    )

    args = parser.parse_args()

    return args


def get_options(args):
    # Interactive mode
    if args.type is None:
        tarot_type = get_type()

        if tarot_type == len(readings):
            reading_type = create_custom()
        else:
            reading_type = readings[get_readings()[tarot_type]]
        language = input(
            "Output Language (leave empty for English): "
        ).strip() or "English"

        return reading_type, language

    # Command-line mode
    return readings[args.type], args.lang or "English"


def get_cards(spread, rng):
    REVERSED_PROB = 0.20
    drawn_cards = rng.sample(tarot_deck, len(spread))
    cards = []
    for position, card in zip(spread, drawn_cards):
        cards.append({
            "position": position,
            "card": card,
            "orientation":
            "Reversed" if rng.random() < REVERSED_PROB else "Upright"
        })
    return cards


def select_model(arg, rng):
    MAIN_PROB = 0.65
    if arg:
        model = arg
        return model
    else:
        model = "gemini-3.1-flash-lite" if rng.random() < MAIN_PROB else rng.choice([
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite",
            "gemini-3.5-flash",
        ])
    return model


def save_to_md(reading, content, args):
    now = datetime.datetime.now().strftime("%B-%d-%Y_%H-%M")
    filename = f"{reading}_{now}.md".replace(" ", "_")
    if args.save:
        write_file(filename, content)
    elif not args.nosave:
        choice = validate_y_or_n("\nSave to .md File? Y/N: ")
        if choice == "Y":
            write_file(filename, content)



def write_file(filename, content):
    try:
        with open(f"output/{filename}", "w", encoding="utf-8") as file:
            file.write(content)
    except Exception as e:
        sys.exit(f"File Write error: {e}")


def sign_response(response, model, args):
    choice = validate_y_or_n("\nSign? Y/N:")
    if args.nosign or choice == "N":
        return response
    else:
        response = response + f"\n\nModel: {model}"
        if args.seed:
            response = response + f"\nSeed: {args.seed}"
        return response


def validate_y_or_n(message):
    while True:
        choice = input(message).upper().strip()
        if choice == "Y" or choice == "N":
            return choice
        else:
            print("Invalid option")
            continue


def print_response(response):
    print(f"\n{response}")
