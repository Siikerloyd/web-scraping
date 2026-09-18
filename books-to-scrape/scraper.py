import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import csv


base_url = "https://books.toscrape.com/"

books_data = []

rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}


for page in range(1, 51):

    if page == 1:
        url = base_url
    else:
        url = f"{base_url}catalogue/page-{page}.html"

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.select("article.product_pod")

    for book in books:

        # Title from listing page
        title = book.select_one("h3 a").get_text(strip=True)

        # Price
        price = book.select_one(".price_color").get_text(strip=True)
        price = float(price.replace("£", ""))

        # Rating
        rating_element = book.select_one(".star-rating")
        rating = rating_map[rating_element["class"][1]]

        # Book link
        book_link = book.select_one("h3 a")["href"]

        if book_link.startswith("catalogue/"):
            book_url = urljoin(base_url, book_link)
        else:
            book_url = urljoin(
                base_url + "catalogue/",
                book_link
            )

        # Image
        image = book.select_one(".image_container img")
        image_url = urljoin(base_url, image["src"])

        # Detail page request
        try:
            detail_response = requests.get(
                book_url,
                timeout=10
            )

            detail_response.raise_for_status()
            detail_response.encoding = "utf-8"

        except requests.RequestException as error:
            print(f"Failed to scrape: {book_url}")
            print(f"Error: {error}")
            continue

        detail_soup = BeautifulSoup(
            detail_response.text,
            "html.parser"
        )

        # Full title from detail page
        title_element = detail_soup.select_one("h1")

        if title_element:
            title = title_element.get_text(strip=True)

        # Description
        description_element = detail_soup.select_one(
            "#product_description + p"
        )

        if description_element:
            description = description_element.get_text(strip=True)
        else:
            description = None

        # Create book dictionary
        book_data = {
            "title": title,
            "price": price,
            "rating": rating,
            "image_url": image_url,
            "book_url": book_url,
            "description": description
        }

        books_data.append(book_data)

    print(f"Page {page}: {len(books)} books scraped")


print("Total books scraped:", len(books_data))


# Save JSON
with open(
    "books.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        books_data,
        file,
        indent=4,
        ensure_ascii=False
    )

print("Data saved to books.json")


# Save CSV
with open(
    "books.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    fieldnames = [
        "title",
        "price",
        "rating",
        "image_url",
        "book_url",
        "description"
    ]

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(books_data)

print("Data saved to books.csv")