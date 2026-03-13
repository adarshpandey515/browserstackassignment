from urllib.parse import urljoin
from selenium.webdriver.common.by import By

BASE_URL = "https://elpais.com/opinion/"


def get_first_five_articles(driver):

    driver.get(BASE_URL)

    anchors = driver.find_elements(By.CSS_SELECTOR, "article h2 a")

    titles = []
    links = []

    for a in anchors:

        title = a.text
        link = a.get_attribute("href")

        if not link:
            continue

        link = urljoin("https://elpais.com", link)

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

    paragraphs = driver.find_elements(
        By.CSS_SELECTOR,
        'div[data-dtm-region="articulo_cuerpo"] p'
    )

    content = []

    for p in paragraphs:
        text = p.text
        if text:
            content.append(text)

    content_text = "\n".join(content)

    img_url = None

    try:
        img = driver.find_element(By.CSS_SELECTOR, "figure img")
        img_url = img.get_attribute("src")
    except:
        pass

    return content_text, img_url