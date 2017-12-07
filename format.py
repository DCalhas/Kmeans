
original = open("Lymphoma45x4026+2classes.arff")


new = open("formatted_data.arff", "w")



oLines = original.readlines()


allData = []
classes = []

for line in oLines:
	if not "@RELATION" in line and not "@ATTRIBUTE" in line and not "@DATA" in line and line != "\n" and line != "" and line != " ":
		values = line.split(",")[:-1]
		classes += [line.split(",")[-1]]
		allData += [values]
	else:
		new.write(line)

for i in range(0, len(allData)):
	for j in range(0, len(allData[i])):
		if allData[i][j] != "?":
			allData[i][j] = float(allData[i][j])

#fill the '?'

#mean per column
mean = []

for i in range(0, len(allData[0])):
	columnMean = 0
	count = 0
	for j in range(0, len(allData)):
		if allData[j][i] != "?":
			columnMean += allData[j][i]
			count += 1
	columnMean /= count
	mean += [columnMean]

for i in range(0, len(allData)):
	for j in range(0, len(allData[i])):
		if allData[i][j] != "?":
			new.write(str(allData[i][j]))
			new.write(",")
		else:
			new.write(str(round(mean[j], 2)))
			new.write(",")
	new.write(classes[i])
