from .db_dbutils_init import get_my_connection

"""执行语句查询有结果返回结果没有返回0；增/删/改返回变更数据条数，没有返回0"""


class MySqLHelper(object):
    def __init__(self):
        self.db = get_my_connection()  # 从数据池中获取连接

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'inst'):  # 单例
            cls.inst = super(MySqLHelper, cls).__new__(cls, *args, **kwargs)
        return cls.inst

    # 封装执行命令
    def execute(self, sql, param=None, autoclose=False):
        """
        【主要判断是否有参数和是否执行完就释放连接】
        :param sql: 字符串类型，sql语句
        :param param: sql语句中要替换的参数"select %s from tab where id=%s" 其中的%s就是参数
        :param autoclose: 是否关闭连接
        :return: 返回连接conn和游标cursor
        """
        cursor, conn = self.db.getconn()  # 从连接池获取连接
        count = 0
        try:
            # count : 为改变的数据条数
            if param:
                count = cursor.execute(sql, param)
            else:
                count = cursor.execute(sql)
            conn.commit()
            if autoclose:
                self.close(cursor, conn)
        except Exception as e:
            pass
        return cursor, conn, count

    # 执行多条命令
    # def executemany(self, lis):
    #     """
    #     :param lis: 是一个列表，里面放的是每个sql的字典'[{"sql":"xxx","param":"xx"}....]'
    #     :return:
    #     """
    #     cursor, conn = self.db.getconn()
    #     try:
    #         for order in lis:
    #             sql = order['sql']
    #             param = order['param']
    #             if param:
    #                 cursor.execute(sql, param)
    #             else:
    #                 cursor.execute(sql)
    #         conn.commit()
    #         self.close(cursor, conn)
    #         return True
    #     except Exception as e:
    #         print(e)
    #         conn.rollback()
    #         self.close(cursor, conn)
    #         return False

    # 释放连接
    def close(self, cursor, conn):
        """释放连接归还给连接池"""
        cursor.close()
        conn.close()

    # 查询所有
    def selectall(self, sql, param=None):
        try:
            cursor, conn, count = self.execute(sql, param)
            res = cursor.fetchall()
            return res,count
        except Exception as e:
            print(e)
            self.close(cursor, conn)
            return count

    # 查询单条
    def selectone(self, sql, param=None):
        try:
            cursor, conn, count = self.execute(sql, param)
            res = cursor.fetchone()
            self.close(cursor, conn)
            return res
        except Exception as e:
            print("error_msg:", e.args)
            self.close(cursor, conn)
            return count

    # 增加
    def insertone(self, sql, param):
        try:
            cursor, conn, count = self.execute(sql, param)
            # _id = cursor.lastrowid()  # 获取当前插入数据的主键id，该id应该为自动生成为好
            conn.commit()
            self.close(cursor, conn)
            return count
            # 防止表中没有id返回0
            # if _id == 0:
            #     return True
            # return _id
        except Exception as e:
            print(e)
            conn.rollback()
            self.close(cursor, conn)
            return count

    # 增加多行
    def insertmany(self, sql, param):
        """
        :param sql:
        :param param: 必须是元组或列表[(),()]或（（），（））
        :return:
        """
        cursor, conn, count = self.db.getconn()
        try:
            cursor.executemany(sql, param)
            conn.commit()
            return count
        except Exception as e:
            print(e)
            conn.rollback()
            self.close(cursor, conn)
            return count

    # 删除
    def delete(self, sql, param=None):
        try:
            cursor, conn, count = self.execute(sql, param)
            self.close(cursor, conn)
            return count
        except Exception as e:
            print(e)
            conn.rollback()
            self.close(cursor, conn)
            return count

    # 更新
    def update(self, sql, param=None):
        try:
            cursor, conn, count = self.execute(sql, param)
            conn.commit()
            self.close(cursor, conn)
            return count
        except Exception as e:
            print(e)
            conn.rollback()
            self.close(cursor, conn)
            return count


if __name__ == '__main__':
    db = MySqLHelper()
    # 调用方法的时候，第一个参数为sql语句，第二个为你传递的参数，单个参数直接给值或者变量，多个参数用元组即可，可以参考下面的例子
    # 需要注意的是 返回值的类型 写完语句记得查看返回值类型，避免使用出错
    #
    # 查询单条 ret为查询结果
    # username = "xp"
    # password = "123456"
    # sql = "select * from user where account=%s and password = %s"
    # ret = db.selectone(sql,(username,password))
    # print(ret)
    # 查询多条  ret为返回的数据库结果，count为数目
    # sql = "select * from project where account = %s"
    # ret, count = db.selectall(sql=sql, param="sjztddx")
    # for row in ret:
    #     print(row)
    # print(count)
    # 增加单条 ret为修改的条数，正常情况一般为1
    # sql2 = 'insert into user (account,password) VALUES (%s,%s)'
    # ret = db.insertone(sql2, ('old3', '22222'))
    # print(ret)
    # 增加多条 ret返回值为改变的数据条数
    # sql3 = 'insert into userinfo (name,password) VALUES (%s,%s)'
    # li = li = [
    #     ('分省', '123'),
    #     ('到达','456')
    # ]
    # ret = db.insertmany(sql3,li)
    # print(ret)
    # 删除  ret返回值为改变的数据条数
    # sql4 = 'delete from  userinfo WHERE name=%s'
    # args = 'xxxx'
    # ret = db.delete(sql4, args)
    # print(ret)
    # 更新 ret为改变的数据条数
    # sql5 = r'update userinfo set password=%s WHERE name LIKE %s'
    # args = ('993333993', '%old%')
    # ret = db.update(sql5, args)
    # print(ret)
