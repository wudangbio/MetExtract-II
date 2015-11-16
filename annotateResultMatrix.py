import csv

import pprint

pp = pprint.PrettyPrinter(indent=1)


# defines a group (input data) for which statistic columns (_Stat_) are calculated
def addGroup(to, groupName, minCount, cols):
    to[groupName] = {}

    to[groupName]["minCount"] = minCount
    to[groupName]["colsNames"] = cols
    to[groupName]["cols"] = []

# matches the input columns to the respective statistic column
def matchRows(groups, rowNames):
    for groupName, groupProps in groups.iteritems():
        for rowName in groupProps["colsNames"]:
            for i in range(len(rowNames)):
                if rowNames[i] == rowName:
                    groupProps["cols"].append(i)


# re-arrange data and add statistic columns
def addStatsColumnToResults(metaFile, groups, toFile, outputOrder, commentStartingCharacter="#"):
    data = []
    comments = []

    with open(metaFile, "rb") as x:
        meta = csv.reader(x, delimiter="\t")

        rowNum = 0
        for line in meta:
            if line[0].startswith(commentStartingCharacter):
                comments.append(line[0].strip())
                continue

            if rowNum == 0:
                headers = line
                matchRows(groups, line)
            else:
                data.append(line)
            rowNum += 1

    for groupName in outputOrder:
        headers.append(groupName)

    for row in data:
        for groupName in outputOrder:
            found = 0
            for pos in groups[groupName]["cols"]:
                try:
                    if row[pos].strip() != "":
                        found += 1
                except:
                    pass;
            row.append(str(found))

    data = sorted(data, key=lambda x: (float(x[4]), float(x[1])))   # sort results according to rt and mz
    data.insert(0, headers)

    with open(toFile, "wb") as x:
        metaWriter = csv.writer(x, delimiter="\t")
        for row in data:
            metaWriter.writerow(row)
        for comment in comments:
            metaWriter.writerow([comment])


# omit those columns that have less results than required by the user input
def performGroupOmit(infile, groupStats, outfile, commentStartingCharacter="#"):
    data = []
    headers = {}
    hrow = []
    comments = []

    with open(infile, "rb") as x:
        meta = csv.reader(x, delimiter="\t")

        rowNum = 0
        for line in meta:
            if line[0].startswith(commentStartingCharacter):
                comments.append(line[0].strip())
                continue

            if rowNum == 0:
                hrow = line
                for i in range(len(line)):
                    headers[line[i]] = i

            else:
                use = False
                for gname, gmin, gomit in groupStats:
                    use = use or (not gomit) or (int(line[headers[gname]]) >= gmin)
                if use:
                    data.append(line)
            rowNum += 1

    with open(outfile, "wb") as x:
        metaWriter = csv.writer(x, delimiter="\t")
        metaWriter.writerow(hrow)
        for row in data:
            metaWriter.writerow(row)
        for comment in comments:
            metaWriter.writerow([comment])

