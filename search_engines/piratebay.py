import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from auto_cascade import *
from search_engine_base import SearchEngineBaseClass

import requests
import string
import bs4
import re


class SearchEngine(SearchEngineBaseClass):
    URL = "https://thepiratebay.org/s/"

    def search(self, query, extra_params={'video': 'on'}):
        params = {
            'q': query,
            'category': 0,
            'page': 0,
            'orderby': 99,
        }

        params.update(extra_params)

        response = requests.get(SearchEngine.URL, params)
        html = response.text
        with open(r"C:\Users\USER\Desktop\EtStuff\Temp\temp.txt", "wb") as f:
            f.write(html)
        return html

    def parse_torrent_results(self, html):
        return []

    def parse_magnet_results(self, html):
        REGEX_UPLOAD_DESCRIPTION = re.compile(r'Uploaded\s+([^\,]+)\,\s+Size\s+([^\,]+)\,\s+.+\s+by\s+([^\,]+)$')

        soup = bs4.BeautifulSoup(html, "html.parser")
        table = soup.find('table', id='searchResult')
        rows = list(r for r in table.find_all("tr") if r.get("class", ["nah"])[0].encode("utf-8") != "header")

        items = []
        for r in rows:
            title = r.find("a", class_="detLink").text
            magnet = r.find("a", title="Download this torrent using magnet").get("href")
            item = Magnet(title, magnet)

            item.seeders, item.leechers = [int(td.text) for td in r.find_all("td", align="right")]
            item.desc = r.find("font", class_="detDesc").text.encode("utf-8").replace("\xc2\xa0", " ")

            match = REGEX_UPLOAD_DESCRIPTION.search("".join(c for c in item.desc if c in string.printable))
            date, size, item.user = match.groups() if match else ("", "", "")

            items.append(item)
        return items


with open(r"C:\Users\USER\Desktop\EtStuff\Temp\temp.txt", "rb") as f:
    html = f.read()
    engine = SearchEngine()
    for item in engine.parse_magnet_results(html):
        print item.title
        print "\t", item.user
        print "\t", item.seeders, item.leechers
        print "\t", item.desc

# if __name__ == "__main__":
    # search_video("mr+robot")
