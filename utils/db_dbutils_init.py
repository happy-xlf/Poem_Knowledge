from dbutils.pooled_db import PooledDB
from . import db_config as config

"""
@功能：创建数据库连接池
"""


class MyConnectionPool(object):
    __pool = None

    def __init__(self):
        self.conn = self.__getconn()
        self.cursor = self.conn.cursor()

    # 创建数据库连接conn和游标cursor
    #def __enter__(self):
        #self.conn = self.__getconn()
        #self.cursor = self.conn.cursor()

    # 创建数据库连接池
    def __getconn(self):
        if self.__pool is None:
            self.__pool = PooledDB(
                creator=config.DB_CREATOR,
                mincached=config.DB_MIN_CACHED,
                maxcached=config.DB_MAX_CACHED,
                maxshared=config.DB_MAX_SHARED,
                maxconnections=config.DB_MAX_CONNECYIONS,
                blocking=config.DB_BLOCKING,
                maxusage=config.DB_MAX_USAGE,
                setsession=config.DB_SET_SESSION,
                host=config.DB_TEST_HOST,
                port=config.DB_TEST_PORT,
                user=config.DB_TEST_USER,
                passwd=config.DB_TEST_PASSWORD,
                db=config.DB_TEST_DBNAME,
                use_unicode=True,
                charset=config.DB_CHARSET
            )
        return self.__pool.connection()

    # 释放连接池资源
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()

    # 关闭连接归还给链接池
    def close(self):
        self.cursor.close()
        self.conn.close()

    # 从连接池中取出一个连接
    def getconn(self):
        conn = self.__getconn()
        cursor = conn.cursor()
        return cursor, conn


# 获取连接池,实例化
def get_my_connection():
    return MyConnectionPool()