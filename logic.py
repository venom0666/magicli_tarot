import sys
import argparse
from tarot import readings, tarot_deck
from constants import logo, tarot_readers, DEFAULT_MODEL_PROBABILITY, REVERSED_PROB, filetypes
from file_exports import ensure_valid_filename


def get_readings():
    """
    Return the available tarot spread names in alphabetical order.

    Returns:
        list[str]: Sorted names of all predefined tarot spreads.
    """
    return list(sorted(readings.keys()))


def print_menu(reading_types):
    """
    Display the interactive menu of available tarot spreads.

    Prints the application logo, the numbered list of predefined spreads,
    the option to create a custom spread, and the option to quit.

    Args:
        reading_types (list[str]): Names of the available tarot spreads.
    """
    print(logo)
    print("Select the Tarot Reading Type:\n")
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
                print("Invalid choice.")
                continue
            if choice < 1 or choice > len(readings)+1:
                print("Invalid choice.")
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
            print("Invalid, Empty Value.")
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
                print("Invalid Choice.")
                continue
            if number < 1:
                print("Invalid Choice.")
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
        description="MagicLI Tarot combines traditional tarot spreads with Google's Gemini API to generate detailed AI-assisted interpretations directly from the command line.",
        epilog="""
    Examples:
    magicli_tarot.py
    magicli_tarot.py -t Celtic
    magicli_tarot.py -t Love -l Spanish
    magicli_tarot.py --seed 42 --save --sign
    magicli_tarot.py --save --print --nosign --reader Madame 
            """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-t", "--type",
        choices=sorted(readings.keys()),
        help="Select a predefined tarot spread."
    )

    parser.add_argument(
        "-l", "--lang",
        default=None,
        help="Generate the reading in the specified language (default: English)."
    )

    parser.add_argument(
            "--reader",
            choices=sorted(tarot_readers.keys()),
            help="Specify the Tarot Reader to use instead of selecting one automatically."
        )

    parser.add_argument(
                "--ext",
                choices=sorted(filetypes),
                default="Pdf",
                help="Specify the File type, default is pdf if --save is used."
            )

    parser.add_argument(
        "--seed",
        type=int,
        help="Initialize the random number generator for reproducible readings."
    )

    parser.add_argument(
        "--print",
        action="store_true",
        help="Print the generated reading."
    )
    
    parser.add_argument(
        "--noprint",
        action="store_true",
        help="Do not print the generated reading."
    )

    parser.add_argument(
        "--sign",
        action="store_true",
        help="Append the reading metadata information."
    )

    parser.add_argument(
        "--nosign",
        action="store_true",
        help="Do not append reading metadata information."
    )

    parser.add_argument(
        "--save",
        action="store_true",
        help="Save the reading to a file."
    )

    parser.add_argument(
        "--nosave",
        action="store_true",
        help="Do not save the reading to a file."
    )

    parser.add_argument(
        "--filename",
        type=str,
        help="Custom filename for the saved Markdown file (without extension)."
    )

    args = parser.parse_args()

    if args.filename and not ensure_valid_filename(args.filename):
        sys.exit()

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


def select_reader(args, rng):
    """
    Select a tarot reader using weighted probabilities.

    The primary tarot reader is selected most of the time, while the remaining
    tarot readers are chosen randomly.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.
        rng (random.Random): Random number generator.

    Returns:
        reader(dict): The selected tarot reader dict.
    """
    if args and args.reader:
        reader = tarot_readers[args.reader]
        return reader
    else:
        reader = tarot_readers["Feline"] if rng.random() < DEFAULT_MODEL_PROBABILITY else rng.choice([
            tarot_readers["Professor"],
            tarot_readers["Crystal"],
            tarot_readers["Madame"],
        ])
    return reader




def sign_response(response, reader, args):
    """
    Optionally append generation metadata to the reading.

    If the user chooses to sign the response and signing is enabled,
    the model name and random seed (when provided) are added to the end
    of the reading.

    Args:
        response (str): Generated tarot reading.
        reader(dict): The selected tarot reader dict.
        args (argparse.Namespace): Parsed command-line arguments.

    Returns:
        str: The original or signed response.
    """
    if args.nosign:
        return response

    signature = f"\n\nReader: {str(reader)[1:-1]}"
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


def print_response(response, args):
    """
    Display the generated tarot reading.

    Prints the reading automatically or suppresses output based on the
    command-line arguments. If neither option is specified, prompts the
    user to decide whether to display the reading.

    Args:
        response (str): The generated tarot reading.
        args (argparse.Namespace): Parsed command-line arguments.
    """
    if args.noprint:
        return

    if args.print or prompt_yes_no("Print response? Y/N: ") == "Y":
        print(f"\n{logo}\n{response}")
