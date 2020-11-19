from dbOperator.load_db import Load
from functools import wraps


class envdata(object):
    def __init__(self):
        self.cfgPath = './cfg/linkDB.json'
        self.dbOP = Load(self.cfgPath)
        self.cur = self.dbOP.cur
        self.operator = self.dbOP.DB_operator
        self.table = 'env'
        self.tableModle = 'weight'

    def returnValue(self, status: bool, message):
        return {'status': status, 'message': message}

    def set_danger(self, id):
        sql = 'UPDATE {} SET `OR_SAFE` = {} WHERE `ID`= "{}"'.format(
            self.table, 0, id)
        try:
            self.cur.execute(sql)
            self.operator.commit()
            return self.returnValue(True, 'edit ok')
        except Exception as e:
            return self.returnValue(False, str(e))

    def add_data(self, list_data):
        str_data = ','.join([str(i) for i in list_data[1:]])
        sql = 'INSERT INTO {}' \
              ' VALUES ("{}",{},{})'.format(self.table,  list_data[0],str_data,1)
        try:
            self.cur.execute(sql)
            self.operator.commit()
            return self.returnValue(True, 'add ok')
        except Exception as e:
            return self.returnValue(False, str(e))

    def load_weight(self):
        sql = 'SELECT * FROM {}'.format(
            self.tableModle)
        try:
            self.cur.execute(sql)
            res = self.cur.fetchall()
            data = res[len(res)-1][1:]
            bias = data[-1]
            return list(data)[:len(data) - 1], bias
        except Exception as e:
            print(str(e))
            return self.returnValue(False, str(e))

    def write_weight(self,data):
        str_data = ','.join([str(x) for x in data])
        sql = 'INSERT INTO {} (`TEMP`,`HUMI`,`YW`,`JSD_X`,`JSD_Z`,`POS_HIGH`,`BIAS`) VALUES ({})'\
            .format(self.tableModle,str_data)
        try:
            self.cur.execute(sql)
            self.operator.commit()
        except Exception as e:
            print(str(e))
            return self.returnValue(False, str(e))

    def load_data(self):
        sql_0 = 'SELECT * FROM {} WHERE `OR_SAFE`= 0'.format(self.table)
        sql_1 = 'SELECT * FROM {} WHERE `OR_SAFE`= 1'.format(self.table)
        try:
            self.cur.execute(sql_0)
            res_0 = self.cur.fetchall()
            self.cur.execute(sql_1)
            res_1 = self.cur.fetchall()
            RES = []
            for now in res_0 + res_1:
                RES.append(now[1:])
            return RES
        except Exception as e:
            return self.returnValue(False, str(e))

    def reLink(self):
        self.dbOP = Load(self.cfgPath)