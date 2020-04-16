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
villagers = []
popularityList = []
outlist = []

#Reads the villagers from file and  puts them in a list
with open('data/villagerList.txt', 'r') as villagerFile:
    for line in villagerFile:
        villagers.append(line.strip())


popularityList = [[0] * 3 for i in range(len(villagers))]
print(popularityList)
