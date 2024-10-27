import pandas as pd
import feedparser
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from legislation_watch.utils import assert_list_has_exactly_one_element, find_exactly_one_element

class KeywordReportGenerator:
    def __init__(self, path: str):
        self.path = path

    def generate_report(self, keyword_url_matches: list):
        if not list:
            print("Warning: no matches given to KeywordReportGenerator")
        
        df = pd.DataFrame(keyword_url_matches)
        df.to_csv(self.path) 


class ParliamentOfCanadaRssFeedParser:
    def __init__(self, rss_feed_url: str, report_path: str, keywords: list = [], num_bills: int | None = None):
        self.rss_feed_url = rss_feed_url
        self.parsed_feed = None
        self.keywords = keywords
        self.keyword_report_generator = KeywordReportGenerator(report_path)
        self.num_bills = num_bills

    def _get_all_bill_urls(self):
        urls = []
        if self.parsed_feed and len(self.parsed_feed.entries):
            if self.num_bills:
                bills = self.parsed_feed.entries[-self.num_bills:]
            else:
                bills = self.parsed_feed.entries
            for bill in bills:
                links = bill.get('links', [])
                gt_message = "Warning: more than one link found"
                lt_message = "warning: no links found"
                if not assert_list_has_exactly_one_element(links, gt_message, lt_message):
                    continue

                if links[0].href:
                    urls.append(links[0].href)
                else:
                    print("warning: no href found for link")
            
        return urls
            
    def search_for_keywords(self, url: str, matched_keyword_urls: list[dict], text_to_search: str):
        for keyword in self.keywords:
                if keyword.lower() in text_to_search:
                    row = {
                        "bill_url": url, 
                        "keyword": keyword
                    }
                    matched_keyword_urls.append(row)

    def run(self):
        self.parsed_feed = feedparser.parse(self.rss_feed_url)
        all_bill_urls = self._get_all_bill_urls()

        matched_keyword_urls = []
        for url in all_bill_urls:
            base_url = "https://" + urlparse(url).netloc
            html_page = requests.get(url).text
            bill_overview_page_soup = BeautifulSoup(html_page, "lxml")

            text_of_the_bill_span = find_exactly_one_element(bill_overview_page_soup, 'span', "Text of the bill")
            if not text_of_the_bill_span:
                continue
            
            full_document_viewer_url = urljoin(base_url, text_of_the_bill_span.find_parent().attrs.get('href'))

            document_viewer_page = requests.get(full_document_viewer_url).text
            document_viewer_page_soup = BeautifulSoup(document_viewer_page, "lxml")

            xml_link = find_exactly_one_element(document_viewer_page_soup, 'a', 'XML')
            if not xml_link:
                continue
            full_xml_url = urljoin(base_url, xml_link.get('href'))

            bill_xml_doc = requests.get(full_xml_url).text.lower()
            self.search_for_keywords(url, matched_keyword_urls, bill_xml_doc)
            

        self.keyword_report_generator.generate_report(matched_keyword_urls)
        print(f"Report generated, found {len(matched_keyword_urls)} matches.")
        