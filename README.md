# Web Scraping

A collection of Python web scraping projects built to develop practical web scraping skills, progressing from basic static websites to more advanced scraping techniques.

## Purpose

This repository documents my progression in web scraping through hands-on projects.

The goal is to learn how to:

* Extract structured data from websites
* Navigate and parse HTML
* Handle pagination and multiple pages
* Follow links and scrape detailed pages
* Clean and transform extracted data
* Handle request errors and unexpected responses
* Export scraped data into useful formats
* Work with dynamic websites
* Store scraped data in databases
* Build more complete and production-oriented scraping applications

## Learning Progression

### 🟢 Basic — Static Websites

Focus:

* `requests`
* `BeautifulSoup`
* HTML/CSS selectors
* Pagination
* URL handling
* Data extraction
* Basic error handling
* CSV and JSON export

Projects:

* **Books to Scrape**

### 🟡 Medium — More Complex Websites

Focus:

* More complex page structures
* Multiple types of data
* Following links between pages
* More robust error handling
* Data cleaning and normalization
* Handling larger scraping tasks
* Working with less predictable website structures

Projects:

* **Quotes to Scrape**
* Additional projects to be added

### 🔴 Advanced — Dynamic & Data Applications

Focus:

* JavaScript-rendered websites
* Browser automation with Playwright
* Network/API inspection
* Working with dynamically loaded content
* Database storage with PostgreSQL
* Larger scraping pipelines
* Data validation and processing
* Building reusable scraping systems

Projects:

* To be added

> This repository focuses on learning and using web scraping techniques on websites where automated access is permitted. It does not aim to bypass CAPTCHAs, authentication, access controls, or other security mechanisms.

## Repository Structure

```text
web-scraping/
│
├── README.md
├── .gitignore
│
├── books-to-scrape/
│   ├── scraper.py
│   └── venv/
│
├── quotes-to-scrape/
│   └── ...
│
└── ...
```

Generated files such as CSV/JSON exports, Python virtual environments, cache files, and compiled Python files are excluded from version control.

## Technologies

* Python
* Requests
* BeautifulSoup
* Playwright
* PostgreSQL
* Git & GitHub

Technologies will be added as the projects progress.

## Current Progress

### Completed

* [x] Basic static HTML scraping
* [x] Pagination
* [x] Following detail-page links
* [x] Data cleaning and normalization
* [x] Error handling
* [x] CSV export
* [x] JSON export

### Next Steps

* [ ] More complex static websites
* [ ] Dynamic JavaScript websites
* [ ] Browser automation
* [ ] PostgreSQL integration
* [ ] Advanced scraping projects


## Goal

Build practical web scraping skills through progressively more challenging projects, while creating a portfolio that demonstrates the ability to collect, process, and store web data using Python.
