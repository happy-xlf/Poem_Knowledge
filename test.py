import re
from utils.mysqlhelper import MySqLHelper
import json
from py2neo import Node,Relationship,Graph,NodeMatcher,RelationshipMatcher
import json,re
import torch
import torch.nn as nn
import numpy as np
import pickle
import pandas as pd
from utils.mysqlhelper import MySqLHelper
graph = Graph('http://localhost:7474',username='neo4j',password='fengge666')


def read_where():
    data=pd.read_excel('static/data/gu_jin_lng_lat.xlsx')
    gu_name=list(data.get('gu_name'))
    return gu_name

def travel_poem(name):
    gu_name=read_where()
    data = graph.run(
        'match data=(p:author{name:'+"'"+name+"'"+'})-[r:`事迹`]->(a:things)  return a.where_name,a.date,a.name').data()
    ans=[]
    for it in data:
        where_name = it.get('a.where_name')
        date = it.get('a.date')
        things_name = it.get('a.name')
        where_list=str(where_name).split(',')
        for it in where_list:
            if it in gu_name:
                ans.append(it)
                print(date+" "+things_name+" "+it)
    ans=list(set(ans))
    ans=",".join(ans)
    print(ans)
    return ans
def common_name(name):
    data = graph.run(
        'match data=(p:author{name:'+"'"+name+"'"+'})-[r:`合称`]->(a:common_name)  return a.name').data()
    ans = []
    for it in data:
        name = it.get('a.name')
        ans.append(name)
    ans=",".join(ans)
    print(ans)
    return ans

def test():
    db=MySqLHelper()
    jsonData=[]
    page=0
    author_name = "李白"
    sql2 = "select * from famous_sentous where author = '" + str(author_name) + "' limit " + str(page) + ",10;"
    ret, num = db.selectall(sql2)
    for row in ret:
        result = {}
        result['sent'] = row[0]
        result['author'] = row[1]
        result['poem_name'] = row[2]
        result['sum'] = sum
        jsonData.append(result)
    print(jsonData)


if __name__ == '__main__':
    test()