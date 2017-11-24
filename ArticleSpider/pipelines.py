# -*- coding: utf-8 -*-


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from scrapy.exceptions import DropItem
import json
import codecs
import MySQLdb
from ArticleSpider.utls.sql_orm import Interface

from twisted.enterprise import adbapi
class JsonWithEncodingPipeline(object):
    # 使用自定义Json文件保存数据
    def __init__(self):
        self.file = codecs.open('article.json','w',encoding='utf-8')

    def open_spider(self,spider):
        pass
    def close_spider(self,spider):
        print('Close')
        self.file.close()

    def process_item(self, item, spider):
        print('Json---------------------Write')
        line = json.dumps(dict(item),ensure_ascii=False) + '\n'
        self.file.write(line)
        return item

class JsonExporterPipeline():
    # 使用FeedJsonItenExporter保存数据
    def __init__(self):
        self.file = open('articleExporter.json','wb')
        self.exporter = JsonItemExporter(self.file,ensure_ascii =False,encoding='utf-8')
        self.exporter.start_exporting()

    def process_item(self,item,spider):
        print('Write')
        self.exporter.export_item(item)
        return item

    def close_spider(self,spider):
        print('Close')
        self.exporter.finish_exporting()
        self.file.close()

class MySQLPipeline():
    # 同步将数据写入mysql
    def __init__(self):
        self.interface = Interface()

    def process_item(self,item,spider):
        self.interface.add_data(dict(item))
        return item

class Asyn_MySQLPipeline():
    # MySQL异步保存数据
    def __init__(self,pool):
        self.pool = pool

    @classmethod
    def connect_mysql(cls):
        pass
class JobBoleImagePipelines(ImagesPipeline):

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok,x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['front_img_path'] = image_paths
        return item
