import requests
from bs4 import BeautifulSoup
import csv
import os
import re


def scrape_ystudios_advanced():
    url = "https://ystudios.net/collections/spring-2026"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    products_data = []

    print("Starting YStudio Advanced Scraper")
    print("=" * 50)

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")

        products = soup.find_all("li", class_="grid__item")

        print(f"Found {len(products)} product containers\n")

        for index, product in enumerate(products, 1):
            name_element = product.find("h3", class_="card__heading")
            name = "N/A"
            if name_element:
                name_link = name_element.find("a")
                name = name_link.text.strip() if name_link else "N/A"

            colors = []
            color_picker = product.find("div", class_="card-information__color-picker")
            if color_picker:
                color_labels = color_picker.find_all("label")
                for label in color_labels:
                    title = label.get("title", "")
                    if title:
                        colors.append(title)

            primary_color = colors[0] if colors else "N/A"
            color_element = product.find("p", class_="card-information__color-label")
            if color_element:
                primary_color = color_element.text.strip()

            price_element = product.find("div", class_="price")
            price = "N/A"
            if price_element:
                sale_price = price_element.find("span", class_="price-item--sale")
                if sale_price:
                    price = sale_price.text.strip()
                else:
                    regular_price = price_element.find(
                        "span", class_="price-item--regular"
                    )
                    price = regular_price.text.strip() if regular_price else "N/A"

            price_number = re.sub(r"[^0-9.]", "", price) if price != "N/A" else "0"

            badges = []
            badges_container = product.find("div", class_="card__product-badges")
            if badges_container:
                badge_elements = badges_container.find_all(
                    "div", class_="product-badge"
                )
                badges = [badge.text.strip() for badge in badge_elements]

            status = "Available"
            if any("Sold" in b or "sold" in str(product).lower() for b in badges):
                status = "Sold Out"
            elif any("Pre-Order" in b for b in badges):
                status = "Pre-Order"
            elif "Restocked" in badges:
                status = "Restocked"

            link_element = product.find("a", {"data-card-product-link": True})
            product_url = link_element.get("href") if link_element else "N/A"

            products_data.append(
                {
                    "Name": name,
                    "Primary_Color": primary_color,
                    "All_Colors": ", ".join(colors) if colors else primary_color,
                    "Price": price,
                    "Price_Numeric": price_number,
                    "Status": status,
                    "Badges": ", ".join(badges),
                    "Product_URL": f"https://ystudios.net{product_url}"
                    if product_url != "N/A"
                    else "N/A",
                }
            )

            print(f"{index:2}. {name} | Color: {primary_color} | {price} | {status}")
            if len(colors) > 1:
                print(f"     Also available in: {', '.join(colors[1:])}")

        if products_data:
            os.makedirs("data", exist_ok=True)

            with open(
                "data/ystudios_products_detailed.csv", "w", newline="", encoding="utf-8"
            ) as csvfile:
                fieldnames = [
                    "Name",
                    "Primary_Color",
                    "All_Colors",
                    "Price",
                    "Price_Numeric",
                    "Status",
                    "Badges",
                    "Product_URL",
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(products_data)

            print("\n" + "=" * 50)
            print(" SCRAPING COMPLETE!")
            print(f" Total products: {len(products_data)}")

            prices = [
                float(p["Price_Numeric"])
                for p in products_data
                if p["Price_Numeric"] != "0"
            ]
            if prices:
                print(f" Average price: LE {sum(prices) / len(prices):.2f}")
                print(f" Most expensive: LE {max(prices):.2f}")
                print(f"Cheapest: LE {min(prices):.2f}")

            print("Saved to: data/ystudios_products_detailed.csv")
            print("=" * 50)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    scrape_ystudios_advanced()
