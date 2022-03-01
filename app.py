from flask import Flask,render_template, request, jsonify
from py2neo import Node,Relationship,Graph,NodeMatcher,RelationshipMatcher
import json,re
import torch
import torch.nn as nn
import numpy as np
import pickle
import pandas as pd
from utils.mysqlhelper import MySqLHelper
from chatbot_graph import ChatBotGraph
app = Flask(__name__)
graph = Graph('http://localhost:7474',username='neo4j',password='fengge666')
import export_poem
chatbot = ChatBotGraph()


@app.route('/')
def hello_world():
    return render_template('show_data.html')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/author/<name>',methods=['GET','POST'])
def author(name):
    return render_template('author.html',name=name)
@app.route('/tz_create_poem')
def tz_create_poem():
    return render_template('create_poem.html')
@app.route('/tz_chat_poem')
def tz_chat_poem():
    return render_template('chat_poem.html')
@app.route('/tz_look_poem_desty/<name>',methods=['GET','POST'])
def tz_look_poem_desty(name):
    return render_template('look_poem_desty.html',name=name)
@app.route('/tz_look_all_poem_desty')
def tz_look_all_poem_desty():
    return render_template('look_all_poem_desty.html')
@app.route('/tz_look_poemer_desty/<name>',methods=['GET','POST'])
def tz_look_poemer_desty(name):
    return render_template('look_poemer_desty.html', name=name)
@app.route('/tz_poem_appearance/<name>',methods=['GET','POST'])
def tz_poem_appearance(name):
    return render_template('poem_appearance.html',poem_name=name)
@app.route('/tz_find_poem/<name>',methods=['GET','POST'])
def tz_find_poem(name):
    return  render_template('find_poem.html',poem_name=name)
@app.route('/tz_find_PoemByDestyAndName/<name>',methods=['GET','POST'])
def tz_find_PoemByDestyAndName(name):
    return render_template('find_PoemByDestyAndName.html',ans=name)
@app.route('/tz_find_poemerByDestyAndName/<name>',methods=['GET','POST'])
def tz_find_poemerByDestyAndName(name):
    return render_template('find_poemerByDestyAndName.html',ans=name)


#写各朝代的诗词总数
@app.route('/desty_sum',methods=['GET','POST'])
def sum_desty():
    data = {}
    data['唐代']=48330
    data['宋代']=200000
    data['元代']=39240
    data['明代']=100000
    data['清代']=92552
    newdata=jsonify(data)
    print(jsonify(data))
    return newdata

#写各朝代的诗词总数
@app.route('/poemer_sum',methods=['GET','POST'])
def sum_poemer():
    data = {}
    data['唐代'] = 2470
    data['宋代'] = 7598
    data['元代'] = 671
    data['明代'] = 2760
    data['清代'] = 5741
    newdata=jsonify(data)
    print(jsonify(data))
    return newdata

#首页各朝代诗人简单浏览
@app.route('/poemer_produce',methods=['GET','POST'])
def poemer_produce():
    desty = request.form.get("desty")
    if desty=="0":
        desty="'唐代'"
    elif desty=="1":
        desty="'宋代'"
    elif desty=="2":
        desty="'元代'"
    elif desty=="3":
        desty="'明代'"
    elif desty=="4":
        desty="'清代'"
    data = graph.run(
        'match data=(p:desty{name:'+desty+'})-[r:`包含`]->(a:author)  return a.name,a.src,a.produce LIMIT 10000 ').data()
    data_list = []
    i = 0
    for it in data:
        name = it.get('a.name')
        src = it.get('a.src')
        produce = it.get('a.produce')
        if i < 8 and src != 'http://www.huihua8.com/uploads/allimg/20190802kkk01/1531722472-EPucovIBNQ.jpg':
            print(name + " " + src + " " + produce)
            result = {}
            result['name'] = name
            result['src'] = src
            result['produce'] = produce
            data_list.append(result)
            i = i + 1
        elif i == 8:
            break
    print(data_list)
    return json.dumps(data_list)

#作诗函数
def check7(ans):
    ans = re.split('[，。]', ans)
    if len(ans)!=5:
        return False
    for i in range(4):
        if len(ans[i])!=7:
            return False
    return True

def check5(ans):
    ans = re.split('[，。]', ans)
    print(ans)
    if len(ans)!=5:
        return False
    for i in range(4):
        if len(ans[i])!=5:
            return False
    return True

#创作诗词
@app.route('/create_poem',methods=['GET','POST'])
def create_poem():
    search_name = request.form.get("search_name")
    se_list=search_name.split(' ')
    f=False
    for it in se_list:
        if it=='7':
            f=True
    if f:
        if len(se_list[0])==4:
            ans=export_poem.qi_cang_poem(se_list[0])
            while check7(ans)==False:
                ans = export_poem.qi_cang_poem(se_list[0])
        else:
            ans=export_poem.qi_gen_poem(se_list[0])
            while check7(ans) == False:
                ans = export_poem.qi_gen_poem(se_list[0])
    else:
        if len(se_list[0])==4:
            ans=export_poem.wu_cang_poem(se_list[0])
            while check5(ans) == False:
                ans=export_poem.wu_cang_poem(se_list[0])
        else:
            ans=export_poem.wu_gen_poem(se_list[0])
            while check5(ans) == False:
                ans=export_poem.wu_gen_poem(se_list[0])
    ans_list=re.split('[，。]', ans)
    print(ans_list)
    return json.dumps(ans_list)

