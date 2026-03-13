import urllib.request
from deep_translator import GoogleTranslator
from collections import Counter


def download_image(url, index):

    if not url:
        print("No image found")
        return

    try:

        filename = f"article_{index}.jpg"

        urllib.request.urlretrieve(url, filename)

        print("Image saved:", filename)

    except:
        print("Could not download image")


def translate_titles(spanish_titles):

    translator = GoogleTranslator(source="es", target="en")

    translated = []

    for t in spanish_titles:
        translated.append(translator.translate(t))

    return translated


def find_repeated_words(titles):

    words = []

    for t in titles:
        words += t.lower().split()

    counter = Counter(words)

    found = False

    for word, count in counter.items():

        if count > 2:

            print("\nWords repeated more than twice:\n")
            print(word, ":", count)

            found = True

    if not found:
        print("No words repeated more than twice")