import json
import datetime

import feedparser
from dateutil import parser as date_parser
from publications import publications
from ..config import beanstalk, articles, g
from ..scrapers import FeedScraper

class Scraper(FeedScraper):
    def __init__(self, publications):
        super(Scraper, self).__init__(publications)

    def _gen_prod_message(self, entry, publication):
        url = entry["link"]
        return {
            "url" : url,
            "scraper" : "independent_feeds",
            "publication" : publication,
            "entry" : {
                "summary" : entry.get("description", ""),
                "published" : entry["published"],
                "title" : entry["title"],
            }
        }

    def _gen_consumer_message(self, article, job):
        entry = job["entry"]
        
        data = {
            "published" : date_parser.parse(entry["published"]),
            "owner" : "Independent",
            "sub_type" : 1,
        }

        return data

scraper = Scraper(publications)
def produce():
    scraper.produce()

def consume(job):
    scraper.consume(job)
