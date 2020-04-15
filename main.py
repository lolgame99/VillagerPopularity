from psaw import PushshiftAPI
from datetime import datetime as dt, timedelta
import json
import operator

api = PushshiftAPI()

startdate= dt.today() - timedelta(days=7)
startstamp = int(startdate.timestamp())
#Function returns a json object with all posts on acvillagers in the last week
gen = api.search_submissions(
                             after=startstamp,
                             subreddit='acvillager',
                             q='[LF]')
results1 = list(gen)
gen = api.search_submissions(
                             after=startstamp,
                             subreddit='adoptmyvillager',
                             q='[LF]')
results2 = list(gen)

villagers = []
popularityList = []
outlist = []

#Reads the villagers from file and  puts them in a list
with open('data/villagerList.txt', 'r') as villagerFile:
    for line in villagerFile:
        villagers.append(line.strip())

popularityList = [[0] * 2 for i in range(len(villagers))]

#Puts villagers into 2D list
for i in range(0, len(villagers)):
    popularityList[i][0] = villagers[i]


#Filters all entries to start with [LF], checks for blacklisted words and cuts the [FT] portion off
for each in results1:
    if each.title.startswith('[LF]'):
        out = each.title.split('[FT]')
        blacklist = ['nmt', 'nmts', 'nook mile tickes', 'villagers', 'villager']
        if not any(x in out[0].lower() for x in blacklist):
            outlist.append(out[0])

for each in results2:
    if each.title.startswith('[LF]'):
        out = each.title.split('[FT]')
        blacklist = ['nmt', 'nmts', 'nook mile tickes', 'villagers', 'villager']
        if not any(x in out[0].lower() for x in blacklist):
            outlist.append(out[0])



#Checks Submission titels for villager name accourances
for i in range(0, len(popularityList)):
    count = 0
    for each in outlist:
        format1 = " "+popularityList[i][0]+" "
        format2 = " "+popularityList[i][0]+","
        format3 = "]"+popularityList[i][0]+" "
        format4 = "]"+popularityList[i][0]+","
        format5 = ","+popularityList[i][0]+" "
        format6 = ","+popularityList[i][0]+","
        if (format1 in each.lower() or format2 in each.lower() or format3 in each.lower() or format4 in each.lower() or format5 in each.lower() or format6 in each.lower()):
            count= count+1
    popularityList[i][1] = count

popularityList = sorted(popularityList, key=operator.itemgetter(1), reverse= True)


print('r/acvillager length: ',len(results1))
print('r/adoptmyvillager length: ',len(results2))
print('RAW length: ',len(results1)+len(results2))
print('Filtered length: ',len(outlist))

with open('data/results.txt', 'w') as f:
    for line in popularityList:
        f.write(line[0]+ " - " + str(line[1]) + "\n")
