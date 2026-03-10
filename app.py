import requests
from collections import Counter
from urllib.parse import urljoin
from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup
from collections import Counter

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


BASE_URL = "https://elpais.com/opinion/"


def get_first_five_articles(driver):
    driver.get(BASE_URL)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    anchors = soup.select("article h2 a")

    titles = []
    links = []

    for a in anchors:
        title = a.get_text(strip=True)
        link = a.get("href")

        if not link:
            continue

        link = urljoin("https://elpais.com", link)

        # keep only real opinion articles
        if "/opinion/" not in link:
            continue

        if not link.endswith(".html"):
            continue

        titles.append(title)
        links.append(link)

        if len(links) == 5:
            break

    return titles, links


def get_article_content_and_image(driver, url):
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    paragraphs = soup.select('div[data-dtm-region="articulo_cuerpo"] p')

    content = []
    for p in paragraphs:
        text = p.get_text(strip=True)
        if text:
            content.append(text)

    content_text = "\n".join(content)

    img_tag = soup.select_one("figure img")
    img_url = None

    if img_tag:
        img_url = img_tag.get("src")

    return content_text, img_url


def download_image(url, index):
    if not url:
        print("No image found")
        return

    try:
        r = requests.get(url, timeout=10)

        filename = f"article_{index}.jpg"

        with open(filename, "wb") as f:
            f.write(r.content)

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


def main():

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options)

    try:

        titles, links = get_first_five_articles(driver)

        print("\nFIRST 5 OPINION ARTICLES (SPANISH)\n")

        for i in range(len(links)):

            print("\n-----------------------------")
            print("TITLE:", titles[i])
            print("-----------------------------\n")

            content, img = get_article_content_and_image(driver, links[i])

            print(content[:500])

            download_image(img, i + 1)

        translated_titles = translate_titles(titles)

        print("\nTRANSLATED TITLES (ENGLISH)\n")

        for t in translated_titles:
            print(t)

        find_repeated_words(translated_titles)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()