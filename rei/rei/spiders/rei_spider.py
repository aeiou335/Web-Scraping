import scrapy
import re
import json
import codecs
import urllib
from datetime import date

from rei.items import ProductItem

class ReiSpider(scrapy.Spider):
	name = "rei"
	allowed_domains = ["rei.com"]

	base_url = 'https://www.rei.com'
	
	
	
	def __init__(self, filters=None):

		today = date.today().isoformat()

		self.filter_set = filters

	
	def start_requests(self):
		url = 'https://www.rei.com/rest/search/results?'
		
		sport_type = ['hiking-clothing',
						  'cycling-clothing', 
						  'running-clothing', 
						  'ski-clothing', 
						  'snowboard-clothing', 
						  'travel-clothing', 
						  'yoga-clothing']
#https://www.rei.com/rest/search/results?ir=collection%3Amens-hiking-clothing&sort=sc_revenue&collection=mens-hiking-clothing&page=1&
#https://www.rei.com/rest/search/results?ir=category%3Awomens-snowboard-clothing&r=category%3Awomens-snowboard-clothing&sort=sc_revenue&page=1&
		for query in sport_type:

			data_men = {'collection': 'mens-' + query, 
					'sort' : 'sc_revenue',
                                        'origin':'web',
                                        'pagesize':'30',
					'ir': 'collection%3Amens-'+ query,
					'page': '1'}
			

			url_men = url
			for key, val in data_men.items():
				url_men = url_men + key + '=' + (val) + '&'

			#url_women = url
			#for key, val in data_women.iteritems():
			#    url_women = url_women + key + '=' + urllib.quote_plus(val) + '&'

			url_men = url_men[:-1]
			#url_women = url_women[:-1]
			
			request_men = scrapy.Request(url_men, meta={'page': 1, 'query': query},
                                            callback=self.parse_gallery, dont_filter=True)
            

			yield request_men																			
			#yield request_women

		# product_url = "https://www.rei.com/product/870162/patagonia-fjord-flannel-shirt-mens"
		# request = scrapy.Request(product_url, callback=self.parse_product, dont_filter=True)
		# yield request

	# parse gallery? it's a json
	def parse_gallery(self, response):

		data = json.loads(response.body_as_unicode())

		cur_page = response.meta['page']
		num_pages = 10
		feature_cat = response.meta['query']


		for product in data['results']:
			title = product['cleanTitle'].strip().lower()
			link = product['link'].strip()
	
			
			item = ProductItem(source_website="rei", features=[feature_cat])
			item['page'] = cur_page
			item['title'] = title
			item['brand'] = product['brand']
			item['price'] = product['displayPrice']['min']
			item['rating'] = product['rating']
			item['rating_count'] = product['reviewCount']
			item['index'] = product['index']
			item['img_url'] = product['thumbnailImageLink'] 
			temp_col = ''
			for col in range(len(product['availableColors'])):
				temp_col += product['availableColors'][col]['color']
				temp_col += ' '
			item['color'] = temp_col

			prod_request = scrapy.Request(self.base_url+link, callback=self.parse_product, dont_filter=True)
			prod_request.meta['item'] = item
			yield prod_request

		if cur_page+1 <= num_pages:
			
			next_url = re.sub('page=\d+', 'page=' + str(cur_page+1), response.url)

			request = scrapy.Request(next_url,
									 headers={'X-Requested-With': 'XMLHttpRequest',
											  'Content-Type': 'application/json; charset=UTF-8'},
									 callback=self.parse_gallery,
									 dont_filter=True)
			request.meta['page'] = cur_page+1
			request.meta['query'] = feature_cat
			yield request

	def parse_product(self, response):
		item = response.meta['item']

		if not re.search("/rei-garage/", response.url):            
			desc = response.xpath('//p[@data-ui="product-information-detail-description"]/text()').extract_first()
			if desc:
				desc = desc.strip()
			for i in range(3):
				temp = response.xpath('//table[@class="product-spec-table table"]/tbody/tr/th/text()').extract()[i].strip()
				if temp == 'Fabric':
					bullets = response.xpath('//table[@class="product-spec-table table"]/tbody/tr/td/text()').extract()[i].strip()
		else:      
			desc = response.xpath('//p[@data-ui="main-product-details-body__description"]/span/text()').extract_first()
			if desc:
				desc = desc.strip()

			bullets = response.xpath('//table[@class="tehcnical-specs__table"]/tbody/tr/th/text()').extract()

			#bullets = response.xpath("//div[@id='react-root']/div/div/div/div[1]/div/div/main/ul/li[4]/div/table/tbody/tr/td").extract()
			#//*[@id="react-root"]/div/div/div/div[1]/div/div/main/ul/li[4]/div/table/tbody/tr[2]/td
			

		#color = response.xpath('').extract()
		url = response.url

		item['descriptions'] = desc
		item['bullets'] = bullets

		item['url'] = url
		yield item
