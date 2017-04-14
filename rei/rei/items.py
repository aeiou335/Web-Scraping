# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
	# raw data
	title = scrapy.Field() # title might need to be derived if want to remove brand name in beginning of name
	brand = scrapy.Field()
	rank = scrapy.Field()
	descriptions = scrapy.Field()
	bullets = scrapy.Field()
	color = scrapy.Field()
	price = scrapy.Field()
	rating = scrapy.Field()
	rating_count = scrapy.Field()
	style_number = scrapy.Field()
	url = scrapy.Field()
	img_url = scrapy.Field()
	index = scrapy.Field()
	style = scrapy.Field()					
	page = scrapy.Field()
	fabric = scrapy.Field()
	# derived data or raw (depending if site provides)
	clothing_type = scrapy.Field()
	materials = scrapy.Field()
	features = scrapy.Field()
	

	# DB informations:
	dbname = scrapy.Field()
	source_website = scrapy.Field()
	# search methods include: all -> no keyword (dick's, ), brand (only for amazon and dick), 
	# feature (for all website except those without features defined by website), search bar (amazon only) 
	#search_method = scrapy.Field()
	keyword = scrapy.Field()
