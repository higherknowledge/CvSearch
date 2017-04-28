import requests
import json
import pickle

filePath = "../LUIS/cache.pickle"

with open(filePath, "rb") as c:
    try:
        cache = pickle.load(c)
    except:
        cache = {}

def getIntent(message):
    #return "none"
    if(cache.has_key(message)):
        intents = cache[message]
        print "message : " + message + ", replying from cache \n"
        return intents['intents'][0]['intent']

    url = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/e12852ab-3722-42ef-8c26-352e372ef4d8"

    querystring = {"subscription-key":"3b2d4fa28c0a4282a91831e3d8be47cd","verbose":"true","timezoneOffset":"0","q": message}

    headers = {
        'cache-control': "no-cache"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    
    try:
        res = json.loads(response.text)
        intent = res['topScoringIntent']['intent']
        newCache = {}
        newCache["intents"] = list()
        newCache["intents"].append({'intent': intent, 'score': res['topScoringIntent']['score'], 'query': message})
        cache[message] = newCache
        
        with open(filePath, "wb") as c:
            pickle.dump(cache, c)
        
        return intent

    except Exception as e:
        print e 
        return "None"

