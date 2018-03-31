# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class HexunpjtPipeline(object):
    def __init__(self):
        # 连接对应数据库
        self.conn = pymysql.connect(host="127.0.0.1", user="root", passwd="root", db="hexun")
        self.conn.set_charset("utf8")
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        # 处理博文列表页中各博文信息
        for j in range(0, len(item["name"])):
            # 将获取到的name,url,hits,comment分别赋给各变量
            name = item["name"][j]
            url = item["url"][j]
            hits = item["hits"][j]
            comment = item["comment"][j]
            # 构造对应的sql语句，实现将获取到的数据插入数据库中
            sql = "insert into myhexun(name,url,hits,comment) VALUES('"+name+"','"+url+"','"+hits+"','"+comment+"')"
            # 通过query事先执行对应的sql语句
            # print(sql)
            # print('sql')
            # self.conn.query(sql)
            self.cursor.execute(sql)
            self.conn.commit()
        return item
    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()
        # print('over')

