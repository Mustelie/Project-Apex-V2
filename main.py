import matplotlib
import matplotlib.pyplot as plt
import json
import sqlite3

import requests
import api_keys

topHeadlinesEndpoints = "/v2/top-headlines?"
EverythingEndpoints = "/v2/everything?"
baseURL = "https://newsapi.org"
newyorktimesID = "the-new-york-times"


# here is jsut everything aboout a query from a time constraint
def EverythingParams10days(query):
    parameter = {
        "apiKey": api_keys.newsAPIKey,
        "q": query,
        "pageSize": 100,
        "from": "2019-04-29",
        "to": "2019-04-19",
        "sortBy": "relevancy"
    }
    return parameter


def getEverythingAbout(dictofparams):
    responses = requests.get(baseURL + EverythingEndpoints, params=dictofparams)
    everything = json.loads(responses.text)

    return everything


queryMueller = EverythingParams10days("mueller")
articlesMueller = getEverythingAbout(queryMueller)

conn = sqlite3.connect('news.sqlite')
cur = conn.cursor()
cur.execute("drop table if exists NewsStories")
cur.execute('''create table NewsStories (title text, link text, sourcename text, time_posted TIMESTAMP)''')
for i in range(0,6):
    pagenumb = 20*i
    for newsdict in articlesMueller['articles'][pagenumb:(pagenumb+20)]:
        cur.execute('''insert into Tweets values (?,?,?)''', (
            newsdict['title'], newsdict['url'], newsdict['source']['name'], newsdict['publishedAt']))
conn.commit()

# from this result, katherine is going to write this to the database
# twenty at a time 
# and then we're going make a table of how many of these are from the NYT

cur.execute('SELECT sourcename FROM NewsStories')
database = cur.fetchall()

def FrequencyofSources(listFromDatabase):
    freqSources = {} 
    for source in database: 
        if source not in freqSources: 
            freqSources[source] = 1 
        else: 
            freqSources[source] += 1
    return freqSources


muellerdictionary = ''

def writetoJson(dictionaryofcounts):
    with open("sourcesfrequencies.txt", "w+") as json: 
        json.write(muellerdictionary)

openedjson = open("sourcefrequencies.txt", "r")
openedmuellerdata = openedjson.loads()

setkeys = openedmuellerdata.keys()
daybar = plt.bar(setkeys, [openedmuellerdata[key] for key in setkeys])
plt.ylabel('Number of Articles')
plt.xlabel('Article Source')
plt.title('Number of Articles Published by the Publisher')
plt.show()



