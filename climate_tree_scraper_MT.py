from joblib import Parallel, delayed
import time
from datetime import datetime
import psycopg2
from googlesearch import search
from webpreview import web_preview
import warnings
import sys
import random
import json
import csv


def parsePlaceCSV():
    with open('place_name_id.csv', mode='r', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        result = []
        for row in reader:
            result.append([row['place'], row['id']])
    return result

def getQuery(name):
    return name + " climate change"

def writeToJson(obj, num):
    with open('./output/' + str(num) + ".json", "w+", encoding='utf-8') as f:
        json.dump(obj, f)

def getJson(place_id, link):
    data = {}
    data['user_id'] = 0
    data['hyperlink'] = link
    title, desc, image = web_preview(link, timeout=1000)
    data['story_title'] = title
    data['description'] = desc
    data['rating'] = 0
    data['place_ids'] = [place_id]
    data['media_type'] = 'article'
    data['date'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    data['solution'] = []
    data['sector'] = []
    data['comments'] = []
    data['liked_by_users'] = []
    return data

def lookupStory(row, num):
    print(row, flush=True)
    placeName = row[0]
    if not placeName:
        return
    query = getQuery(placeName)
    try:
        tmpJson = []
        for link in search(query, stop=1):
            tmpJson.append(getJson(row[1], link))  # row[1] stands for the place_id
        writeToJson(tmpJson, num)
    except:
        print("ERROR", num, sys.exc_info()[0])

warnings.filterwarnings("ignore")

tmp = parsePlaceCSV()
print("starting loop")
Parallel(n_jobs=8)(delayed(lookupStory)(tmp[i], i) for i in range(len(tmp)))

