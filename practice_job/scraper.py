import json
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.pagesjaunes.fr"
SEARCH_URL = f"{BASE_URL}/annuaire/region/ile-de-france/geometre"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def get_soup(url: str) -> BeautifulSoup:
    """Fetch a webpage and return a BeautifulSoup object."""
    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def get_text(element, selector: str = None) -> str | None:
    """Safely extract stripped text from an element or sub-selector."""
    target = element.select_one(selector) if selector else element
    return target.get_text(" ", strip=True) if target else None

def extract_hours(soup: BeautifulSoup) -> dict:
    """Extract opening hours table."""
    hours = {}
    rows = soup.select("#bloc-horaires table.liste-horaires-principaux tr")

    for row in rows:
        day_el = row.select_one(".jour")
        if not day_el:
            continue

        day = day_el.get_text(" ", strip=True)
        times = [t.get_text(" ", strip=True) for t in row.select(".horaire")]
        closed = row.select_one(".ferme")

        if times:
            hours[day] = " / ".join(times)
        elif closed:
            hours[day] = closed.get_text(" ", strip=True)
        else:
            hours[day] = None

    return hours

def extract_dl_data(soup: BeautifulSoup, selector: str) -> dict:
    """Extract key-value pairs from a definition list (<dl>)."""
    data = {}
    dl_block = soup.select_one(selector)
    if not dl_block:
        return data

    items = dl_block.find_all(["dt", "dd"])
    for i in range(0, len(items) - 1, 2):
        key = items[i].get_text(" ", strip=True)
        val = items[i + 1].get_text(" ", strip=True)
        data[key] = val

    return data

def parse_detail_page(url: str) -> dict:
    """Scrape all fields from a single listing detail page."""
    soup = get_soup(url)

    image_el = soup.select_one("figure.header-visuel img")
    image_url = urljoin(BASE_URL, image_el["src"]) if image_el and image_el.get("src") else None

    facebook_el = soup.select_one("a.FACEBOOK")
    facebook_data = facebook_el.get("data-pjlb") if facebook_el else None

    prestations = [
        li.get_text(" ", strip=True)
        for li in soup.select(".prestations.generique ul.list-v li span")
    ]
    print("Establishment element:", soup.select_one("dl.info-etablissement"))
    print("Company element:", soup.select_one("dl.info-entreprise"))

    return {
        "url": url,
        "title": get_text(soup, "h1.pjts_denom"),
        "activity": get_text(soup, ".zone-activites .activite"),
        "address": get_text(soup, ".pjts_address"),
        "phone": get_text(soup, ".coord-numero"),
        "website": get_text(soup, ".SITE_EXTERNE .value"),
        "facebook_data": facebook_data,
        "image_url": image_url,
        "description": get_text(soup, "#teaser-description .description p"),
        "prestations": prestations,
        "hours": extract_hours(soup),
        "establishment": extract_dl_data(soup, "dl.info-etablissement"),
        "company": extract_dl_data(soup, "dl.info-entreprise"),
    }

def main():
    # 1. Fetch main search page
    print(f"Fetching search results from: {SEARCH_URL}")
    soup = get_soup(SEARCH_URL)
    listings = soup.select("li.bi")
     # Check for pagination
    pagination_links = soup.select("a[href]")

    for link in pagination_links:
        text = link.get_text(" ", strip=True)
        href = link.get("href")

        if text in ["2", "3", "4", "Suivant", "Next"] or "page" in (href or "").lower():
            print("TEXT:", text)
            print("HREF:", href)
            print("-" * 40)

    print(f"Found {len(listings)} listings.")

    # 2. Extract detail links
    detail_links = []
    for listing in listings:
        link_el = listing.select_one("a.bi-denomination")
        if link_el and link_el.get("href"):
            full_url = urljoin(BASE_URL, link_el["href"])
            detail_links.append(full_url)

    print(f"Found {len(detail_links)} listings.")

    # 3. Scrape the first listing as a test
    if detail_links:
        id="k8m2pa"
        for url in detail_links[:5]:
            print(f"\nScraping: {url}\n")
            data = parse_detail_page(url)
            print(json.dumps(data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()