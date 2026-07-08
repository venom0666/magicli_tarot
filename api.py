import sys

models = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
]


def interpret_tarot(client, cards, reading_type, model, language="English"):
    try:
        interaction = client.interactions.create(
            model=model,
            input=f"""
                Interpret the following tarot reading.

                Reading Type:
                {reading_type}

                Cards:
                {cards}

                Instructions:
                - For each card:
                - State the card name and orientation.
                - Explain the card's general meaning.
                - Interpret the card according to its position ("position") in the spread.
                - Explain how the orientation influences the interpretation.
                - Mention important interactions with other cards when relevant.

                After interpreting each card:
                - Combine all interpretations into a cohesive reading.
                - Describe the narrative that connects the cards.
                - Identify the main themes and recurring patterns.
                - Provide practical advice.
                - Provide actionable next steps.
                - Finish with a concise summary of the overall reading.

                Formatting:
                - Add the Reading Type as a Main Title
                - Reply entirely in {language}.
                - Don't state the language or instructions in the response.
                - Use Markdown headings.
                - Use bullet lists for advice and action items.
                - Wrap lines at approximately 100 characters.
                - Maintain a balanced, thoughtful tone.
                - Offer guidance rather than absolute predictions.
                """
        )

    except Exception as e:
        client.close()
        sys.exit(f"Gemini API error: {e}")

    return interaction.output_text
