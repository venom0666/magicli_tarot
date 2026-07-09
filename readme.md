# **MAGICLI_TAROT**

#### Video Demo: <TODO>

#### Description

**MagicLI Tarot** is a command-line Python application that simulates tarot card readings using traditional tarot spreads and Google's Gemini API. The program randomly draws cards from a standard 78-card tarot deck, assigns upright or reversed orientations, and generates a detailed interpretation based on the selected spread.

Users can choose from several predefined spreads or create a custom spread, specify the output language, AI model and optionally save the reading as a Markdown file.

With the Power of **Python** and **AI**, we are bringing Tarot Readings to the comfort of your own CLI

## Features

    - 78-card tarot deck
    - Multiple predefined spreads
    - Custom spreads
    - Random upright/reversed cards
    - AI-generated interpretations using Gemini
    - Multiple output languages
    - Save readings as Markdown
    - Interactive mode
    - Command-line mode
    - Reproducible readings with --seed

## Requirements

    - Python 3.13.12+
    - google-genai==2.10.0
    - python-dotenv==1.2.2

```bash
pip install -r requirements.txt

```

## Usage

### Interactive mode

```bash
python magicli_tarot.py

```

Example

```
Select the Tarot Reading Type:
 1 - Situation, Obstacle, Advice
 2 - Celtic Cross
 3 - Compass Spread
 4 - Dream Messages
 5 - General Spread
 6 - Your Life Right Now
 7 - Love Spread
 8 - Hierarchy of Needs
 9 - Past, Present, Future
10 - Two Paths
11 - Today's Energy
12 - Custom
 Q - Quit

Choice: 1

Output Language (leave empty for English):
```

### Command line

```bash
python magicli_tarot.py -t Celtic

```

#### Example help:

```bash
$ python magicli_tarot.py --help
usage: magicli-tarot.py [-h] [-t {Advice,Celtic,Compass,Dream,General,Life,Love,Needs,Past,Path,Today}]
                  [-l LANG]
                  [--model {gemini-2.5-flash,gemini-2.5-flash-lite,gemini-3.5-flash,gemini-3.1-flash-lite}]
                  [--seed SEED] [--sign] [--nosign] [--save] [--nosave]

Magicli_tarot brings the Power of Python and AI, to create insightful
tarot readings delivering them to the comfort of your own CLI.

options:
  -h, --help            show this help message and exit
  -t, --type {Advice,Celtic,Compass,Dream,General,Life,Love,Needs,Past,Path,Today}
                        Tarot spread type
  -l, --lang LANG       Output language (default: English)
  --model {gemini-2.5-flash,gemini-2.5-flash-lite,gemini-3.5-flash,gemini-3.1-flash-lite}
                        Model to interpret readings
  --seed SEED           Random seed
  --sign                Automatically add signature from response
  --nosign              Automatically remove signature from response
  --save                Automatically save to .md file
  --nosave              Automatically don't save to .md file
```

#### Type and Language

```bash
python magicli_tarot.py -t General -l Spanish

```

#### Type, Language, Seed, Sign and Nosave

```bash
python magicli_tarot.py -t Dream -l Spanish --seed 58 --sign --nosave

```

## Project Structure TODO

- magicli_tarot.py
- api.py
- logic.py
- tarot.py
- test_magicli_tarot.py
- requirements.txt
- readme.md

**Briefly explain each file**

## Design Decisions TODO

Explain why you wrote it this way.

For example:

I separated the application into functions that each perform a single task. get_cards() is responsible only for drawing cards, while interpret_tarot() handles communication with the Gemini API. This separation makes the code easier to understand and test.

Talk about:

why dictionaries represent spreads
why argparse
why Markdown output
why --seed
why random orientations

This section is often what distinguishes a good project from a great one.

## Testing

The project includes automated tests using pytest.

Tests verify:

- Number of cards drawn
- Validate orientation for drawn cards
- No duplicate cards
- Spread generation
- Model selection
- Reading types retrieval
- Exact cards drawn with seed
- Exact model selected with seed

## Limitations TODO

Every project has them.

Example:

The interpretation depends on the Gemini API and therefore requires an internet connection.

## Future Improvements TODO

For example

- HTML, DOC and PDF export
- Card images with an image generator for HTML, DOC and PDF
- Reading history
- User profiles
- Multiple AI providers
