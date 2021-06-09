import pymongo
import time
from sqlalchemy import create_engine, text



time.sleep(10) #timeshift cause mongodb need to be running first

#function to read positive and  wordlist for sentiment analysis
def read_words(sentiment):
    f = open(f'{sentiment}_words.txt', mode='r')
    result = f.readlines()
    f.close()
    result = [line.strip('\n') for line in result if not line.startswith(';') and len(line)>1]
    return result

#create list with pos/neg words
neg_words = read_words('negative')
pos_words = read_words('positive')

#connection to my_mongodb
client = pymongo.MongoClient('my_mongodb')
db = client.news_snippets_new #choose db
collection = db.newspaper_new # choose collection


#postgres data
UNAME = "postgres"
PWD = "9876"
HOST = "my_postgres"
PORT = "5432"
DB = 'postgres'

#connection to postgres container
engine = create_engine(f"postgresql://{UNAME}:{PWD}@{HOST}:{PORT}/{DB}", echo = True) 

#create table in postgres
create_query = """CREATE TABLE IF NOT EXISTS news_new (
    text TEXT,
    score NUMERIC
);"""

engine.execute(create_query)

#read entries from mongodb
entries = collection.find()

for entry in entries:
    snippet = entry['snippet'] #create textsnippet out of mongodb entry
    n_pos = len([w for w in pos_words if w in snippet])
    n_neg = len([w for w in neg_words if w in snippet])
    if n_pos > n_neg:
        engine.execute(text("""INSERT INTO news_new VALUES (:snippet, :score)"""), {'snippet':snippet, 'score': 1})
    elif n_pos < n_neg:
        engine.execute(text("""INSERT INTO news_new VALUES (:snippet, :score)"""), {'snippet':snippet, 'score': 0})
    else:
        engine.execute(text("""INSERT INTO news_new VALUES (:snippet, :score)"""), {'snippet':snippet, 'score': 2})



