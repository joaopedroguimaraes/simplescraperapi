import hashlib
import mimetypes
from pathlib import PurePosixPath, Path
from urllib.parse import urlparse, to_bytes

import pymongo
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline


class S3FilesPipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None, *,
                  item=None):
        # print('===============================')
        code_number = item['code_number']
        media_guid = ''.join(Path(request.url).name.split('.')[:-1])
        media_ext = Path(request.url).suffix
        if media_ext not in mimetypes.types_map:
            media_ext = ""
            media_type = mimetypes.guess_type(request.url)[0]
            if media_type:
                media_ext = mimetypes.guess_extension(media_type)
        return f"/{code_number}/{media_guid}{media_ext}"


class MongoPipeline:
    collection_name = 'codes'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        item_dict = ItemAdapter(item).asdict()
        item_dict.pop('file_urls')
        self.db[self.collection_name].insert_one(item_dict)
        return item
