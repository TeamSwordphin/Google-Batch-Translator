import json
import os
import tkinter as tk
from tkinter import filedialog

import six
from google.cloud import translate_v2 as translate

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/json/credentials"
translate_client = translate.Client()


# Initialize Translator
def translate_text(target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    # 	print(u"Text: {}".format(result["input"]))
    # 	print(u"Translation: {}".format(result["translatedText"]))
    # 	print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))

    return result["translatedText"]


# Initialize Windows Explorer file prompter
root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()

# Open json file
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Create new proxy json
with open("output.json", "w", encoding="utf8") as outputFile:
    newData = {}
    currentLine = 1

    for key, value in data.items():
        if len(value) <= 1 or value[0:3].encode().isalpha():
            # Either the string is too short or is in english, don't need to translate it
            print(
                "Line either too short or is already in english. Line "
                + str(currentLine)
            )
            newData[key] = value
        else:
            translatedSentence = translate_text("en", value)
            newData[key] = translatedSentence
            print("Translated line " + str(currentLine) + " - " + translatedSentence)

        currentLine += 1

    # Output json file
    json.dump(newData, outputFile, ensure_ascii=False)
    print("Processed Lines - " + str(len(newData)))
