import time
from datetime import datetime
# import psycopg2
from googlesearch import search
from webpreview import web_preview
import warnings
import sys
import random
import json
import csv
from time import sleep

def parsePlaceCSV():
    with open('similar_to_seattle_by_pop.csv', mode='r', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        result = []
        for row in reader:
            result.append([row['place'], row['id']])
    return result

def parseSolutionCSV():
    with open('strategy_sector_solution.csv', mode='r', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        result = []
        for row in reader:
            result.append([row['Strategy'], row['Sector'], row['Solution']])
    return result

def writeToJson(obj, placeid, num):
    with open('./output/' + placeid + "_" + str(num) + ".json", "w+", encoding='utf-8') as f:
        json.dump(obj, f)

def getJson(place_id, link, strategy, sector, solution):
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
    data['solution'] = [solution]
    data['sector'] = [sector]
    data['strategy'] = [strategy]
    data['comments'] = []
    data['liked_by_users'] = []
    data['flagged_by_users'] = []
    return data


warnings.filterwarnings("ignore")

places = parsePlaceCSV()
solutions = parseSolutionCSV()
num = 0
for place in places:  # do iterate for each place
    print(place, flush=True)
    placeName = place[0]
    if not placeName:
        continue
    placeid = place[1];
    for sol in solutions:
        query = placeName + " " + sol[2] #sol[2] is solution name
        try:
            for link in search(query, num=1, stop=1):
                print(link, flush=True)
                tmpJson = []
                num += 1
                try:
                    tmpJson.append(getJson(placeid, link, sol[0], sol[1], sol[2]))
                    writeToJson(tmpJson,placeid, num)
                except:
                    print("Preview Error: ", num, sys.exc_info()[0])
                sleep(3)
        except:
            print("Search Error: ", num, sys.exc_info()[0])