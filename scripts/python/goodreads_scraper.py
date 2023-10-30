import argparse
import logging
import json
import datetime

import bs4

from scripts.python.config import BASE_URL, DEFAULT_CACHE, DEFAULT_LOG_LEVEL, MAX_BOOKS
from src.utils.request_helpers import send_and_cache_request
from src.utils.scraper_classes import GoodReadsGenres, Book

LOG_LEVEL = DEFAULT_LOG_LEVEL
CACHE = DEFAULT_CACHE

DEFAULT_GENRE = GoodReadsGenres.Fantasy
GENRE = DEFAULT_GENRE

logger: logging.Logger


def main():
    global LOG_LEVEL, CACHE, GENRE
    parse_args()
    # get_books(GENRE)
    soup = get_most_read_books(GENRE)

    links = extract_links_from_most_read_soup(soup)
    urls = [f"{BASE_URL}{link}" for link in links]

    urls_cropped = urls[:MAX_BOOKS]
    books = [scrape_book(url) for url in urls_cropped]

    # write books to json file
    # add date to filename
    filename = f"{GENRE}_{datetime.datetime.now().strftime('%y-%m-%d')}_most_read.json"
    with open(filename, "w") as f:
        json.dump(books, f, default=lambda x: x.encode(), indent=4, ensure_ascii=False)


def scrape_book(url: str):
    html = send_and_cache_request(url, CACHE)
    soup = bs4.BeautifulSoup(html, "html.parser")

    title = soup.find("h1", {"class": "Text__title1"}).text.strip()
    author = soup.find("span", {"class": "ContributorLink__name"}).text.strip()
    rating = soup.find("div", {"class": "RatingStatistics__rating"}).text.strip()
    description = soup.find("span", {"class": "Formatted"}).text.strip()
    genre_list = soup.find("ul", {"aria-label": "Top genres for this book"})
    genres = [
        genre.text.strip()
        for genre in genre_list.find_all("span", {"class": "Button__labelItem"})
    ]
    # remove "...more" from genre tags
    genres = genres[:-1]

    return Book(title, author, rating, description, genres)


def extract_links_from_most_read_soup(soup: bs4.BeautifulSoup):
    content = soup.find("div", {"class": "bigBoxBody"})
    link_tags = content.find_all("a")
    links = [link_tags[i].get("href") for i in range(0, len(link_tags))]
    return links


def get_books(genre: GoodReadsGenres):
    global CACHE
    url = f"{BASE_URL}/genres/{genre}"
    html = send_and_cache_request(url, CACHE)
    soup = bs4.BeautifulSoup(html, "html.parser")
    # return books_from_soup(soup)
    # print(soup)


def get_most_read_books(genre: GoodReadsGenres):
    global CACHE
    url = f"{BASE_URL}/genres/most_read/{genre}"
    html = send_and_cache_request(url, CACHE)
    soup = bs4.BeautifulSoup(html, "html.parser")
    return soup
    # return books_from_soup(soup)
    # print(soup)


def parse_args():
    global logger, LOG_LEVEL, CACHE, GENRE

    parser = argparse.ArgumentParser(
        description="Scrape Goodreads book data",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "genre",
        help="Genre of books",
        type=GoodReadsGenres,
        choices=list(GoodReadsGenres),
    )
    parser.add_argument(
        "--cache",
        help="Cache scraped data",
        action=argparse.BooleanOptionalAction,
        default=DEFAULT_CACHE,
    )
    parser.add_argument(
        "--log",
        help="Log level",
        choices=list(logging._nameToLevel.keys()),
        default=logging.getLevelName(DEFAULT_LOG_LEVEL),
    )
    args = parser.parse_args()
    LOG_LEVEL = args.log
    CACHE = args.cache
    GENRE = args.genre
    logging.basicConfig(level=LOG_LEVEL)
    logger = logging.getLogger(__name__)


if __name__ == "__main__":
    main()
