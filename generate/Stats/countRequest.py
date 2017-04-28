count = file("output.txt", "r")
lines = str(count.read())

lines = lines.split("\n")

count = 0

for line in lines:
    if "count" in line:
        count += int(line.split()[2])

print count

# count without condition 3128
# count with condition 2833