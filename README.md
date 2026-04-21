# ystudios-web-scraper

I built this to scrape product data from YStudio's Spring 2026 collection.

## What it does

- Pulls product names, colors, prices, availability
- Handles multiple color variants per product
- Saves everything to CSV and Excel
- Generates a simple report with price stats

## Tech stack

- Python 3
- BeautifulSoup for scraping
- Pandas for data work
- Requests for HTTP calls

## How to run

```bash
pip install -r requirements.txt
python scraper.py
python analyze.py
