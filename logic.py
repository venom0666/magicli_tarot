import sys
import argparse
import datetime
import os
from tarot import readings, tarot_deck
from constants import models

REVERSED_PROB = 0.20
DEFAULT_MODEL_PROBABILITY = 0.65
FOLDER_PATH = "./output/"


def get_readings():
    """Return a sorted list of available tarot spread names."""
    return list(sorted(readings.keys()))


def print_menu(reading_types):
    """Display the menu of available tarot spreads."""
    print("\nSelect the Tarot Reading Type:\n")
    for i, reading in enumerate(reading_types, start=1):
        print(f"{i:2} - {readings[reading]['Name']}")
    print(f"{len(readings) + 1} - Custom")
    print(" Q - Quit\n")


def get_type():
    """
    Prompt the user to select a tarot spread.

    Returns:
        int: The index of the selected spread, or the custom spread option.
    """
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


def prompt_text(message):
    """
    Prompt the user for non-empty text input.

    Continues prompting until a non-empty value is entered. The returned
    text is stripped of leading and trailing whitespace and converted to
    title case.

    Args:
        message (str): Prompt displayed to the user.

    Returns:
        str: The validated text entered by the user.
    """
    while True:
        text = input(message).strip().title()
        if text == "":
            print("Invalid Empty Value")
            continue
        else:
            return text

def prompt_positive_int(message):
    """
    Prompt the user for a positive integer.

    Continues prompting until the user enters an integer greater than
    zero.

    Args:
        message (str): Prompt displayed to the user.

    Returns:
        int: The validated positive integer.
    """
    while True:
            try:
                number = int(input(message))
            except (TypeError, ValueError):
                print("Invalid Choice")
                continue
            if number < 1:
                print("Invalid Choice")
                continue
            else:
                return number

def create_custom():
    """
    Create a custom tarot spread from user input.

    Returns:
        dict: A dictionary containing the spread name and card positions.
    """
    definitions = []
    name = prompt_text("New Spread Name: ")
    num_cards = prompt_positive_int("Number of Cards: ")

    for card_number in range(num_cards):
        definitions.append(prompt_text(f"Meaning for Card {card_number+1}: ").strip().title())
    return {"Name": name, "Meaning": definitions}


def parse_args():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="magicli_tarot brings the Power of Python and AI, to create insightful tarot readings delivering them to the comfort of your own CLI."
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
    """
    Determine the reading type and language.

    Uses command-line arguments when provided; otherwise, prompts the
    user interactively.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.

    Returns:
        tuple: A tuple containing the selected reading definition and
        output language.
    """
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
    """
    Draw random tarot cards for a spread.

    Each card is assigned its position in the spread and randomly marked
    as upright or reversed.

    Args:
        spread (list[str]): Card positions for the selected spread.
        rng (random.Random): Random number generator.

    Returns:
        list[dict]: Information about each drawn card.
    """
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
    """
    Select a Gemini model using weighted probabilities.

    The primary model is selected most of the time, while the remaining
    models are chosen randomly.

    Args:
        rng (random.Random): Random number generator.

    Returns:
        str: The selected Gemini model name.
    """
    if arg:
        model = arg
        return model
    else:
        model = "gemini-3.1-flash-lite" if rng.random() < DEFAULT_MODEL_PROBABILITY else rng.choice([
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite",
            "gemini-3.5-flash",
        ])
    return model


def save_to_md(reading, content, args):
    """
    Save a tarot reading as a Markdown file.

    Prompts the user before writing the file.

    Args:
        reading (str): Name of the tarot spread.
        content (str): Reading to save.
    """
    now = datetime.datetime.now().strftime("%B-%d-%Y_%H-%M")
    filename = (f"{reading}_{now}.md"
                .replace(" ", "_")
                .replace(",","")
                .replace("'", "")
                )
    if args.save:
        write_file(filename, content)
    elif not args.nosave:
        choice = prompt_yes_no("\nSave to .md File? Y/N: ")
        if choice == "Y":
            write_file(filename, content)

def ensure_output_directory():
    """
    Ensure that the output directory exists.

    Creates the output directory if it does not already exist.
    """
    if not os.path.isdir(FOLDER_PATH):
        os.mkdir(FOLDER_PATH)

def write_file(filename, content):
    """
    Write text content to a Markdown file in the output directory.
    If output directory does not exist it will be created.

    Args:
        filename (str): Name of the file to create.
        content (str): Text to write to the file.

    Raises:
        SystemExit: If the file cannot be written.
    """
    ensure_output_directory()
    try:
        with open(f"output/{filename}", "w", encoding="utf-8") as file:
            file.write(content)
    except Exception as e:
        sys.exit(f"File Write error: {e}")


def sign_response(response, model, args):
    """
    Optionally append generation metadata to the reading.

    If the user chooses to sign the response and signing is enabled,
    the model name and random seed (when provided) are added to the end
    of the reading.

    Args:
        response (str): Generated tarot reading.
        model (str): Gemini model used to generate the reading.
        args (argparse.Namespace): Parsed command-line arguments.

    Returns:
        str: The original or signed response.
    """
    if args.nosign:
        return response

    signature = f"\n\nModel: {model}"
    if args.seed is not None:
        signature += f"\nSeed: {args.seed}"

    if args.sign or prompt_yes_no("\nSign? Y/N:") == "Y":
        return response + signature

    return response


def prompt_yes_no(message):
    """
    Prompt the user for a yes-or-no response.

    Continues prompting until the user enters either 'Y' or 'N'.

    Args:
        message (str): Prompt displayed to the user.

    Returns:
        str: The validated response ('Y' or 'N').
    """
    while True:
        choice = input(message).upper().strip()
        if choice == "Y" or choice == "N":
            return choice
        else:
            print("Invalid option")
            continue


def print_response(response):
    """
    Display the generated tarot reading.

    Args:
        response (str): The reading to print.
    """
    print(f"\n{response}")
