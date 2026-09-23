import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import csv


def get_text_or_none(soup, selector):
    element = soup.select_one(selector)

    if not element:
        return None

    text = element.get_text(strip=True)

    if not text:
        return None

    return text


def get_attr_or_none(soup, selector, attribute):
    element = soup.select_one(selector)

    if not element:
        return None

    return element.get(attribute)


all_quotes = []

for page in range (1, 11):

    if page == 1:
        url = "https://quotes.toscrape.com"
    else:
        url = f"https://quotes.toscrape.com/page/{page}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

    except requests.RequestException as e:
        print(f"Page {page} request failed: {e}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    quotes = soup.select(".quote")

    for quote_index, quote in enumerate(quotes, start=1):

        try:
            text = get_text_or_none(quote, "span.text")

            author = get_text_or_none(quote, "small.author")

            tag_elements = quote.select("a.tag")

            tags = [
                tag.get_text(strip=True)
                for tag in tag_elements
            ]

            relative_url = get_attr_or_none(
                quote,
                "span a",
                "href"
            )

            if not relative_url:
                print(
                    f"Quote {quote_index}: "
                    "Author URL is missing, skipping quote."
                )
                continue

            author_url = urljoin(url, relative_url)

            try:
                author_response = requests.get(
                    author_url,
                    timeout=10
                )

                author_response.raise_for_status()

                author_soup = BeautifulSoup(
                    author_response.text,
                    "html.parser"
                )

                author_born_date = get_text_or_none(
                    author_soup,
                    "span.author-born-date"
                )

                author_born_location = get_text_or_none(
                    author_soup,
                    "span.author-born-location"
                )

                author_description = get_text_or_none(
                    author_soup,
                    ".author-description"
                )

                full_quote_details = {
                    "Author_name": author,
                    "quote": text,
                    "tags": tags,
                    "birth_date": author_born_date,
                    "birth_location": author_born_location,
                    "author_description": author_description
                }

                all_quotes.append(full_quote_details)

            except requests.RequestException as e:
                print(f"Author request failed: {e}")
                continue

        except Exception as e:
            print(f"Quote {quote_index} failed: {e}")
            continue


with open("quotes.json", "w", encoding="utf-8") as file:
    json.dump(
        all_quotes,
        file,
        ensure_ascii=False,
        indent=4
    )


if len(all_quotes) > 0:

    with open(
        "quotes.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=all_quotes[0].keys()
        )

        writer.writeheader()

        for quote in all_quotes:
            row = quote.copy()
            row["tags"] = ", ".join(row["tags"])
            writer.writerow(row)

else:
    print("Failed to scrape any quotes.")