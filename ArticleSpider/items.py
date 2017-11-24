# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JobboleArticlesItem(scrapy.Item):
    # art_url = scrapy.Field()
    # artURL_id = scrapy.Field()
    # front_url = scrapy.Field()
    # front_img_path = scrapy.Field()
    title = scrapy.Field()
    # up_count = scrapy.Field()
    # collect_count = scrapy.Field()
    # comment_count = scrapy.Field()
    # create_date = scrapy.Field()
    # category = scrapy.Field()
    # tags = scrapy.Field()
    # content = scrapy.Field()
