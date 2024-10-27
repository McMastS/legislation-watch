import argparse
from legislation_watch.rss_feed_parser import ParliamentOfCanadaRssFeedParser

arg_parser = argparse.ArgumentParser(description="Search the Parliament of Canada Bills RSS Feed for the given keywords")
arg_parser.add_argument("keywords", nargs="+", help="Keywords to search (case insensitive) within Canadian Parliament bills. To search for a phrase, wrap the phrase in quotes eg. 'pension fund'")
arg_parser.add_argument("--num-bills", nargs="?", type=int, help="Specify the number of bills to search through.")
args = arg_parser.parse_args()

url = "https://www.parl.ca/legisinfo/en/bills/rss"
parser = ParliamentOfCanadaRssFeedParser(url, report_path="~/Downloads/testing_report.xlsx", keywords=args.keywords, num_bills=args.num_bills)
parser.run()
