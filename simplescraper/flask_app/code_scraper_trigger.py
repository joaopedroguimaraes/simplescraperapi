import os
import sys
import time

import crochet
from scrapy.crawler import CrawlerRunner

from scrapy import signals
from scrapy.signalmanager import dispatcher
from scrapy.utils.project import get_project_settings

from .database import Database
# from ..simplescraper.spiders.code_spider import CodeSpider

crochet.setup()
RUNNER = CrawlerRunner(get_project_settings())


class CodeScraperTrigger:

    def __init__(self):
        self.scrape_complete = False
        self.number_of_items = 1
        self.database = Database()
        path_to_scrapy_project = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), 'simplescraper')
        sys.path.append(path_to_scrapy_project)

    def parse_data(self, code_number):
        self.__scrape_with_crochet(code_number=code_number)
        while self.scrape_complete is False:
            time.sleep(5)
        return self.database.find_one(code_number)

    def __crawler_result(self, item):
        pass

    @crochet.run_in_reactor
    def __scrape_with_crochet(self, code_number):
        dispatcher.connect(self.__crawler_result,
                           signal=signals.item_scraped)
        eventual = RUNNER.crawl('codes', code_number=code_number)
        eventual.addCallback(self.__finished_scrape)
        return eventual

    def __finished_scrape(self, *args, **kwargs):
        self.scrape_complete = True
