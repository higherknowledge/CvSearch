import json

csv = file("queries.csv", "r")
lines = str(csv.read())
csv.close()

cache = dict()

for line in lines.split("\n")[1:]:
    try:
        values = line.split(",")   
        cache[values[0].replace("\"", "")] = str(line[line.index("\"{\"\"query"):]).replace("\"\"", "'").replace("\"", "")
    except:
        print "no response"

cache = json.dumps(cache, indent = True)

jsonFile = file("cache.json", "w+")
jsonFile.write(cache)
