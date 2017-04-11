from docx import Document
import re
import sys
import json as toJson

document = Document(sys.argv[1])
paragraphs = document.paragraphs

json = dict()
currentKey = None

for x in paragraphs:
    try:
        runs = x.runs
        for run in runs:
            if run.font.bold and str(run.text).isupper() and len(str(run.text)) > 5:
                if currentKey is None or len(str(json[currentKey])) != 0:
                    currentKey = run.text
                break

        if currentKey != None:
            if not json.has_key(currentKey):
                json[currentKey] = ""
            json[currentKey] += re.sub(r" +", " ", str(x.text.encode('utf8', 'ignore')).replace(currentKey, ""))
    
    except Exception as e:
        #print e
        continue

f = open(sys.argv[2], "w")
f.write(toJson.dumps(json, indent = True))
f.close()