import numpy as np
from envListen.dataOp import envdata
import random

def predict_fun(data):
    print(data)
    el = envdata()
    weight,bias = el.load_weight()  # 权重
    predict,y =fun(weight,data,bias)
    if predict==0:
        return True
    else:
        return False

def fun(weight,data, bias):
    res = 0
    y=data[-1]
    for a,b in zip(weight,data[:len(data)-1]):
        res += (a+b)
    res = sign(res+bias)
    return res , y


def sign(v):
    if v > 0:
        return 0
    else:
       return 1

def train_fun():
    el = envdata()
    weight,bias = el.load_weight()  # 权重
    print(weight)
    train_datas = el.load_data()  # 样本集
    print(train_datas)
    
    learning_rate = 0.5  # 学习速率

    train_num = 10  # 迭代次数

    for i in range(train_num):
        train = random.choice(train_datas)
        predict,y =fun(weight,train,bias)  # 输出
        if y * predict <= 0:  # 判断误分类点
            for j in range(len(weight)):
                weight[j] = weight[j] + learning_rate * y * train[j]  # 更新权重
            bias = bias + learning_rate * y  # 更新偏置量
    print(weight)
    weight.append(bias)
    el.write_weight(weight)
    return weight
