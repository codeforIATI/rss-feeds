import re
from datetime import date
from os.path import join
from os import environ
import json
from urllib.parse import urlsplit, urlunsplit

import yaml
import requests
from bs4 import BeautifulSoup as bs
import parsedatetime
from slugify import slugify


def get_base_url(url):
    split = urlsplit(url)
    return urlunsplit((split.scheme, split.netloc, '', '', ''))


def authenticate(session, auth):
    for k, v in auth["data"].items():
        match = re.match(r'\{\{ ([^ ]+) \}\}', v)
        if match:
            auth["data"][k] = environ.get(match.group(1))
    print("Authenticating: " + auth["url"])
    session.post(auth["url"], data=auth["data"])
    return session


def load_feed(feed):
    session = requests.Session()
    if feed.get("auth"):
        session = authenticate(session, feed["auth"])
    print("Fetching: " + feed["url"])
    r = session.get(feed["url"])
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
            cal = parsedatetime.Calendar()
            cleaned_v = date(*cal.parse(v.text)[0][:3])
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


def write_item(item, feed_id):
    item_date = item.get("date", date.today())
    fname = slugify(
        "{}-{}".format(
            item_date,
            item["headline"]),
        max_length=100) + ".md"
    fpath = join("public", "_" + feed_id, fname)
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
