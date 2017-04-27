import xml.etree.ElementTree as xmlParser
import json as toJson
import sys
import re
from Intent import getIntent

rootElement = xmlParser.parse('output.xml')
json = dict()
currentKey = "details"
currentParagraph = ""
headings = []

for line in rootElement.iter("textline"):
    text = ""
    isLineBold = True
    for letter in line.iter("text"):
        text += letter.text
        attributes = dict(letter.attrib)
        if attributes.has_key('font') and ("Bold" not in str(attributes['font'])):
              isLineBold = False

    temp = str(text.encode('utf8', 'ignore')).replace('\n','')
    #if temp.isupper() and isLineBold:
    if isLineBold:
        intent = getIntent(str(text))
        # if currentKey == None:
        #     currentKey = re.sub(r" +", " ", temp)
        
        headings.append(currentKey)

        if len(currentParagraph) > 0 and intent != "None":
            json[currentKey] = currentParagraph
            currentKey = intent
            currentParagraph = ""
        else:
            currentParagraph += temp
    else:
        currentParagraph += temp

json["filePath"] = sys.argv[1]
f = open(sys.argv[1], "w")
f.write(toJson.dumps(json, indent = True))
f.close()

with open('headings.csv', 'a') as file:
    for heading in headings:
        file.write(heading.replace(",", " ") + ", 0" + "\n")