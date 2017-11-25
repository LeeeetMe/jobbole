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
        print('Item===',item,'item=====]]]')

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


from twisted.enterprise import adbapi


class MysqlTwistedPipeline(object):
    '''
    异步机制将数据写入到mysql数据库中
    '''

    # 创建初始化函数，当通过此类创建对象时首先被调用的方法
    def __init__(self, dbpool):
        self.dbpool = dbpool

    # 创建一个静态方法,静态方法的加载内存优先级高于init方法，java的static方法类似，
    # 在创建这个类的对之前就已将加载到了内存中，所以init这个方法可以调用这个方法产生的对象
    @classmethod
    # 名称固定的
    def from_settings(cls, settings):
        # 先将setting中连接数据库所需内容取出，构造一个地点
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset="utf-8",
            # 游标设置
            cursorclass= MySQLdb.cursors.DictCursor,
            # 设置编码是否使用Unicode
            use_unicode=True
        )
        # 通过Twisted框架提供的容器连接数据库,MySQLdb是数据库模块名
        dbpool = adbapi.ConnectionPool("MySQLdb", dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用Twisted异步的将Item数据插入数据库
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 这里不往下传入item,spider，handle_error则不需接受,item,spider)

    def do_insert(self, cursor, item):
        # 执行具体的插入语句,不需要commit操作,Twisted会自动进行
        insert_sql = """
             insert into articles(title) VALUES(%s)
        """
        cursor.execute(insert_sql, (item["title"]))

    def handle_error(self, failure, item, spider):
        # 出来异步插入异常
        print(failure)

class JobBoleImagePipelines(ImagesPipeline):

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok,x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['front_img_path'] = image_paths
        return item
