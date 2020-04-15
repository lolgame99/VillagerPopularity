import json
outlist = []
with open('data/villagersRaw.txt', 'r') as infile:
    with open('data/villagerList.txt', 'w') as outfile:
        lines = infile.readlines()
        #outfile.write('[')
        for each in lines:
            split = each.split('(')
            outlist.append(split[0])
            print(split[0])
            #outfile.write('"'+split[0].lower()+'", ')
            outfile.write(split[0].lower()+'\n')
        #outfile.write(']')
