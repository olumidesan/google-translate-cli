

import time
import dryscrape

import urllib.parse as Parser

from utils import iso_639_1_codes, has_internet

session = dryscrape.Session()

# This might change depending on one's location, or actually, at Google's whim
BASE_GOOGLE_TRANSLATE_URL = "https://translate.google.com/?hl=en#view=home&op=translate"

# May also change at a point
TRANSLATED_TEXT_SELECTOR = "body > div.frame > div.page.tlid-homepage.homepage.translate-text > div.homepage-content-wrap > \
                            div.tlid-source-target.main-header > div.source-target-row > div.tlid-results-container.results-container \
                            > div.tlid-result.result-dict-wrapper > div.result.tlid-copy-target > div.text-wrap.tlid-copy-target > div \
                            > span.tlid-translation.translation"


def encode_query_parameters(s, d, t):
    parameters = dict(sl=s, tl=d, text=t)

    return "&" + Parser.urlencode(parameters, quote_via=Parser.quote)


def get_input():

    while 1:
        try:
            source_language = iso_639_1_codes[input('Enter the source language for the text you want to translate: ').lower()]
            destination_language = iso_639_1_codes[input('Enter the destination language for the text you want to translate: ').lower()]
        except KeyError:
            print("\nSorry, text translation for that language isn't supported. Try another language.\n")
            continue
        else:
            break

    text_to_translate = input(f'Enter the text that you want to translate: ').lower()

    query_string = BASE_GOOGLE_TRANSLATE_URL + encode_query_parameters(source_language, destination_language, text_to_translate)

    return query_string


def main():

    if has_internet():

        url = get_input()

        print("\nTranslating...")

        session.visit(url)
        translated_text = session.at_css(TRANSLATED_TEXT_SELECTOR).text()

        return f"\nTranslation: {translated_text}\n"
    
    return "It looks like you have no internet connection. :( Kindly connect to the internet and try again.\n"


if __name__ == "__main__":
    print(main())








