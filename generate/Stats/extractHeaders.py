count = file("output.txt", "r")
lines = str(count.read())
count.close()
lines = lines.split("\n")

count = 0

output = file("headers.txt", "w")

for line in lines:
    if "header" in line:
        count += 1
        try:
            output.write(line.split()[2] + "\n")
        except:
            print "fail"

output.close()
