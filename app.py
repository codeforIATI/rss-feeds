from os.path import join
import json
from urllib.parse import urlsplit, urlunsplit

import yaml
import requests
from bs4 import BeautifulSoup as bs
from dateutil.parser import parse as date_parse
from slugify import slugify


def get_base_url(url):
    split = urlsplit(url)
    return urlunsplit((split.scheme, split.netloc, '', '', ''))


def load_feed(feed):
    print("Fetching: " + feed["url"])
    r = requests.get(feed["url"])
    soup = bs(r.content, features="html.parser")
    return soup


def parse_feed(soup, feed):
    for item in soup.select(feed["item"]):
        feed_item = {}
        for feed_element, element_selector in feed["selectors"].items():
            if element_selector:
                feed_item[feed_element] = item.select_one(element_selector)
        yield feed_item


def clean_url(url, base_url):
    if url.startswith('/'):
        return base_url + url
    return url


def clean_item(item, base_url):
    cleaned_item = {}
    for k, v in item.items():
        if v is None:
            continue
        if k == "date":
            cleaned_v = date_parse(v.text, fuzzy=True).date()
        elif k == "link":
            cleaned_v = clean_url(v.get("href"), base_url)
        elif k == "illustration":
            if v.get("data-src"):
                link = v.get("data-src")
            else:
                link = v.get("src")
            cleaned_v = {
                "link": clean_url(link, base_url),
                "width": v.get("width"),
                "height": v.get("height"),
            }
        else:
            cleaned_v = v.text
        cleaned_item[k] = cleaned_v
    return cleaned_item


def write_item(item, id_):
    fname = slugify(
        "{}-{}".format(
            item["date"],
            item["headline"]),
        max_length=100) + ".md"
    fpath = join("public", "_" + id_, fname)
    with open(fpath, 'w') as f:
        f.write("---\n{}---\n".format(
            yaml.dump(item)))


if __name__ == "__main__":
    with open("feeds.json") as f:
        feeds = json.load(f)

    for feed in feeds:
        base_url = get_base_url(feed["url"])
        soup = load_feed(feed)
        for item in parse_feed(soup, feed):
            item = clean_item(item, base_url)
            write_item(item, feed["id"])
