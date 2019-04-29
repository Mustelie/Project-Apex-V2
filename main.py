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



# from this result, katherine is going to write this bullshit to the database
# twenty at a time 
# and then we're going make a table of how many of these are from the NYT
