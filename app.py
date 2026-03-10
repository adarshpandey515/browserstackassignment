import re
from collections import Counter
from urllib.parse import urljoin, urlparse

from deep_translator import GoogleTranslator
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "https://elpais.com"
OPINION_URL = "https://elpais.com/opinion/"


# this one filters only real article links in opinion section

def looks_like_real_opinion_article(one_link):
    if not one_link:
        return False

    parsed = urlparse(one_link)
    path_value = parsed.path.lower()

    if "/opinion/" not in path_value:
        return False

    skip_parts = [
        "/opinion/",
        "/opinion/editoriales",
        "/opinion/columnas",
        "/opinion/tribunas",
        "/opinion/cartas-al-director",
        "/autor/",
        "/tag/",
    ]

    for one_skip in skip_parts:
        if path_value.rstrip("/") == one_skip.rstrip("/"):
            return False

    # usually article url has date like /2026-03-10/
    if re.search(r"/\d{4}-\d{2}-\d{2}/", path_value):
        return True

    # fallback if last slug looks article-like
    bits = [x for x in path_value.split("/") if x]
    return len(bits) >= 4



def get_first_five_headlines(driver):
    driver.get(OPINION_URL)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "article"))
    )

    lang_now = driver.execute_script(
        "return document.documentElement.lang || '';"
    )
    print("Website lang:", lang_now)
    if "es" in str(lang_now).lower():
        print("Spanish check passed.")
    else:
        print("Spanish check uncertain, continuing.")

    links_collected = []
    already_seen = set()

    all_anchors = driver.find_elements(By.CSS_SELECTOR, "article a")
    for a in all_anchors:
        href = (a.get_attribute("href") or "").strip()
        txt = (a.text or "").strip()

        if not href:
            continue

        href = urljoin(BASE_URL, href)

        if href in already_seen:
            continue

        if not looks_like_real_opinion_article(href):
            continue

        if not txt:
            continue

        links_collected.append({"title_es": txt, "url": href})
        already_seen.add(href)

        if len(links_collected) == 5:
            break

    return links_collected



def translate_titles(all_titles_es):
    translator_obj = GoogleTranslator(source="es", target="en")
    out_data = []

    for t in all_titles_es:
        try:
            out_data.append(translator_obj.translate(t))
        except Exception:
            out_data.append("(translation failed)")

    return out_data



def repeated_words_more_than_two(all_titles_en):
    bag = []
    for title in all_titles_en:
        words = re.findall(r"[a-z']+", title.lower())
        bag.extend(words)

    counter_data = Counter(bag)
    return {k: v for k, v in counter_data.items() if v > 2}



def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        first_five = get_first_five_headlines(driver)

        if not first_five:
            print("No headlines found")
            return

        print("\nFirst 5 Opinion headlines in Spanish:")
        title_list_es = []
        for i, h in enumerate(first_five, 1):
            print(f"{i}. {h['title_es']}")
            print(f"   {h['url']}")
            title_list_es.append(h["title_es"])

        translated = translate_titles(title_list_es)
        print("\nTranslated headlines in English:")
        for i, line in enumerate(translated, 1):
            print(f"{i}. {line}")

        repeated = repeated_words_more_than_two(translated)
        print("\nWords repeated more than 2 times:")
        if not repeated:
            print("No repeated words over threshold")
        else:
            for w, c in sorted(repeated.items(), key=lambda x: (-x[1], x[0])):
                print(f"{w}: {c}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
