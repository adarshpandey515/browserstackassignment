# El Pais Opinion Scraper + BrowserStack Test

This project does:
- Open El Pais Opinion page and check Spanish language signal.
- Grab first 5 opinion articles.
- Print title + article content in Spanish.
- Download cover image if available.
- Translate article titles to English.
- Count words repeated more than 2 times in translated titles.
- Run BrowserStack checks in 5 parallel sessions (desktop + mobile mix).

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run scraper app

```bash
python app.py
```

