import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from nordea.items import Article


class NordeaSpider(scrapy.Spider):
    name = 'nordea'
    start_urls = ['https://www.nordea.com/sv/press-och-nyheter/nyheter-och-pressmeddelanden/']

    def parse(self, response):
        links = response.xpath('//h3[contains(@class, "title")]/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)


    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//small/text()').get().split()[0]
        if date:
            date = date.strip()

        content = response.xpath('//article//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
