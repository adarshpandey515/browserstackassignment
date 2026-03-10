# El País Opinion Scraper

## Overview

This project is a small web scraping script that collects articles from the **Opinion section of El País**, a Spanish news website.

The script automatically:

* Opens the El País Opinion page
* Extracts the first **5 opinion articles**
* Prints the **title and first 500 characters of the article content in Spanish**
* Downloads the **cover image** of each article if available
* Translates the **article titles to English**
* Analyzes translated titles and finds **words repeated more than twice**

This project demonstrates basic skills in **web scraping, API usage, and text processing**.

---

## Features

* Scrapes the **first 5 articles** from the Opinion section
* Extracts **article titles and content**
* Downloads **cover images**
* Translates titles using **Google Translator API**
* Performs **word frequency analysis** on translated titles
* Handles **non-article pages (like tags)** by filtering valid article URLs
* Avoids Selenium errors such as stale elements

---

## Technologies Used

* **Python**
* **Selenium** – to load web pages
* **BeautifulSoup** – to parse HTML
* **Requests** – to download images
* **Deep Translator** – to translate Spanish titles to English
* **Collections (Counter)** – for word frequency analysis

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd elpais-opinion-scraper
```

### 2. Install dependencies

```bash
pip install selenium
pip install beautifulsoup4
pip install deep-translator
pip install requests
```

### 3. Install ChromeDriver

Download ChromeDriver matching your Chrome version and ensure it is available in your system PATH.

---

## Project Structure

```
project-folder/
│
├── app.py
├── README.md
├── article_1.jpg
├── article_2.jpg
├── article_3.jpg
├── article_4.jpg
└── article_5.jpg
```

Images will be saved automatically after running the script.

---

## How the Script Works

1. **Open Opinion Section**

   * The script loads the El País opinion page.

2. **Extract Article Links**

   * It collects article titles and links.
   * Only links ending with `.html` are selected to ensure they are real articles.

3. **Scrape Article Content**

   * Each article page is opened.
   * The first **500 characters of Spanish article text** are extracted.

4. **Download Cover Image**

   * If an article has a cover image, it is downloaded locally.

5. **Translate Titles**

   * Article titles are translated from Spanish to English using GoogleTranslator.

6. **Word Frequency Analysis**

   * The script counts words across translated titles.
   * Words appearing **more than twice** are printed.

---

## Example Output

```
FIRST 5 OPINION ARTICLES (SPANISH)

TITLE: La democracia y sus desafíos

La democracia enfrenta nuevos retos en el contexto global actual...

Image saved: article_1.jpg

Translated Titles (English)

Democracy and its challenges
The future of European politics
...

Words repeated more than twice:
democracy : 3
```

---

# Note:
export BROWSERSTACK_USERNAME=your_username

export BROWSERSTACK_ACCESS_KEY=your_access_key

# output

browserstack
![](/screenshot/image.png)

Terminal
![](/screenshot/image2.png)

## Notes

* The script only prints **500 characters of each article** to keep output readable.
* Some articles may not contain cover images; the script handles this case safely.
* Filtering ensures non-article pages (tags, categories) are ignored.

---

## Possible Improvements

* Save scraped articles into a **CSV or JSON file**
* Add **automatic retries for network errors**
* Use **async scraping** for faster execution
* Perform deeper **text analysis or sentiment analysis**

---

## Author

Adarsh Pandey
