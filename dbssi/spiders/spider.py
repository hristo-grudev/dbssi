import scrapy

from scrapy.loader import ItemLoader

from ..items import DbssiItem
from itemloaders.processors import TakeFirst


class DbssiSpider(scrapy.Spider):
	name = 'dbssi'
	start_urls = ['https://www.dbs.si/info-portal']

	def parse(self, response):
		post_links = response.xpath('//a[@class="more"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@rel="next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//section[@id="content"]//text()[normalize-space() and not(ancestor::h1 | ancestor::p[@class="subtitle"])]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//p[@class="subtitle"]/text()').get()

		item = ItemLoader(item=DbssiItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
