import time
import pymongo
import requests
import config

connection = pymongo.MongoClient("my_mongodb")
db = connection.news_snippets_new




while True:
    response = requests.get('http://api.zeit.de/content?q=Klimawandel&limit=50', headers={'X-Authorization': config.KEY})

    data = response.json() #store data as json

    for i in range(50):
        snippet = data['matches'][i]['snippet']
        doc = {'snippet': snippet}
        db.newspaper_new.insert(doc)


    time.sleep(3600)
