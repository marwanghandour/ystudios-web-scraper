# ystudios-web-scraper# YStudio Product Scraper

A Python web scraper that extracts product data from YStudio's Spring 2026 collection.

## 🚀 Features

- Extracts product names, colors, prices, and availability status
- Handles multiple color variants per product
- Identifies special status (Pre-Order, Sold Out, Restocked)
- Exports clean CSV files ready for Excel/Google Sheets
- Respectful scraping with proper headers and delays

## 📊 Data Extracted

| Field | Description |
|-------|-------------|
| Name | Product name |
| Color | Primary color/variant |
| Price | Current price (LE currency) |
| Status | Available, Sold Out, or Pre-Order |
| Badges | Product tags (Men, Restocked, etc.) |
| Product URL | Direct link to product |

## 🛠️ Technologies Used

- Python 3.x
- Requests - HTTP requests
- BeautifulSoup4 - HTML parsing
- CSV module - Data export

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/marwanghandour/ystudios-web-scraper.git

# Install requirements
pip install -r requirements.txt

# Run the scraper
python scraper.py
