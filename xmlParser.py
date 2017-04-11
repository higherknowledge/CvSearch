import xml.etree.ElementTree as xmlParser
import json as toJson
import sys

rootElement = xmlParser.parse('output.xml')
json = dict()
currentKey = None
currentParagraph = ""

for line in rootElement.iter("textline"):
    text = ""
    isLineBold = True
    for letter in line.iter("text"):
        text += letter.text
        attributes = dict(letter.attrib)
        if attributes.has_key('font') and ("Bold" not in str(attributes['font'])):
              isLineBold = False

    temp = str(text.encode('utf8', 'ignore')).replace('\n','')
    
    if temp.isupper() and isLineBold:
        if currentKey == None:
            currentKey = temp
        if len(currentParagraph) > 0 and len(temp) > 5:
            json[currentKey] = currentParagraph
            currentKey = temp
            currentParagraph = ""
        else:
            currentParagraph += temp
    else:
        currentParagraph += temp

f = open(sys.argv[1], "w")
f.write(toJson.dumps(json, indent = True))
f.close()
