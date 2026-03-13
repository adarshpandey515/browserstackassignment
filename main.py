from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from scraper import get_first_five_articles, get_article_content_and_image
from utils import download_image, translate_titles, find_repeated_words


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