count = file("output.txt", "r")
lines = str(count.read())
count.close()
lines = lines.split("\n")

count = 0

output = file("headlen.csv", "w")

for line in lines:
    if "length" in line:
        count += 1
        output.write(str(count) + "," + (line.split()[2]) + "\n")

output.close()
