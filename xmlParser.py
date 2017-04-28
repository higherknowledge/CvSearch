import xml.etree.ElementTree as xmlParser
import json as toJson
import sys
import re
from Intent import getIntent

try:

    rootElement = xmlParser.parse('output.xml')
    json = dict()
    currentKey = "details"
    currentParagraph = ""
    headings = []

    for line in rootElement.iter("textline"):
        text = ""
        isLineBold = True
        count = 0
        boldCount = 0

        for letter in line.iter("text"):
            text += letter.text
            attributes = dict(letter.attrib)
            count += 1
            if attributes.has_key('font') and ("Bold" in str(attributes['font'])):
                boldCount += 1
        
        isLineBold = boldCount >= (count / 2)
        temp = str(text.encode('utf8', 'ignore')).replace('\n','').strip()
        
        if isLineBold and len(text) > 5 and len(text) < 40:
            try:
                intent = getIntent(str(text))

            except:
                intent = "None"
                print "in catch"
            
            headings.append(currentKey)

            if len(currentParagraph) > 0 and intent != "None":
                json[currentKey] = currentParagraph
                currentKey = intent
                currentParagraph = ""

            else:
                currentParagraph += temp
        else:
            currentParagraph += temp

    json["filePath"] = sys.argv[2]

    f = open(sys.argv[1], "w")
    f.write(toJson.dumps(json, indent = True))
    f.close()


    with open('headings.csv', 'a') as file:
        for heading in headings:
            file.write(heading.replace(",", " ") + ", 0" + "\n")
except:
    print "NO XML"