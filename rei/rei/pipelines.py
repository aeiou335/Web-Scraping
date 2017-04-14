# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import xlwt
import scrapy
from datetime import date

class ReiPipeline(object):
	def index(table):
		for j in range(1,300):
			table.write(j,0,j)
		table.write(0,0,'Bestselling')
		table.write(0,1,'Brand')
		table.write(0,2,'Product')
		table.write(0,3,'Price')
		table.write(0,4,'Review_star')
		table.write(0,5,'Review_count')
		table.write(0,6,'Img_web')
		table.write(0,7,'Web')
		table.write(0,8,'Description')
		table.write(0,9,'Fabric')
		table.write(0,10,'Color')
		table.write(0,11,'Sports-Type')
		table.write(0,12,'Gender')
		table.write(0,13,'CreateDate')
	file = xlwt.Workbook()
	hy_table = file.add_sheet("mens-hiking-clothing",cell_overwrite_ok = True)
	index(hy_table)
	cy_table = file.add_sheet("mens-cycling-clothing",cell_overwrite_ok = True)
	index(cy_table)
	ru_table = file.add_sheet("mens-running-clothing",cell_overwrite_ok = True)
	index(ru_table)
	ski_table = file.add_sheet("mens-ski-clothing",cell_overwrite_ok = True)
	index(ski_table)
	snow_table = file.add_sheet("mens-snowboard-clothing",cell_overwrite_ok = True)
	index(snow_table)
	tra_table = file.add_sheet("mens-travel-clothing",cell_overwrite_ok = True)
	index(tra_table)
	yoga_table = file.add_sheet("mens-yoga-clothing", cell_overwrite_ok = True)
	index(yoga_table)

	

	def printing(self, table, item, spider):
		table.write(int(item['index']) + (int(item['page'])-1) * 30, 1, str(item['brand']))
		table.write(int(item['index']) + (int(item['page'])-1) * 30, 2, str(item['title']))
		table.write(int(item['index']) + (int(item['page'])-1) * 30, 3, str(item['price']))
		table.write(int(item['index']) + (int(item['page'])-1) * 30, 4, str(item['rating']))
		table.write(int(item['index']) + (int(item['page'])-1) * 30, 5, str(item['rating_count']))
		table.write(int(item['index']) + (int(item['page'])-1) * 30, 6, str(item['img_url']))
		table.write(int(item['index']) + (int(item['page'])-1) * 30, 7, str(item['url']))
		table.write(int(item['index']) + (int(item['page'])-1) * 30, 8, str(item['descriptions']))
		table.write(int(item['index']) + (int(item['page'])-1) * 30, 9, str(item['bullets']))
		table.write(int(item['index']) + (int(item['page'])-1) * 30, 10, str(item['color']))
		table.write(int(item['index']) + (int(item['page'])-1) * 30, 11, str(item['features']))
		table.write(int(item['index']) + (int(item['page'])-1) * 30, 12, 'Male')
		table.write(int(item['index']) + (int(item['page'])-1) * 30, 13, date.today().isoformat())

	def process_item(self, item, spider):
		if 'hiking' in str(item['features']):
			self.printing(self.hy_table, item, spider)
		elif 'cycling' in str(item['features']):
			self.printing(self.cy_table, item, spider)
		elif 'running' in str(item['features']):
			self.printing(self.ru_table, item, spider)
		elif 'ski' in str(item['features']):
			self.printing(self.ski_table, item, spider)
		elif 'snowboard' in str(item['features']):
			self.printing(self.snow_table, item, spider)
		elif 'travel' in str(item['features']):
			self.printing(self.tra_table, item, spider)
		else:
			self.printing(self.yoga_table, item, spider)


		self.file.save('test.xls')
		return item
	