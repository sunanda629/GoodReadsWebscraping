# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GoodreadsItem(scrapy.Item):
	Group_Name = scrapy.Field()
	member_cnt = scrapy.Field()
	category = scrapy.Field()
	tags = scrapy.Field()
	location = scrapy.Field()
	group_type = scrapy.Field()
	avg_time_per_book = scrapy.Field()
	curr_reading_titles = scrapy.Field()
	curr_reading_authors = scrapy.Field()
	bookshelf_link = scrapy.Field()
