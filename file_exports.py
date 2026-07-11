import datetime
import os
import re 
import sys
from constants import FOLDER_PATH, file_logo
from logic import prompt_yes_no


def save_to_file(reading, content, args, reader):
    """
    Save a tarot reading as a Markdown file.

    Prompts the user before writing the file.

    Args:
        reading (str): Name of the tarot spread.
        content (str): Reading to save.
        args (argparse.Namespace): Parsed command-line arguments.
        reader(dict): The selected tarot reader dict.
    """    
    now = datetime.datetime.now().strftime("%B-%d-%Y_%H-%M")
    if args.save:
        filename = set_default_filename(reading, now, reader) if not args.filename else args.filename
        write_file(filename, content)
    elif not args.nosave:
        choice = prompt_yes_no("Save to .md File? Y/N: ")
        if choice == "Y":
            filename = change_filename(reading,args, now, reader)
            write_file(filename, content)

def ensure_output_directory():
    """
    Ensure that the output directory exists.

    Creates the output directory if it does not already exist.
    """
    if not os.path.isdir(FOLDER_PATH):
        os.mkdir(FOLDER_PATH)
        print(f"Folder: {FOLDER_PATH} - Has been created.")

def change_filename(reading, args, now, reader):
    """
    Determine the filename for the saved reading.

    Uses the filename provided through the command-line arguments when
    available. Otherwise, prompts the user to choose between a custom
    filename or the default generated filename.

    Args:
        reading (str): Name of the tarot spread.
        args (argparse.Namespace): Parsed command-line arguments.
        now (str): Timestamp appended to the filename.
        reader(dict): The selected tarot reader dict.

    Returns:
        str: The filename to use when saving the reading.
    """
    if args.filename:
        filename = args.filename
        return f"{filename}_{now}.md"
    while True:
        choice = prompt_yes_no("Change Filename? Y/N): ")
        if choice == "Y":
            filename = prompt_filename("New Filename: ")
            return f"{filename}_{now}.md"
        else:
            return set_default_filename(reading, now, reader)


def set_default_filename(reading, now, reader):
    """
    Generate the default filename for a tarot reading.

    The filename is based on the reading name and the current timestamp,
    with spaces and unsupported characters removed.

    Args:
        reading (str): Name of the tarot spread.
        now (str): Timestamp appended to the filename.
        reader(dict): The selected tarot reader dict.

    Returns:
        str: The generated filename.
    """
    filename = (f"{reader["Name"]}_{reading}_{now}.md"
                    .replace(" ", "_")
                    .replace(",","")
                    .replace("'", "")
                    )
    return filename


def ensure_valid_filename(filename):
    """
    Validate a filename entered by the user.

    A valid filename must be between 5 and 50 characters long and may
    contain only letters, numbers, underscores, and hyphens.

    Args:
        filename (str): Filename to validate.

    Returns:
        bool: True if the filename is valid, otherwise False.
    """
    if re.match(string=filename, pattern=r'^[a-zA-Z0-9_-]{5,50}'):
        return True
    elif len(filename) < 5 or len(filename)>50:
        print("Invalid filename, length must be between 5-50.")
        return False
    else:
        print("Invalid filename special characters, only '_' and '-' are allowed.")
        return False
    

def prompt_filename(message):
    """
    Prompt the user for a valid filename.

    Continues prompting until a filename that satisfies the validation
    rules is entered.

    Args:
        message (str): Prompt displayed to the user.

    Returns:
        str: The validated filename.
    """
    while True:
        filename = input(message).strip().title()
        if ensure_valid_filename(filename):
            return filename
        else:
            continue

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
    content = file_logo + "\n" + content
    ensure_output_directory()
    try:
        with open(f"output/{filename}", "w", encoding="utf-8") as file:
            file.write(content)
            print(f"File: {FOLDER_PATH}{filename} - Has been Created.")
    except OSError as e:
        sys.exit(f"File Write error: {e}")
