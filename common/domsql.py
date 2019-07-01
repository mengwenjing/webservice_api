import pymysql
from common.read_config import config

class DoMysql:

    def __init__(self):
        host = config.get_str('db','host')
        port = config.get_int('db','port')
        user = config.get_str('db','user')
        pwd = config.get_str('db','pwd')
        self.mysql = pymysql.connect(host=host, port=port, user=user, password=pwd)
        self.cursor = self.mysql.cursor(pymysql.cursors.DictCursor)#返回的数据类型是字典

    def fetch_one(self,sql):
        self.cursor.execute(sql)
        self.mysql.commit()
        return self.cursor.fetchone()#返回查询结果集里面最近的一条数据

    def fetch_all(self,sql):
        self.cursor.execute(sql)
        self.mysql.commit()
        return self.cursor.fetchall()#返回全部结果

    def close(self):
        self.cursor.close()
        self.mysql.close()