#创作诗词
@app.route('/look_poem_desty',methods=['GET','POST'])
def look_poem_desty():
    desty=request.form.get("desty")
    page =request.form.get("page")

    # desty="唐代"
    db = MySqLHelper()
    sql=''
    sql2=''
    sql3=''
    sum=''
    f=False
    if desty=="唐代":
        sql = "select * from tang limit "+str(page)+",16;"
        sum=48330
    elif desty=="宋代":
        sql = "select * from song limit "+str(page)+",16;"
        sum=200000
    elif desty=="元代":
        sql = "select * from yuan limit "+str(page)+",16;"
        sum=39240
    elif desty=="明代":
        sql = "select * from ming limit "+str(page)+",16;"
        sum=100000
    elif desty=="清代":
        sql = "select * from qing limit "+str(page)+",16;"
        sum=92552
    elif desty=="五言绝句":
        sql="select * from tang where formal='"+str("五言绝句")+"' limit "+str(page)+",16;"
        sql2="select count(*) from tang where formal='"+str("五言绝句")+"';"
        ret=db.selectone(sql2)
        sum=ret[0]
    elif desty=="七言绝句":
        sql="select * from tang where formal='"+str("七言绝句")+"' limit "+str(page)+",16;"
        sql2="select count(*) from tang where formal='"+str("七言绝句")+"';"
        ret=db.selectone(sql2)
        sum=ret[0]
    elif desty=="五言律诗":
        sql="select * from tang where formal='"+str("五言律诗")+"' limit "+str(page)+",16;"
        sql2="select count(*) from tang where formal='"+str("五言律诗")+"';"
        ret=db.selectone(sql2)
        sum=ret[0]
    elif desty=="七言律诗":
        sql="select * from tang where formal='"+str("七言律诗")+"' limit "+str(page)+",16;"
        sql2="select count(*) from tang where formal='"+str("七言律诗")+"';"
        ret=db.selectone(sql2)
        sum=ret[0]
    elif desty=="词":
        sql="select * from song where ci_name!='"+str("无")+"' limit "+str(page)+",16;"
        sql2="select count(*) from song where ci_name!='"+str("无")+"';"
        ret=db.selectone(sql2)
        sum=ret[0]
    elif desty=="曲":
        sql="select * from yuan where qu_name!='"+str("无")+"' limit "+str(page)+",16;"
        sql2="select count(*) from yuan where qu_name!='"+str("无")+"';"
        ret=db.selectone(sql2)
        sum=ret[0]
    else:
        f=True
        author=desty
        sql2="select desty from author where author=%s"
        ret= db.selectone(sql=sql2,param=author)
        desty=ret[0]
        if desty == "唐代":
            sql = "select * from tang where author ='"+str(author)+"' limit " + str(page) + ",16;"
            sql3 = "select count(*) from tang where author ='" + str(author) + "';"
        elif desty == "宋代":
            sql = "select * from song where author ='"+str(author)+"' limit " + str(page) + ",16;"
            sql3 = "select count(*) from song where author ='" + str(author) + "';"
        elif desty == "元代":
            sql = "select * from yuan where author ='"+str(author)+"' limit " + str(page) + ",16;"
            sql3 = "select count(*) from yuan where author ='" + str(author) + "';"
        elif desty == "明代":
            sql = "select * from ming where author ='"+str(author)+"' limit " + str(page) + ",16;"
            sql3 = "select count(*) from ming where author ='" + str(author) + "';"
        elif desty == "清代":
            sql = "select * from qing where author ='"+str(author)+"' limit " + str(page) + ",16;"
            sql3 = "select count(*) from qing where author ='" + str(author) + "';"
        ret = db.selectone(sql=sql3)
        sum=ret[0]

    jsonData = []
    ret, count = db.selectall(sql=sql)
    for row in ret:
        result = {}
        result['title'] = row[0]
        result['desty']=row[1]
        result['author'] = row[2]
        content_list=str(row[3]).replace('\n','').split('。')

        result['tag']=row[7]
        if desty=='词':
            result['formal']='词'
        elif desty=='曲':
            result['formal']='曲'
        else:
            result['formal']=row[8]
        #格式化诗句内容
        ans_content_list = []
        if (result['formal'] == '七言' or result['formal'] == '七言绝句' or result['formal'] == '七言律诗'):
            for it in content_list:
                if it != '':
                    ju_list = it.split('，')
                    if len(ju_list) != 2:
                        continue
                    ans_content_list.append(ju_list[0] + "，")
                    ans_content_list.append(ju_list[1] + "。")
            result['content'] = ans_content_list
        else:
            for it in content_list:
                if it != '':
                    it = it + "。"
                    ans_content_list.append(it)
            result['content'] = ans_content_list
        result['sum']=sum
        jsonData.append(result)
    print(json.dumps(jsonData))
    return json.dumps(jsonData)

