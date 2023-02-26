import scrapy
from scrapy import Field


class CodeItem(scrapy.Item):
    code_number = Field()
    file_infos = Field()
    file_urls = Field()


class FileItem(scrapy.Item):
    file_title = Field()
    file_names = Field()
