import sys
import os
MAIN_DIRECTORY = os.path.dirname(os.path.dirname(__file__)) or ".."
sys.path.append(MAIN_DIRECTORY)
from auto_cascade import *
from search_engine_base import SearchEngineBaseClass

import requests
import urllib
import string
import bs4
import re


class SearchEngine(SearchEngineBaseClass):
    URL = "https://thepiratebay.org/s/"

    def search(self, query, extra_params={'video': 'on'}):
        params = {
            'q': urllib.quote_plus(query),
            'category': 0,
            'page': 0,
            'orderby': 99,
        }

        params.update(extra_params)

        response = requests.get(SearchEngine.URL, params)
        result = response.text
        return result

    def parse_torrent_results(self, html):
        return []

    def parse_magnet_results(self, html):
        REGEX_UPLOAD_DESCRIPTION = re.compile(r'Uploaded\s+([^\,]+)\,\s+Size\s+([^\,]+)\,\s+.+\s+by\s+([^\,]+)$')

        soup = bs4.BeautifulSoup(html, "html.parser")
        table = soup.find('table', id='searchResult')

        if not table:
            raise Exception("Error querying %s" % self.URL)

        rows = list(r for r in table.find_all("tr") if r.get("class", ["nah"])[0].encode("utf-8") != "header")

        items = []
        for r in rows:
            title = r.find("a", class_="detLink").text
            link = r.find("a", title="Download this torrent using magnet").get("href")
            item = Magnet(title, link)

            item.seeders, item.leechers = [int(td.text) for td in r.find_all("td", align="right")]
            item.desc = r.find("font", class_="detDesc").text.encode("utf-8").replace("\xc2\xa0", " ")

            match = REGEX_UPLOAD_DESCRIPTION.search("".join(c for c in item.desc if c in string.printable))
            upload_date, size, item.uploader = match.groups() if match else ("", "", "")

            item.upload_date = parse_date_string(upload_date)
            item.size = parse_size_string(size)

            items.append(item)
        return items


if __name__ == "__main__":
    TEST_FILE = os.path.join(MAIN_DIRECTORY, "temp", "temp.txt")
    engine = SearchEngine()

    # with open(TEST_FILE, "wb") as f:
    #     result = engine.search("mr robot")
    #     f.write(result)

    with open(TEST_FILE, "rb") as f:
        html = f.read()
        for item in engine.parse_magnet_results(html):
            print item.title
            print "\t", item.uploader
            print "\t", item.seeders, item.leechers
            print "\t", item.upload_date, item.size
            print "\t", item.desc


