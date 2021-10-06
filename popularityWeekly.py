from psaw import PushshiftAPI
from datetime import datetime as dt, timedelta
import json
import operator
import mysql.connector

api = PushshiftAPI()
mydb = mysql.connector.connect(
  host="localhost",
  user="admin",
  passwd="Bimbo123.",
  database="acnhsite"
  )
def main():
  resultPop = []
  results1 = []
  results2 = []
  lastweek1 = []
  lastweek2 = []

  before= dt.today() - timedelta(days=7)
  after = dt.today() - timedelta(days=14)
  beforeStamp = int(before.timestamp())
  afterStamp = int(after.timestamp())


  gen = api.search_submissions(
                               after=beforeStamp,
                               subreddit='acvillager',
                               q='[LF]')
  results1 = list(gen)
  gen = api.search_submissions(
                               after=beforeStamp,
                               subreddit='adoptmyvillager',
                               q='[LF]')
  results2 = list(gen)
  #Function returns a json object with all posts on acvillagers in the last week
  resultPop = getVillagerPop(results1, results2)

  gen = api.search_submissions(
                               before=beforeStamp,
                               after=afterStamp,
                               subreddit='acvillager',
                               q='[LF]')
  lastweek1 = list(gen)
  gen = api.search_submissions(
                               before=beforeStamp,
                               after=afterStamp,
                               subreddit='adoptmyvillager',
                               q='[LF]')
  lastweek2 = list(gen)
  #Function returns a json object with all posts on acvillagers in the week before last
  lastweekPop = getVillagerPop(lastweek1, lastweek2)

  for thisWeek in resultPop:
    for lastWeek in lastweekPop:
      if thisWeek[0] == lastWeek[0]:
        thisWeek[2] = thisWeek[1] - lastWeek[1]

  try:
      with open('data/resultsWeek.txt', 'w') as f:
          for line in resultPop:
              f.write(line[0]+ ";" + str(line[1]) + ";" + str(line[2]) + "\n")
      print("Saved resultsWeek.txt file")
  except Error:
      print("Failed to save results.txt file")
      print(Error)

  mycursor = mydb.cursor()


  mycursor.execute("DELETE FROM villagerPopularityWeek;")
  mydb.commit()

  sql = "INSERT INTO villagerPopularityWeek (villager, postcount, difference) VALUES (%s, %s, %s)"
  try:
      for each in resultPop:
        val = (each[0], each[1], each[2])
        mycursor.execute(sql, val)
      mydb.commit()
      print("Inserted data into database")
  except Error:
    print("Failed to insert data into database")
    print(Error)




#Funtion to get All posts from r/acvillager and r/adoptmyvillager since the time of $startstamp
#Returns a list with villager name and number of posts
def getVillagerPop(results1, results2):

  villagers = []
  popularityList = []
  outlist = []

  #Reads the villagers from file and  puts them in a list
  with open('data/villagerList.txt', 'r') as villagerFile:
      for line in villagerFile:
          villagers.append(line.strip())

  popularityList = [[0] * 3 for i in range(len(villagers))]

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
  print("---------------------")
  return popularityList

if __name__=="__main__":
  main()