@app.route('/look_all_poem_desty',methods=['GET','POST'])
def look_all_poem_desty():
    page = request.form.get("page")
    # desty="唐代"
    db = MySqLHelper()
    # sql = 'select count(*) from author'
    # ret=db.selectone(sql)
    sum=20088
    sql2="select * from author  limit " + str(page) + ",100;"
    jsonData = []
    ret, count = db.selectall(sql=sql2)
    for row in ret:
        result = {}
        result['author'] = row[0]
        result['desty'] = row[5]
        result['num'] = row[2]
        result['sum'] = sum
        jsonData.append(result)
    print(json.dumps(jsonData))
    return json.dumps(jsonData)

#模糊查询诗人，分页展示
@app.route('/look_poemerByDestyAndName',methods=['POST','GET'])
def look_poemerByDestyAndName():
    page = request.form.get("page")
    desty = request.form.get("desty")
    poemer_name=request.form.get("poemer_name")
    print(desty+" "+poemer_name)
    db = MySqLHelper()
    sql = "select * from author where desty='" + str(desty) + "' and author like '%"+poemer_name+"%' limit " + str(page) + ",20;"
    sql2 = "select count(*) from author where desty='" + str(desty) + "' and author like '%"+poemer_name+"%'";
    ret=db.selectone(sql2)
    sum=ret[0]
    print("诗人个数："+str(sum))
    jsonData = []
    ret, count = db.selectall(sql=sql)
    for row in ret:
        result = {}
        result['author'] = row[0]
        result['produce'] = row[1]
        result['src'] = row[4]
        result['sum'] = sum
        jsonData.append(result)
    print(json.dumps(jsonData))
    return json.dumps(jsonData)

@app.route('/look_poemer_desty',methods=['GET','POST'])
def look_poemer_desty():
    page = request.form.get("page")
    desty=request.form.get("desty")
    db = MySqLHelper()
    sql = ''
    sql2 = ''
    sum = ''
    f = False
    sql = "select * from author where desty='"+str(desty)+"' limit " + str(page) + ",20;"
    sql2="select count(*) from author where desty='"+str(desty)+"';"
    ret=db.selectone(sql2)
    sum=ret[0]
    jsonData = []
    ret, count = db.selectall(sql=sql)
    for row in ret:
        result = {}
        result['author'] = row[0]
        result['produce'] = row[1]
        result['src'] = row[4]
        result['sum'] = sum
        jsonData.append(result)
    print(json.dumps(jsonData))
    return json.dumps(jsonData)

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
    if len(ans)!=0:
        ans=",".join(ans)
        return ans
    else:
        return "无"
def common_name(name):
    data = graph.run(
        'match data=(p:author{name:'+"'"+name+"'"+'})-[r:`合称`]->(a:common_name)  return a.name').data()
    ans = []
    for it in data:
        name = it.get('a.name')
        ans.append(name)
    if len(ans)!=0:
        ans=",".join(ans)
        return ans
    else:
        return "无"

def zuopin(name):
    data = graph.run(
        'match data=(p:author{name:' + "'" + name + "'" + '})-[r:`写作`]->(a:poem)  return a.name limit 30').data()
    ans = []
    for it in data:
        name = it.get('a.name')
        ans.append(name)
    ans = ",".join(ans)
    print(ans)
    return ans

@app.route('/get_author_message',methods=['GET','POST'])
def get_author_message():
    author_name = request.form.get("author_name")
    if author_name=="":
        return False
    db=MySqLHelper()
    sql='select * from author where author=%s'
    ret=db.selectone(sql=sql,param=author_name)
    jsonData = []
    result={}
    result['author']=ret[0]
    result['desty']=ret[5]
    result['produce']=ret[1]
    result['experience']=ret[3]
    result['zi']=ret[8]
    result['hao']=ret[9]
    result['begin_time']=ret[6]
    result['end_time']=ret[7]
    result['travel_name']=travel_poem(author_name)
    result['common_name']=common_name(author_name)
    result['zuopin']=zuopin(author_name)
    jsonData.append(result)
    return json.dumps(jsonData)

@app.route('/get_famous_sentenous',methods=['GET','POST'])
def get_famous_sentenous():
    author_name = request.form.get("author_name")
    page = request.form.get("page")
    db=MySqLHelper()
    jsonData = []
    sql="select count(*) from famous_sentous where author = '"+str(author_name)+"' "
    res=db.selectone(sql)
    sum=res[0]
    print(sum)
    sql8="select * from famous_sentous where author = '"+str(author_name)+"' limit " + str(page) + ",10;"
    ret, count = db.selectall(sql=sql8)
    for row in ret:
        result = {}
        result['sent'] = row[0]
        result['author'] = row[1]
        result['poem_name'] = row[2]
        result['sum']=sum
        jsonData.append(result)
    print(json.dumps(jsonData))
    return json.dumps(jsonData)

