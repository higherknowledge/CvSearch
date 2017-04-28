from docx import Document
import re
import sys
import json as toJson
from Intent import getIntent

document = Document(sys.argv[1])
paragraphs = document.paragraphs

json = dict()
json["filePath"] = sys.argv[3]
currentKey = None
para = ""
heading = "details"
headings = []
count = 0

for x in paragraphs:
    try:
        runs = x.runs

        # check for bold words and the following words till it's end are below the bold word
        for run in runs:
            tempHeading = str(run.text).strip()
            if run.font.bold and len(tempHeading) > 5 and len(tempHeading) < 40:
                # print "length is " + str(len(str(run.text)))
                print "header is " + tempHeading
                heading = re.sub(r" +", " ", heading)
                intent = getIntent(tempHeading)
                count += 1
                if intent != "None":
                    headings.append(heading)
                    json[heading] = str(para)
                    heading = intent
                    para = ""
            
            else:
                para += re.sub(r" +", " ", str(run.text.encode('utf8', 'ignore')))  
    
    except Exception as e:
        continue

f = open(sys.argv[2], "w")
f.write(toJson.dumps(json, indent = True))
f.close()

print "count is " + str(count) + "\n"

with open('headings.csv', 'a') as file:
    for heading in headings:
        file.write(heading.replace(",", " ") + ", 0" + "\n")