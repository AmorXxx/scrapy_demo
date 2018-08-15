import pymysql


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

    # 插入数据，插入之前先查询是否存在，如果存在再查询是不是最新数据
    def insertData(self, my_dict):
        sqlExist = "SELECT * FROM detail  WHERE package_id ='%s 'AND time = '%s'" % (my_dict['package_id'], my_dict['time'])
        res = self.cursor.execute(sqlExist)
        if res :  # res为查询到的数据条数如果大于0就代表数据已经存在
            sqlRep = "SELECT * FROM detail WHERE package_id = '%s'" % (my_dict['package_id'])
            Rep = self.cursor.execute(sqlRep)
            if Rep == my_dict:  # 查询数据库内的是不是最新信息
                # 删除旧的数据
                sqlDel = "DELETE FROM  detail WHERE package_id ='%s ' AND time = '%s' AND context = '%s'" % (my_dict['package_id'], my_dict['time'],my_dict['context'])
                self.cursor.execute(sqlDel)
                # 插入新的数据
                try:
                    cols = ', '.join(my_dict.keys())  # 用，分割
                    values = '"," '.join(my_dict.values())
                    sql = "INSERT INTO amor.detail (%s) VALUES (%s)" % (cols, '"' + values + '"')
                    # 拼装后的sql如下
                    # INSERT INTO amor.detail (id，package_id,time,context) VALUES ("1"," 800933170252017
                    # 567"," 2018-08-05 13:04:03"," 客户 签收人: 已签收，签收人凭取货码签收。 已签收 感谢使用圆通速递，期待再次为您服务")
                    result = self.cursor.execute(sql)
                    insert_id = self.conn.insert_id()  # 插入成功后返回的id
                    self.conn.commit()
                    # 判断是否执行成功
                    if result:
                        print("更新数据成功，id=", insert_id)
                        return insert_id + 1

                except pymysql.Error as e:
                    print("数据库错误，原因%d: %s" % (e.args[0], e.args[1]))
            else:
                print('物流信息已更新')
        else:
            try:
                cols = ', '.join(my_dict.keys())  # 用，分割
                values = '"," '.join(my_dict.values())
                sql = "INSERT INTO detail (%s) VALUES (%s)" % (cols, '"' + values + '"')
                # 拼装后的sql如下
                # INSERT INTO amor.detail (id，package_id,time,context) VALUES ("1"," 800933170252017
                # 567"," 2018-08-05 13:04:03"," 客户 签收人: 已签收，签收人凭取货码签收。 已签收 感谢使用圆通速递，期待再次为您服务")
                result = self.cursor.execute(sql)
                insert_id = self.conn.insert_id()  # 插入成功后返回的id
                self.conn.commit()
                # 判断是否执行成功
                if result:
                    print("插入成功，id=", insert_id)
                    return insert_id + 1

            except pymysql.Error as e:
                print("数据库错误，原因%d: %s" % (e.args[0], e.args[1]))

    # 查询最后一条数据的id值
    def getLastId(self):
        sql = "SELECT max(id) FROM detail"
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
