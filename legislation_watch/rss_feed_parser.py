import feedparser
import requests
from bs4 import BeautifulSoup, PageElement
from urllib.parse import urljoin, urlparse

class ParsedLegislationFeed:
    pass

class ParliamentOfCanadaRssFeedParser:
    def __init__(self, rss_feed_url: str, keywords: list = []):
        self.rss_feed_url = rss_feed_url
        self.parsed_feed = None
        self.keywords = keywords

    def _get_all_bill_urls(self):
        urls = []
        if self.parsed_feed and len(self.parsed_feed.entries):
            bills = self.parsed_feed.entries
            for bill in bills:
                links = bill.get('links', [])
                if len(links) > 1:
                    print("Warning: more than one link found")
                    continue
                
                if len(links) == 0:
                    print("warning: no links found")
                    continue

                if links[0].href:
                    urls.append(links[0].href)
                else:
                    print("warning: no href found for link")
            
        return urls
        
    def run(self):
        self.parsed_feed = feedparser.parse(self.rss_feed_url)
        all_bill_urls = self._get_all_bill_urls()

        for url in all_bill_urls:
            html_page = requests.get(url).text
            bill_overview_page_soup = BeautifulSoup(html_page, "lxml")
            text_of_the_bill_spans = bill_overview_page_soup.find_all('span', string="Text of the bill")
            if len(text_of_the_bill_spans) > 1:
                print("More than two Text of the bill links found")
                continue

            if len(text_of_the_bill_spans) == 0:
                print("No text of the bill links found")
                continue
            
            base_url = "https://" + urlparse(url).netloc
            text_of_the_bill_span: PageElement = text_of_the_bill_spans[0]
            url_to_bill_document_viewer_page = urljoin(base_url, text_of_the_bill_span.find_parent().attrs.get('href'))
            document_viewer_page = requests.get(url_to_bill_document_viewer_page).text
            document_viewer_page_soup = BeautifulSoup(document_viewer_page, "lxml")
            xml_links = document_viewer_page_soup.find_all('a', string='XML')
            if len(xml_links) > 1:
                print("More than two XML links found")
                continue

            if len(xml_links) == 0:
                print("No XML links found")
                continue
            
            xml_link = xml_links[0]
            url_to_xml = urljoin(base_url, xml_link.get('href'))

            
            bill_xml_doc = requests.get(url_to_xml).text
            for keyword in self.keywords:
                if keyword in bill_xml_doc:
                    print(f"Keyword {keyword} matched: {url}")
                    
            
            


        # handle case where "the text of this bill is not available"

        