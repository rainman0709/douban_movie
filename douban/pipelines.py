# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from twisted.enterprise import adbapi
from scrapy.exceptions import DropItem

class DoubanPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb', host='localhost', db='scrapydb', user='root', passwd='root', charset='utf8',
                                                use_unicode=True)

    def process_item(self, item, spider):
        if item['movie_name']:
            query = self.dbpool.runInteraction(self.__conditional_insert,item)
            return item
        else:
            raise DropItem("Missing name, it's not good!")

    def __conditional_insert(self, tx, item):
        update = tx.execute("select 1 from scrapydb.douban_backup where address = '{0}'".format(MySQLdb.escape_string(item['address'])))
        if update:
            tx.execute("update scrapydb.douban_backup set movie_year = '{0}',address = '{1}',movie_name = '{2}',movie_describe = '{3}',score = '{4}',judge_number = '{5}' where address = '{6}'".format(MySQLdb.escape_string(item['movie_year']),MySQLdb.escape_string(item['address']),MySQLdb.escape_string(item['movie_name']),MySQLdb.escape_string(item['movie_describe']),MySQLdb.escape_string(item['score']),MySQLdb.escape_string(item['judge_number']),MySQLdb.escape_string(item['address'])))
        else:
            tx.execute("insert into scrapydb.douban_backup (movie_year,address,movie_name,movie_describe,score,judge_number) values ('{0}','{1}','{2}','{3}','{4}','{5}')".format(MySQLdb.escape_string(item['movie_year']),MySQLdb.escape_string(item['address']),MySQLdb.escape_string(item['movie_name']),MySQLdb.escape_string(item['movie_describe']),MySQLdb.escape_string(item['score']),MySQLdb.escape_string(item['judge_number'])))
