import numpy as np
import pandas as pd
import os

# 将信息写入csv表格
def write_msg(to_user_id: str, key: str, value: str):
    file_name = to_user_id + '.csv'
    if os.path.exists(file_name)!=1:
        f = open(file_name,mode='a+')
        f.write("Owner,Key,Value")
        f.close()
    data = pd.read_csv(file_name,encoding='gbk')
    data = data.values.tolist()
    for i in data:
        if i[1] == key:
            return [0,"error"]
    data.append([to_user_id,key,value])
    data = pd.core.frame.DataFrame(data)
    data.rename(columns={0:'Owner',1:'Key',2:'Value'},inplace=True)
    data.to_csv(file_name,index=None,encoding='gbk')
    return [1,"success"]

# 从csv表格中读取
def read_msg(to_user_id: str, key: str):
    file_name = to_user_id + '.csv'
    if os.path.exists(file_name)!=1:
        f = open(file_name,mode='a+')
        f.write("Owner,Key,Value")
        f.close()
    data = pd.read_csv(file_name,encoding='gbk')
    data = data.values.tolist()
    for i in data:
        if str(i[1]) == key:
            return [1,i[2]]
    return [0,"not found"]

# 处理消息函数
# to_user_id为用户名
# recived_msg为接收的消息
def handle_msg(to_user_id: str, recived_msg: str):
    name = to_user_id
    if '存' in recived_msg:
        _, key, value = recived_msg.split(" ")
        ret = write_msg(to_user_id,key,value)
        if ret[0]==0:
            return name+"您好,您的关键词已重复，请重新输入"
        else:
            return name+"您好,您的关键词"+key+"已录入"
    elif '取' in recived_msg:
        _, key = recived_msg.split(" ")
        ret, msg = read_msg(to_user_id,key)
        if ret==0:
            return name+"您好,未找到您的关键词，请重新输入"
        else:
            return name+"您好,您的关键词"+key+"的内容是：\n" + str(msg)
    else:
        return recived_msg