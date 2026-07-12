import datetime
import os
import re 
import sys
import logic
from markdown_pdf import MarkdownPdf, Section
from constants import FOLDER_PATH, file_logo, html_file_logo, filetypes, logo
import markdown



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
    message = "Would you like to save the reading to a File? Y/N: "    
    now = datetime.datetime.now().strftime("%B-%d-%Y_%H-%M")
    if args.save:
        filename = set_default_filename(reading, now, reader) if not args.filename else args.filename
        write_file(filename, content, args)
    elif not args.nosave:
        choice = logic.prompt_yes_no(message)
        if choice == "Y":
            filename = change_filename(reading,args, now, reader)
            write_file(filename, content, args)

def ensure_output_directory(folder):
    """
    Ensure that the output directory exists.

    Creates the output directory if it does not already exist.
    """
    if not os.path.isdir(folder):
        os.mkdir(folder)
        print(f"Folder: {folder} - Has been created.")

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
    message = f"""Default filename : {set_default_filename(reading, now, reader)}
    Would you like to keep this filename? Y/N: """
    if args.filename:
        filename = args.filename
        return f"{filename}_{now}.md"
    while True:
        choice = logic.prompt_yes_no(message)
        if choice == "N":
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
    filename = (f"{reader["Name"]}_{reading}_{now}"
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

def write_file(filename, content, args):
    ensure_output_directory(FOLDER_PATH)
    #add conditional if args.save skip print menu
    if not args.save:
        print("\nSelect File Format: ")
        for _ in range(len(filetypes)):
            print(f"{_ +1} - {sorted(filetypes)[_]}")
    while True:
        if not (args.ext and args.save):
            try:
                choice = int(input("Choice: "))
                choice = sorted(filetypes)[choice - 1] if choice > 0 else None
            except TypeError,ValueError,IndexError:
                print("Invalid choice.")
                continue
        else:
            choice = args.ext
        match choice:
            case "Html":
                write_to_html(filename, content)
                break
            case "Md":
                write_to_md(filename, content)
                break
            case "Pdf":
                write_to_pdf(filename, content) 
                break
            case "Txt":
                write_to_txt(filename, content) 
                break
            case _:
                print("Invalid choice")
                continue




def write_to_md(filename, content):
    """
    Write text content to a Markdown file in the output directory.
    If output directory does not exist it will be created.

    Args:
        filename (str): Name of the file to create.
        content (str): Text to write to the file.

    Raises:
        SystemExit: If the file cannot be written.
    """
    ensure_output_directory(f"{FOLDER_PATH}Markdown/")
    content = file_logo + "\n" + content

    try:
        with open(f"{FOLDER_PATH}MD/{filename}.md", "w", encoding="utf-8") as file:
            file.write(content)
            print(f"File: {FOLDER_PATH}MD/{filename}.md - Has been Created.")
    except OSError as e:
        sys.exit(f"File Write error: {e}")

def write_to_pdf(filename, content):
    """
        Write text content to a Pdf file in the output directory.
        If output directory does not exist it will be created.
    
        Args:
            filename (str): Name of the file to create.
            content (str): Text to write to the file.
    
        Raises:
            SystemExit: If the file cannot be written.
        """

    ensure_output_directory(f"{FOLDER_PATH}PDF/")

    content = html_file_logo + "\n" + content

    pdf = MarkdownPdf(toc_level=2, optimize=True)
    user_css="""body  {font-family: 'FiraMono Nerd Font', monospace;}
    div {line-height: 1;}"""
    pdf.add_section(Section(content), user_css=user_css)
    


    try:
        pdf.save(f"{FOLDER_PATH}PDF/{filename}.pdf")
        print(f"File: {FOLDER_PATH}PDF/{filename}.pdf - Has been Created.")
    except OSError as e:
        sys.exit(f"File Write error: {e}")

def write_to_html(filename, content):
    """
        Write text content to a Html file in the output directory.
        If output directory does not exist it will be created.
    
        Args:
            filename (str): Name of the file to create.
            content (str): Text to write to the file.
    
        Raises:
            SystemExit: If the file cannot be written.
        """

    content = html_file_logo + "\n" + content

    content = markdown.markdown(content)
    ensure_output_directory(f"{FOLDER_PATH}HTML/")


    try:
        with open(f"{FOLDER_PATH}HTML/{filename}.html", "w", encoding="utf-8", errors="xmlcharrefreplace") as file:
            file.write(content)
            print(f"File: {FOLDER_PATH}HTML/{filename}.html - Has been Created.")
    except OSError as e:
        sys.exit(f"File Write error: {e}")


def write_to_txt(filename, content):
    """
    Write text content to a Txt file in the output directory.
    If output directory does not exist it will be created.

    Args:
        filename (str): Name of the file to create.
        content (str): Text to write to the file.

    Raises:
        SystemExit: If the file cannot be written.
    """
    ensure_output_directory(f"{FOLDER_PATH}TXT/")
    content = logo + "\n" + content

    try:
        with open(f"{FOLDER_PATH}TXT/{filename}.txt", "w", encoding="utf-8") as file:
            file.write(content)
            print(f"File: {FOLDER_PATH}TXT/{filename}.txt - Has been Created.")
    except OSError as e:
        sys.exit(f"File Write error: {e}")