@app.route('/poemer_things',methods=['GET','POST'])
def poemer_things():
    name=request.form.get("author_name")
    data = graph.run(
        'match data=(p:author{name:' + "'" + name + "'" + '})-[r:`事迹`]->(a:things)  return a.name,a.date,p.bg_time,p.ed_time,p.produce').data()

    bg = int(str(data[0].get('p.bg_time')).replace('年', ''))
    ed = int(str(data[0].get('p.ed_time')).replace('年', ''))
    produce=str(data[0].get('p.produce')).split('。')[0]+"。"

    dit = {}
    for i in range(len(data)):
        name = str(data[len(data) - i - 1].get('a.name'))
        date = int(re.findall(r'\d+',str(data[len(data) - i - 1].get('a.date')))[0])
        if date >= bg and date <= ed:
            if date not in dit.keys():
                dit[date] = name
            else:
                dit[date] = dit[date] + "<br>" + name
    jsonDate=[]
    jsonDate.append({'time':str(bg)+"年~"+str(ed)+"年",'things':produce})
    new_dit=sorted(dit)
    for it in new_dit:
        dict={}
        dict['time']=str(it)+"年"
        dict['things']=dit[it]
        jsonDate.append(dict)
    print(jsonDate)
    return json.dumps(jsonDate)


@app.route('/get_common_name_relation',methods=['GET','POST'])
def get_common_name_relation():
    author_name=request.form.get("author_name")
    data = graph.run(
        'match data=(p:author{name:' + "'" + author_name + "'" + '})-[r:`合称`]->(a:common_name)  return a.name,p.src').data()
    common_list = []
    author_img_src = str(data[0].get('p.src'))
    other_src = "/static/images/color_back.jpeg"
    ans_map = {}
    ans = {}
    nodes = []
    edges = []
    i = 0
    ans_map[author_name] = i
    i = i + 1
    for it in data:
        name = it.get('a.name')
        ans_map[name] = i
        common_list.append(name)
        i = i + 1
    # 加入作者节点
    dit = {}
    dit["name"] = author_name
    dit["image"] = author_img_src
    nodes.append(dit)
    for it in common_list:
        dic = {}
        dic["name"] = it
        dic["image"] = other_src
        nodes.append(dic)

    # 加入其他合称的作者节点与关系
    for it in common_list:
        data = graph.run(
            'match data=(p:common_name{name:' + "'" + it + "'" + '})-[r:`包含`]->(a:author)  return a.name,a.src').data()
        for k in data:
            qi_name = str(k.get('a.name'))
            qi_src = str(k.get('a.src'))
            if qi_name not in ans_map.keys():
                dic = {}
                dic["name"] = qi_name
                dic["image"] = qi_src
                nodes.append(dic)
                ans_map[qi_name] = i
                i = i + 1
            dic = {}
            dic["source"] = ans_map[qi_name]
            dic["target"] = ans_map[it]
            dic["relation"] = "合称"
            edges.append(dic)

    ans["nodes"] = nodes
    ans["edges"] = edges
    print(json.dumps(ans))
    return json.dumps(ans)

@app.route('/get_friend_relation',methods=['GET','POST'])
def get_friend_relation():
    author_name=request.form.get("author_name")
    data = graph.run(
        'match data=(p:author{name:' + "'" + author_name + "'" + '})-[r:`好友`]->(a:author) return p.bg_time,p.ed_time,p.src,a.name,a.src,a.bg_time,a.ed_time').data()
    if len(data)>0:
        bg_time=int(str(data[0].get('p.bg_time')).replace('年',''))
        ed_time=int(str(data[0].get('p.ed_time')).replace('年',''))
        friend_map={}
        friend_src={}
        ans = {}
        nodes = []
        edges = []
        i=0
        author_img_src=str(data[0].get('p.src'))
        friend_map[author_name]=i
        friend_src[author_name]=author_img_src
        #添加作者节点
        dit = {}
        dit["name"] = author_name
        dit["image"] = author_img_src
        nodes.append(dit)
        i=i+1
        friend_list=[]
        bg_time_list=[]
        ed_time_list=[]
        for it in data:
            name=str(it.get('a.name'))
            img_src=str(it.get('a.src'))
            a_bg_time=str(it.get('a.bg_time'))
            a_ed_time=str(it.get('a.ed_time'))
            if a_bg_time=='无' or a_ed_time=='无' or img_src=="http://www.huihua8.com/uploads/allimg/20190802kkk01/1531722472-EPucovIBNQ.jpg":
                continue
            a_bg_time=int(a_bg_time.replace('年',''))
            a_ed_time =int(a_ed_time.replace('年',''))
            if a_ed_time<bg_time or a_bg_time>ed_time:
                continue
            friend_map[name]=i
            friend_src[name]=img_src
            # 构建第一层作者关系网络
            dic = {}
            dic["name"] = name
            dic["image"] = friend_src[name]
            nodes.append(dic)

            edg_dic = {}
            edg_dic["source"] = 0
            edg_dic["target"] = friend_map[name]
            edg_dic["relation"] = "好友"
            edges.append(edg_dic)
            friend_list.append(name)
            bg_time_list.append(a_bg_time)
            ed_time_list.append(a_ed_time)
            i=i+1

        #构建第二层还有关系网
        for j in range(len(friend_list)):
            bg_time=bg_time_list[j]
            ed_time=ed_time_list[j]
            data = graph.run(
                'match data=(p:author{name:' + "'" + friend_list[j] + "'" + '})-[r:`好友`]->(a:author)  return p.bg_time,p.ed_time,p.src,a.name,a.src,a.bg_time,a.ed_time ').data()
            for kk in data:
                name=str(kk.get('a.name'))
                img_src=str(kk.get('a.src'))
                a_bg_time = str(kk.get('a.bg_time'))
                a_ed_time = str(kk.get('a.ed_time'))
                if a_bg_time == '无' or a_ed_time == '无' or img_src=="http://www.huihua8.com/uploads/allimg/20190802kkk01/1531722472-EPucovIBNQ.jpg":
                    continue
                a_bg_time = int(a_bg_time.replace('年', ''))
                a_ed_time = int(a_ed_time.replace('年', ''))
                if a_ed_time < bg_time or a_bg_time > ed_time:
                    continue
                if name not in friend_map.keys():
                    friend_map[name]=i
                    i=i+1
                    friend_src[name]=img_src
                    #添加新节点
                    dic = {}
                    dic["name"] = name
                    dic["image"] = img_src
                    nodes.append(dic)
                #添加对应的链接线
                edg_dic = {}
                edg_dic["source"] = friend_map[friend_list[j]]
                edg_dic["target"] = friend_map[name]
                edg_dic["relation"] = "好友"
                edges.append(edg_dic)
        ans["nodes"]=nodes
        ans["edges"]=edges
        print(json.dumps(ans))
        return json.dumps(ans)
    else:
        ans={}
        ans["nodes"]='无'
        return json.dumps(ans)

