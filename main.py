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
def EverythingParams10days():
    parameter = {
        "apiKey": api_keys.newsAPIKey,
        "q": "mueller",
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


queryMueller = EverythingParams10days()
articlesMueller = getEverythingAbout(queryMueller)

conn = sqlite3.connect('news.sqlite')
cur = conn.cursor()
#cur.execute("drop table if exists NewsStories")
cur.execute("drop table if exists NewsStories")
cur.execute('''create table if not exists NewsStories (title text, link text, sourcename text, time_posted TIMESTAMP)''')
for i in range(0,5):
    pagenumb = 20*i
    for newsdict in articlesMueller['articles'][pagenumb:(pagenumb+20)]:
        cur.execute('''insert into NewsStories values (?,?,?,?)''', (
            newsdict['title'], newsdict['url'], newsdict['source']['name'], newsdict['publishedAt']))
    conn.commit()
# from this result, katherine is going to write this to the database
# twenty at a time 
# and then we're going make a table of how many of these are from the NYT

# still need to select the database portion 
cur.execute("SELECT sourcename FROM NewsStories ")
sourcesLists = cur.fetchall()
#print(sourcesLists)
sourcelist = [source[0] for source in sourcesLists]

def FrequencyofSources(listFromDatabase):
    freqSources = {} 
    for source in listFromDatabase: 
        if source not in freqSources: 
            freqSources[source] = 1 
        else: 
            freqSources[source] += 1
    return json.dumps(freqSources)


muellerdictionary = FrequencyofSources(sourcelist)


with open("sourcesfrequencies.txt", "w+") as frequencies: 
    frequencies.write(muellerdictionary)

#visualization portion is here 
openedjson = open("sourcesfrequencies.txt", "r")
openedmuellerdata = json.loads(openedjson.read())

#print(openedmuellerdata)
setkeys = openedmuellerdata.keys()
newkeylist = sorted(setkeys, key=lambda k: openedmuellerdata[k])[:10]
daybar = plt.pie([openedmuellerdata[key] for key in newkeylist], labels = newkeylist, shadow=True, startangle=90)
plt.title('Number of Articles Published by the Publisher')
plt.savefig('muellergraph.png')

# HERES THE PORTION FOR THE NEW YORK TIMES AND NEWS API COMPARISON
cur.execute("drop table if exists NYTStories")
cur.execute('''create table if not exists NYTStories (link text, time_posted TIMESTAMP)''')
for page in range(0,10):
    NYTParamsNetanyahu = {
    "q": "Netanyahu", 
    "page": page, 
    "sort": "newest", 
    "api-key": api_keys.nytAPIkey}
    nytresponses = requests.get("https://api.nytimes.com/svc/search/v2/articlesearch.json?", params = NYTParamsNetanyahu)
    everythingnyt = json.loads(nytresponses.text)
    #write into the data base here at this point 
    for nytdict in everythingnyt['response']['docs']:
        var1 = nytdict['web_url']
        var2 = nytdict['pub_date']
        cur.execute('''insert into NYTStories values (?,?)''', (var1, var2))
    conn.commit()

paramsNYTcompNEWSAPIdotORG = {
    "apiKey": api_keys.newsAPIKey,  
    "q": "Netanyahu",    
    "sortBy": "publishedAt", 
    "pageSize": 100, 
    "sources": "the-new-york-times" 
}
def EverythingCompNYT(dictofparams):
    responses = requests.get(baseURL+EverythingEndpoints, params = dictofparams)
    everythingfromNYT = json.loads(responses.text)

    return everythingfromNYT
SameParamsNewsApiNews = EverythingCompNYT(paramsNYTcompNEWSAPIdotORG)
cur.execute("drop table if exists NewsStoriesvsNYT")
cur.execute('''create table if not exists NewsStoriesvsNYT (title text, link text, sourcename text, time_posted TIMESTAMP)''')
for i in range(0,5):
    pagenumb = 20*i
    for newsdict in SameParamsNewsApiNews['articles'][pagenumb:(pagenumb+20)]:
        cur.execute('''insert into NewsStoriesvsNYT values (?,?,?,?)''', (
            newsdict['title'], newsdict['url'], newsdict['source']['name'], newsdict['publishedAt']))
    conn.commit()

cur.execute("SELECT link FROM NYTStories")
list1 = cur.fetchall()
cur.execute("SELECT link FROM NewsStoriesvsNYT")
list2 = cur.fetchall()

# MAKE THE LISTS HERE 


def similaritiesbetweenboth(list1, list2): 
    counter = 0
    for url in list1: 
        if url in list2: 
            counter += 1 
    return counter

counts = similaritiesbetweenboth(list1, list2)
with open("amountofmatches.txt", "w+") as matches: 
    strings = """
    When looking at the at the two api keys with the same 
    parameters, newsapi.org had a success/ match rate of {}$""".format(counts)
    matches.write(strings)

daybar = plt.pie([counts, 100-counts], labels = ["NYT Stories", "Non-NYT Stories"],
                 shadow=True, colors=['indigo', 'turquoise'], startangle=90)
plt.title('Number of Articles Published by the NYT from News API Results')
plt.legend(["NYT Stories", "Non-NYT Stories"])
plt.savefig('netanyahugraph.png')