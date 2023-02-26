import scrapy
from scrapy import FormRequest

from ..items import CodeItem, FileItem


class CodeSpider(scrapy.Spider):
    name = "codes"
    BASE_URL = 'https://simpleenergy.com.br/teste/'
    start_urls = [BASE_URL]

    def __init__(self, code_number, *args, **kwargs):
        super(CodeSpider, self).__init__(*args, **kwargs)
        self.code_number = code_number

    def parse(self, response, **kwargs):
        form_data = {'codigo': self.code_number}
        return FormRequest.from_response(response,
                                         formdata=form_data,
                                         callback=self.fetch_code_infos)

    def fetch_code_infos(self, response):
        code_info = CodeItem()
        body = response.xpath('//body')

        code_info['code_number'] = body.xpath('div[1]/text()').get() \
            .strip()

        file_infos = []
        file_urls_all = []
        for div in body.xpath('div')[1:]:
            file_item = FileItem()
            file_item['file_title'] = div.xpath('div[1]/text()') \
                .get().strip()
            file_names = []
            for subdiv in div.xpath('div')[1:]:
                file_url = f"{self.BASE_URL}" \
                           f"{subdiv.xpath('a/@href').get()}"
                file_urls_all.append(file_url)
                file_names.append(file_url.split('/')[-1])
            file_item['file_names'] = file_names
            file_infos.append(file_item)

        code_info['file_urls'] = file_urls_all
        code_info['file_infos'] = file_infos
        yield code_info
