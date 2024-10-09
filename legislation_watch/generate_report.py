from legislation_watch.rss_feed_parser import ParliamentOfCanadaRssFeedParser

url = "https://www.parl.ca/legisinfo/en/bills/rss"
parser = ParliamentOfCanadaRssFeedParser(url, keywords=['Investment restrictions', 'Pension Fund'])
parser.run()
