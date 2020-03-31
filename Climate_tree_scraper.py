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
from time import sleep

def parsePlaceCSV():
    print('parsing csv')
    with open('seattle_name_id.csv', mode='r', encoding='utf8') as csvfile:
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


warnings.filterwarnings("ignore")

tmp = parsePlaceCSV()
num = 0
print("starting loop")
for row in tmp:  # do iterate for each place
    print(row, flush=True)
    placeName = row[0]
    if not placeName:
        continue
    query = getQuery(placeName)
    try:
        for link in search(query, num=10, stop=10):
            print(link, flush=True)
            tmpJson = []
            num += 1
            try:
                tmpJson.append(getJson(row[1], link))  # row[1] stands for the place_id
                writeToJson(tmpJson, num)
            except:
                print("Preview Error: ", num, sys.exc_info()[0])
            sleep(3)
    except:
        print("Search Error: ", num, sys.exc_info()[0])