#前台展示：三位诗人旅行地图
@app.route('/get_where_relation_show_threePoemer',methods=['GET','POST'])
def get_where_relation_show_threePoemer():
    author_list=['李白','杜甫','白居易']
    nums=['one','two','three']
    ans={}
    address_data = pd.read_excel('static/data/gu_jin_lng_lat.xlsx')
    gu_name = list(address_data.get('gu_name'))
    kk=0
    for author_name in author_list:
        data = graph.run(
            'match data=(p:author{name:' + "'" + author_name + "'" + '})-[r:`事迹`]->(a:things) return a.date,a.name,a.where_name').data()
        date_list = []
        things_list = []
        where_list = []
        for it in data:
            date = str(it.get('a.date'))
            things = str(it.get('a.name'))
            where_name = str(it.get('a.where_name'))
            if things != '无':
                date_list.append(str(date))
                things_list.append(things)
                where_list.append(where_name)
        ans_list = []
        ans_dic = {}
        for i in range(len(date_list)):
            i = len(date_list) - i - 1
            date = date_list[i]
            things = things_list[i]
            where_name = where_list[i].split(',')
            for k in where_name:
                if k in gu_name and k not in ans_dic:
                    dit = {}
                    dit['name'] = k
                    dit['things'] = date + "," + things
                    ans_dic[k] = date + "," + things
                    ans_list.append(dit)
                    break
        new_ans_list = []
        head = ans_list[0]['name']
        small = []
        small.append({"name": head})
        small.append({"name": head, "value": 100, "things": ans_dic[head]})
        new_ans_list.append(small)
        for i in range(1, len(ans_list)):
            next = ans_list[i]['name']
            small = []
            small.append({"name": head})
            small.append({"name": next, "value": 50, "things": ans_dic[next]})
            new_ans_list.append(small)
        ans[nums[kk]]=new_ans_list
        kk=kk+1
    ans["name"]=author_list
    print(ans)
    return jsonify(ans)

@app.route('/get_where_relation',methods=['GET','POST'])
def get_where_relation():
    author_name = request.form.get("author_name")
    address_data=pd.read_excel('static/data/gu_jin_lng_lat.xlsx')
    gu_name=list(address_data.get('gu_name'))

    data = graph.run(
        'match data=(p:author{name:' + "'" + author_name + "'" + '})-[r:`事迹`]->(a:things) return a.date,a.name,a.where_name').data()
    date_list=[]
    things_list=[]
    where_list=[]

    for it in data:
        date=str(it.get('a.date'))
        things=str(it.get('a.name'))
        where_name=str(it.get('a.where_name'))
        if things!='无':
            date_list.append(str(date))
            things_list.append(things)
            where_list.append(where_name)
    ans_list=[]
    ans_dic={}
    for i in range(len(date_list)):
        i=len(date_list)-i-1
        date=date_list[i]
        things=things_list[i]
        where_name=where_list[i].split(',')
        for k in where_name:
            if k in gu_name and k not in ans_dic:
                dit={}
                dit['name']=k
                dit['things']=date+","+things
                ans_dic[k]=date+","+things
                ans_list.append(dit)
                break
    new_ans_list=[]
    head=ans_list[0]['name']
    small = []
    small.append({"name": head})
    small.append({"name":head,"value":100,"things":ans_dic[head]})
    new_ans_list.append(small)

    # nsmall = []
    # nsmall.append({"name": head})
    # nsmall.append({"name": ans_list[1]['name'], "value": 100, "things": ans_dic[ans_list[1]['name']]})
    # new_ans_list.append(nsmall)
    # for i in range(1,len(ans_list)):
    #     next=ans_list[i]['name']
    #     small=[]
    #     small.append({"name":head})
    #     small.append({"name":next,"value":100,"things":ans_dic[next]})
    #     new_ans_list.append(small)
    for i in range(0,len(ans_list)):
        if i==0:
            head=ans_list[i]['name']
            continue
        next=ans_list[i]['name']
        small = []
        small.append({"name": head})
        small.append({"name": next, "value": 100, "things": ans_dic[next]})
        new_ans_list.append(small)
        head=next
    ans_xlf={}
    ans_xlf["one"]=new_ans_list
    print(json.dumps(ans_xlf))
    return json.dumps(ans_xlf)

