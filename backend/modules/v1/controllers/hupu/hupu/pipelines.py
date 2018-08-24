# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
import pymysql


class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['img_src']:
            yield Request(image_url)

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise DropItem('Item contains no images')
        item['img_path'] = image_path
        mysqlCommand = MySQLCommand()
        mysqlCommand.connectMysql()
        # 这里每次查询数据库中最后一条数据的id，新加的数据每成功插入一条id+1
        dataCount = int(mysqlCommand.getLastId()) + 1
        for path in image_path:
            my_dic = dict(id=str(dataCount), img_path=str(path))  # 组建字典
            try:
                # 插入数据，如果已经存在就进行更新
                res = mysqlCommand.insertData(my_dic)  # 插入字典
                if res:
                    dataCount = res
            except Exception as e:
                print("插入数据失败", str(e))  # 输出插入失败的报错语句
        mysqlCommand.closeMysql()
        return item


class MySQLCommand(object):
    def __init__(self):
        self.host = 'localhost'
        self.port = 3306  # 端口号
        self.user = 'root'  # 用户名
        self.password = ""  # 密码
        self.db = "amor"  # 库

    # 链接数据库
    def connectMysql(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                                        passwd=self.password, db=self.db, charset='utf8')
            self.cursor = self.conn.cursor()
        except:
            print('connect mysql error.')

    # 插入数据
    def insertData(self, my_dict):

        # 插入新的数据
        try:
            cols = ', '.join(my_dict.keys())  # 用，分割
            values = '"," '.join(my_dict.values())
            sql = "INSERT INTO amor.hupu (%s) VALUES (%s)" % (cols, '"' + values + '"')
            result = self.cursor.execute(sql)
            insert_id = self.conn.insert_id()  # 插入成功后返回的id
            self.conn.commit()
            # 判断是否执行成功
            if result:
                print("更新数据成功，id=", insert_id)
                return insert_id + 1

        except pymysql.Error as e:
            print("数据库错误，原因%d: %s" % (e.args[0], e.args[1]))

    # 查询最后一条数据的id值
    def getLastId(self):
        sql = "SELECT max(id) FROM hupu"
        try:
            self.cursor.execute(sql)
            row = self.cursor.fetchone()  # 获取查询到的第一条数据
            if row[0]:
                return row[0]  # 返回最后一条数据的id
            else:
                return 0  # 如果表格为空就返回0
        except:
            print(sql + ' execute failed.')

    def closeMysql(self):  # 关闭数据库
        self.cursor.close()
        self.conn.close()
