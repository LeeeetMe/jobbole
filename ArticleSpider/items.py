# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose,TakeFirst,Join
from scrapy.loader import ItemLoader
import re,json


class ArticleItemLoader(ItemLoader):
    '''自定义输入/输出'''
    # 数据列表中的list的第一个元素
    default_output_processor = TakeFirst()

def get_Number(value):
    '''点赞、收藏、评论(数)'''
    value_match = re.match('.*?(\d+).*', value)
    if value_match:
        value = int(value_match.group(1))
    else:
        value = 0
    return value

def date_conver(value):
    value = value.replace('·', '').strip()
    return value

def return_value(value):
    return value

def content_dumps(value):
    content = json.dumps(value)
    return content

class JobboleArticlesItem(scrapy.Item):
    art_url = scrapy.Field()
    artURL_id = scrapy.Field()
    front_url = scrapy.Field(output_processor=MapCompose(return_value))
    front_img_path = scrapy.Field()
    title = scrapy.Field()
    up_count = scrapy.Field(input_processor= MapCompose(get_Number))
    collect_count = scrapy.Field(input_processor= MapCompose(get_Number))
    comment_count = scrapy.Field(input_processor= MapCompose(get_Number))
    create_date = scrapy.Field(input_processor = MapCompose(date_conver))
    category = scrapy.Field()
    tags = scrapy.Field(output_processor = Join(','))
    content = scrapy.Field()
