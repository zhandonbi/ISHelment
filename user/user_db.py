from dbOperator.load_db import Load
from functools import wraps


class User(object):
    def __init__(self):
        cfgPath = './cfg/linkDB.json'
        dbOP = Load(cfgPath)
        self.cur = dbOP.cur
        self.operator = dbOP.DB_operator
        self.tableUser = 'user'

    def returnValue(self, status: bool, message):
        return {'status': status, 'message': message}

    def get_field_content(self, fields, key: str, value):
        FField = ''
        if fields is None:
            FField = '*'
        else:
            FField = ','.join(fields)
        sql = 'SELECT {} FROM {} WHERE {} = {}'.format(FField, self.tableUser,
                                                       key, value)
        self.cur.execute(sql)
        return self.cur.fetchall()

    def check_userID(self, workID):
        res = self.get_field_content(['"workID"'], 'workID', workID)
        if len(res) == 0:
            return None
        else:
            return res

    def check_userName(self, userName):
        res = self.get_field_content(['"workID"'], 'name',
                                     '"{}"'.format(userName))
        if len(res) is 0:
            return None
        else:
            return res[0][0]

    def add_user(self, userName, age, deviceID):
        if self.check_userName(userName=userName) is not None:
            return self.returnValue(False, '用户已存在')
        sql = 'INSERT INTO {} (name,age,linkNumber,workFinish,workCount)' \
              ' VALUES ("{}",{},"{}",0,0)'.format(self.tableUser, userName, age, deviceID)
        if int(age) <= 0 or deviceID is not None:
            try:
                self.cur.execute(sql)
                self.operator.commit()
                return self.returnValue(True, '新建员工 {}'.format(userName))
            except Exception as e:
                return self.returnValue(False, str(e))
        else:
            return self.returnValue(False, "数据不符合规范")

    def del_user(self, userID):
        if self.check_userID(userID) is None:
            return self.returnValue(False, '无此用户')
        else:
            sql = 'DELETE FROM {} WHERE workID = {}'.format(
                self.tableUser, userID)
            try:
                self.cur.execute(sql)
                self.operator.commit()
            except Exception as e:
                return self.returnValue(False, str(e))
            return self.returnValue(True, '已删除{}'.format(userID))

    def edit_user(self, userID, newMessage: dict):
        if self.check_userID(userID) is None:
            self.returnValue(False, '人员不存在')
        else:
            setV = ''
            for key, value in newMessage.items():
                setV += '{}={},'.format(key, value)
            sql = 'UPDATE {} SET {} WHERE workID = {}'.format()
            try:
                self.cur.execute(sql)
                return self.returnValue(True, '人员{}删除完成'.format(userID))
            except Exception as e:
                return self.returnValue(False, str(e))

    def to_dir(message):
        res = {}
        field = [
            'userID',
            'name',
            'age',
            'deviceID',
            'workFinish',
            'workCount'
        ]
        for f,v in zip(field,message):
            res[f] = v
        return res

    def find_user_by_id(self, userID):
        sql = 'SELECT * FROM {} WHERE `workID` = {}'.format(
            self.tableUser, userID)
        try:
            self.cur.execute(sql)
            res = self.cur.fetchall()
            if len(res) != 0:
                return self.returnValue(True, self.toDir(list(res[0])))
            else:
                return self.returnValue(False, '用户不存在')
        except Exception as e:
            return self.returnValue(False, str(e))

    def find_user_by_name(self, userName):
        sql = 'SELECT * FROM {} WHERE `name` = \'{}\''.format(
            self.tableUser, userName)
        try:
            self.cur.execute(sql)
            res = self.cur.fetchall()
            if len(res) != 0:
                final_res = []
                for now_line in res:
                    final_res.append(self.toDir(list(now_line)))
                return self.returnValue(True, final_res)
            else:
                return self.returnValue(False, '用户不存在')
        except Exception as e:
            return self.returnValue(False, str(e))
