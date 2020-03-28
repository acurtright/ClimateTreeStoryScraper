import time
from datetime import datetime
import psycopg2
from googlesearch import search
from webpreview import web_preview
import warnings
import sys
import random
import json

def getNameTable():
    host="localhost"
    dbname="climateTree"
    user="postgres"
    password="700813"
    conn_str='host={0} user={1} dbname={2} password={3}'.format(host, user, dbname, password)
    conn=psycopg2.connect(conn_str)
    cur=conn.cursor()
    cur.execute('select "NAME".name,"PLACE_INFO".place_id from "NAME_PLACE" inner join "PLACE_INFO" on "NAME_PLACE".place_id = "PLACE_INFO".place_id'
    ' inner join "NAME" on "NAME".name_id = "NAME_PLACE".name_id order by "PLACE_INFO".population desc')
    return cur.fetchall()

array=[]

def getQuery(name,tup):
    return name+" climate change"
   
def writeToJson(obj,num):
    with open('../climateChange/json'+str(num)+".json","w+",encoding='utf-8') as f:
        json.dump(obj,f)

def getJson(name,tup,place_id,link):
    data={}
    data['user_id']=0
    data['hyperlink']=link
    title,desc,image=web_preview(link, timeout=1000)
    data['story_title']=title
    data['description']=desc
    data['rating']=0
    data['place_ids']=[place_id]
    data['media_type']='article'
    data['date']=datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    data['solution']=[]
    data['sector']=[]
    data['comments']=[]
    data['liked_by_users']=[]
    return data

warnings.filterwarnings("ignore")
tmp=getNameTable()
# to search
num=0
for row in tmp : #do iterate for each place
    num+=1
    print(num)
    if num>50000:
        break
    tup=[]
   
    query=getQuery(row[0],tup) #row[0] stands for the name of place
    try:
        tmpJson=[]
        for j in search(query,stop=1):
            tmpJson.append(getJson(row[0],tup,row[1],j)) #row[1] stands for the place_id
        writeToJson(tmpJson,num)
    except:
        print("ERROR",num, sys.exc_info()[0])