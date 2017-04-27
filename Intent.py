import requests
import json

def getIntent(message):
    url = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/e12852ab-3722-42ef-8c26-352e372ef4d8"

    querystring = {"subscription-key":"9ba5a167ea0d4b2ca890c2a04786514f","verbose":"true","timezoneOffset":"0","q": message}

    headers = {
        'cache-control': "no-cache",
        'postman-token': "25d619ec-cee4-c11b-ac56-04de7f15f9e5"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    # print response.text
    try:
        res = json.loads(response.text)
        return res['topScoringIntent']['intent']
    except:
        return "None"