#诗词模糊搜索
@app.route('/get_poem_by_nameAndDesty',methods=['GET','POST'])
def get_poem_by_nameAndDesty():
    poem_name = request.form.get("poem_name")
    desty_name = request.form.get("desty_name")
    page=request.form.get("page")
    db = MySqLHelper()
    jsonData = []
    sql=''
    sql2=''
    if desty_name=='唐代':
        sql="select * from tang where title like '%" + poem_name + "%';"
        sql2="select * from tang where title like '%"+poem_name+"%' limit " + str(page) + ",16;"
    elif desty_name=='宋代':
        sql="select * from song where title like '%" + poem_name + "%';"
        sql2 = "select * from song where title like '%" + poem_name + "%' limit " + str(page) + ",16;"
    elif desty_name=='元代':
        sql="select * from yuan where title like '%" + poem_name + "%';"
        sql2 = "select * from yuan where title like '%" + poem_name + "%' limit " + str(page) + ",16;"
    elif desty_name=='明代':
        sql="select * from ming where title like '%" + poem_name + "%';"
        sql2 = "select * from ming where title like '%" + poem_name + "%' limit " + str(page) + ",16;"
    elif desty_name=='清代':
        sql="select * from qing where title like '%" + poem_name + "%';"
        sql2 = "select * from qing where title like '%" + poem_name + "%' limit " + str(page) + ",16;"
    elif desty_name=='五言绝句' or desty_name=='七言绝句' or desty_name=='五言律诗' or desty_name=='七言律诗':
        sql = "select * from song where title like '%" + poem_name + "%' and formal='"+desty_name+"';"
        sql2 = "select * from song where title like '%" + poem_name + "%' and formal='"+desty_name+"' limit " + str(page) + ",16;"
    elif desty_name=='曲':
        sql = "select * from yuan where title like '%" + poem_name + "%' and qu_name!='无';"
        sql2 = "select * from yuan where title like '%" + poem_name + "%' and qu_name!='无' limit " + str(page) + ",16;"
    elif desty_name=='词':
        sql = "select * from song where title like '%" + poem_name + "%' and ci_name!='无';"
        sql2 = "select * from song where title like '%" + poem_name + "%' and ci_name!='无' limit " + str(page) + ",16;"
    else:
        sql3="select * from author where author='"+desty_name+"'"
        ans=db.selectone(sql=sql3)
        author=str(ans[0])
        desty_name=str(ans[5])
        if desty_name == '唐代':
            sql = "select * from tang where title like '%" + poem_name + "%' and author='"+author+"';"
            sql2 = "select * from tang where title like '%" + poem_name + "%' and author='"+author+"' limit " + str(page) + ",16;"
        elif desty_name == '宋代':
            sql = "select * from song where title like '%" + poem_name + "%' and author='"+author+"';"
            sql2 = "select * from song where title like '%" + poem_name + "%' and author='"+author+"' limit " + str(page) + ",16;"
        elif desty_name == '元代':
            sql = "select * from yuan where title like '%" + poem_name + "%' and author='"+author+"';"
            sql2 = "select * from yuan where title like '%" + poem_name + "%' and author='"+author+"' limit " + str(page) + ",16;"
        elif desty_name == '明代':
            sql = "select * from ming where title like '%" + poem_name + "%' and author='"+author+"';"
            sql2 = "select * from ming where title like '%" + poem_name + "%' and author='"+author+"' limit " + str(page) + ",16;"
        elif desty_name == '清代':
            sql = "select * from qing where title like '%" + poem_name + "%' and author='"+author+"';"
            sql2 = "select * from qing where title like '%" + poem_name + "%' and author='"+author+"' limit " + str(page) + ",16;"
    ret2, count = db.selectall(sql=sql)
    sum=count
    ret,counts=db.selectall(sql=sql2)
    for row in ret:
        result = {}
        result['title'] = row[0]
        result['desty'] = row[1]
        result['author'] = row[2]
        content_list = str(row[3]).replace('\n', '').split('。')
        result['trans_content'] = str(row[4]).replace('\n', '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
        result['appear'] = str(row[5]).replace('\n', '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
        result['background'] = str(row[6]).replace('\n', '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
        result['tag'] = row[7]
        if row[8] != '无':
            result['formal'] = row[8]
        elif row[10] != '无':
            result['formal'] = '词'
        elif row[11] != '无':
            result['formal'] = '曲'
        else:
            result['formal'] = '无'
        ans_content_list = []
        if (result['formal'] == '七言' or result['formal'] == '七言绝句' or result['formal'] == '七言律诗'):
            for it in content_list:
                if it != '':
                    ju_list = it.split('，')
                    if len(ju_list) != 2:
                        continue
                    ans_content_list.append(ju_list[0] + "，")
                    ans_content_list.append(ju_list[1] + "。")
            result['content'] = ans_content_list
        else:
            for it in content_list:
                if it != '':
                    it = it + "。"
                    ans_content_list.append(it)
            result['content'] = ans_content_list
        result['sum']=sum
        jsonData.append(result)
    print(json.dumps(jsonData))
    return json.dumps(jsonData)

@app.route('/get_poem_by_name',methods=['GET','POST'])
def get_poem_by_name():
    poem_name = request.form.get("poem_name")
    db = MySqLHelper()
    desty = ['tang', 'song', 'yuan', 'ming', 'qing']
    jsonData = []
    for it in desty:
        sql = "select * from " + it + " where title like '%" + poem_name + "%';"
        ret, count = db.selectall(sql=sql)
        for row in ret:
            result = {}
            result['title'] = row[0]
            result['desty'] = row[1]
            result['author'] = row[2]
            content_list = str(row[3]).replace('\n', '').split('。')
            result['trans_content'] = str(row[4]).replace('\n', '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
            result['appear'] = str(row[5]).replace('\n', '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
            result['background'] = str(row[6]).replace('\n', '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
            result['tag'] = row[7]
            if row[8] != '无':
                result['formal'] = row[8]
            elif row[10] != '无':
                result['formal'] = '词'
            elif row[11] != '无':
                result['formal'] = '曲'
            else:
                result['formal'] = '无'
            ans_content_list = []
            if (result['formal'] == '七言' or result['formal'] == '七言绝句' or result['formal'] == '七言律诗'):
                for it in content_list:
                    if it != '':
                        ju_list = it.split('，')
                        if len(ju_list)!=2:
                            continue
                        ans_content_list.append(ju_list[0] + "，")
                        ans_content_list.append(ju_list[1] + "。")
                result['content'] = ans_content_list
            else:
                for it in content_list:
                    if it != '':
                        it = it + "。"
                        ans_content_list.append(it)
                result['content'] = ans_content_list
            jsonData.append(result)
    print(json.dumps(jsonData))
    return json.dumps(jsonData)

@app.route('/get_poem_message',methods=['GET','POST'])
def get_poem_message():
    poem_name=request.form.get("poem_name")
    db=MySqLHelper()
    desty=['tang','song','yuan','ming','qing']
    jsonData=[]
    for it in desty:
        sql = "select * from " + it + " where title = '" + poem_name + "';"
        row= db.selectone(sql=sql)
        # for row in ret:
        if row!=None:
            result = {}
            result['title'] = row[0]
            result['desty'] = row[1]
            result['author'] = row[2]
            content_list = str(row[3]).replace('\n', '').split('。')
            result['trans_content'] = str(row[4]).replace('\n', '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
            result['appear'] = str(row[5]).replace('\n', '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
            result['background'] = str(row[6]).replace('\n', '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
            result['tag'] = row[7]
            if row[8] != '无':
                result['formal'] = row[8]
            elif row[10] != '无':
                result['formal'] = '词'
            elif row[11] != '无':
                result['formal'] = '曲'
            else:
                result['formal'] = '无'
            ans_content_list = []
            if (result['formal'] == '七言' or result['formal'] == '七言绝句' or result['formal'] == '七言律诗'):
                for it in content_list:
                    if it!='':
                        ju_list = it.split('，')
                        if len(ju_list)!=2:
                            continue
                        ans_content_list.append(ju_list[0] + "，")
                        ans_content_list.append(ju_list[1]+"。")
                result['content'] = ans_content_list
            else:
                for it in content_list:
                    if it!='':
                        it=it+"。"
                        ans_content_list.append(it)
                result['content'] = ans_content_list
            jsonData.append(result)
            break
    print(json.dumps(jsonData))
    return json.dumps(jsonData)

@app.route('/get_poem_author_message',methods=['GET','POST'])
def get_poem_author_message():
    poem_name = request.form.get("poem_name")
    db = MySqLHelper()
    desty = ['tang', 'song', 'yuan', 'ming', 'qing']
    author=''
    jsonData=[]
    for it in desty:
        sql = "select * from " + it + " where title = '" + poem_name + "';"
        ret = db.selectone(sql=sql)
        if ret!=None:
            author=ret[2]
            break
    sql2="select * from author where author='"+author+"';"
    ret=db.selectone(sql=sql2)
    dic={}
    dic['author']=ret[0]
    dic['produce']=ret[1]
    dic['experience']=ret[3]
    jsonData.append(dic)
    print(json.dumps(jsonData))
    return json.dumps(jsonData)

@app.route('/get_poem_zhu',methods=['GET','POST'])
def get_poem_zhu():
    poem_name = request.form.get("poem_name")
    db = MySqLHelper()
    desty = ['tang', 'song', 'yuan', 'ming', 'qing']
    zhu=''
    jsonData=[]
    for it in desty:
        sql = "select * from " + it + " where title = '" + poem_name + "';"
        ret = db.selectone(sql=sql)
        if ret!=None:
            zhu=ret[12]
            break
    dic={}
    dic['zhu']=zhu
    jsonData.append(dic)
    print(json.dumps(jsonData))
    return json.dumps(jsonData)

#获取诗词的相关时空背景：诗词
@app.route('/get_poemtime_about_poem',methods=['GET','POST'])
def get_poemtime_about_poem():
    poem_name = request.form.get("poem_name")
    db=MySqLHelper()
    desty = ['tang', 'song', 'yuan', 'ming', 'qing']
    author=''
    bg_time=''
    for it in desty:
        sql = "select * from " + it + " where title = '" + poem_name + "';"
        ret = db.selectone(sql=sql)
        if ret!=None:
            author=ret[2]
            bg_time=str(ret[9]).replace('年','')
            break
    # print(author)
    # print(bg_time)
    date_list=[]
    back_list=[]
    poem_list=[]
    content_list=[]
    flag=False
    left=right=0
    if bg_time!='无':
        flag=True
        left=int(bg_time)-3
        right=int(bg_time)+3
    for it in desty:
        sql = "select * from " + it + " where author = '" + author + "';"
        ret,count = db.selectall(sql=sql)
        if ret!=None:
            for row in ret:
                if str(row[9])!='无' and str(row[9]).find('．')==-1 and str(row[9]).find('—')==-1 and str(row[6])!='无':
                    time=int(str(row[9]).replace('年',''))
                    if flag:
                        if time>=left and time<=right and bool(re.search(r'\d', row[6])):
                            date_list.append(time)
                            back_list.append(row[6])
                            poem_list.append(row[0])
                            content_list.append(row[3])
                    else:
                        date_list.append(time)
                        back_list.append(row[6])
                        poem_list.append(row[0])
                        content_list.append(row[3])
    jsonData=[]
    for dd in range(left,right+1):
        for i in range(len(date_list)):
            time=date_list[i]
            poem=poem_list[i]
            back=back_list[i]
            content=content_list[i].replace('\n','').split('。')
            ans_content=[]
            for it in content:
                if it!='':
                    ans_content.append(it+"。")
            if time==dd:
                dic={}
                dic['time']=str(time)+"年"
                dic['title']=poem
                dic['back']=back
                dic['content']=ans_content
                jsonData.append(dic)
    #print(json.dumps(jsonData).encode('utf-8').decode("unicode-escape"))
    return json.dumps(jsonData)

#诗词情感分析
from poem_emotion_predict import poem_emotion_predict
@app.route('/get_emotion_by_poem_name',methods=['GET','POST'])
def get_emotion_by_poem_name():
    poem_name = request.form.get("poem_name")
    db = MySqLHelper()
    desty = ['tang', 'song', 'yuan', 'ming', 'qing']
    content=''
    for it in desty:
        sql = "select * from " + it + " where title = '" + poem_name + "';"
        ret = db.selectone(sql=sql)
        if ret != None:
            content=str(ret[3]).replace('\n','')
            trans_content = str(ret[4]).replace('\n', '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
            appear = str(ret[5]).replace('\n', '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
            break
    jsonData=poem_emotion_predict(content)
    jsonData[0]['appear'] = appear
    jsonData[0]['trans_content'] = trans_content
    return json.dumps(jsonData)

#诗句情感分析
from poem_emotion_predict import poem_emotion_predict
@app.route('/get_emotion_by_ju',methods=['GET','POST'])
def get_emotion_by_ju():
    poem_name = request.form.get("poem_name")
    ju_name=request.form.get("ju_name")
    # index=int(request.form.get("index"))
    db = MySqLHelper()
    desty = ['tang', 'song', 'yuan', 'ming', 'qing']
    content=''
    appear=''
    trans_content=''
    for it in desty:
        sql = "select * from " + it + " where title = '" + poem_name + "';"
        ret = db.selectone(sql=sql)
        if ret != None:
            content=str(ret[3]).split('\n')
            trans_content=str(ret[4])
            #trans_content = str(ret[4]).replace('\n', '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
            appear = str(ret[5]).replace('\n', '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
            break
    index=0
    for i in range(len(content)):
        if content[i].find(ju_name)!=-1:
            index=i
    ans_trans='无'
    if trans_content!='无':
        trans_content=trans_content.split('。')
        ans_trans=trans_content[index].replace('\n','')+"。"
    jsonData=poem_emotion_predict(ju_name)
    jsonData[0]['appear']=appear
    jsonData[0]['trans_content']=ans_trans
    return json.dumps(jsonData)


@app.route('/send_question',methods=['GET','POST'])
def send_question():
    que=request.form.get("que")
    print(que)
    que=str(que)
    print("我的问题："+que)
    answer = chatbot.chat_main(que)
    ans={}
    ans["answer"]=answer
    print(json.dumps(ans).encode('utf-8').decode("unicode-escape"))
    return json.dumps(ans)


if __name__ == '__main__':
    app.run(debug=True)
