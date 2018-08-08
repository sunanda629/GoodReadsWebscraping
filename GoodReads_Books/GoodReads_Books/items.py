# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GoodreadsBooksItem(scrapy.Item):
	title = scrapy.Field()
	author = scrapy.Field()
	rating = scrapy.Field()
	num_ratings = scrapy.Field()
	num_pages = scrapy.Field()
	year_published = scrapy.Field()
	url = scrapy.Field()
	pass
