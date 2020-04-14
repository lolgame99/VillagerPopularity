from psaw import PushshiftAPI
import json
import datetime as dt

api = PushshiftAPI()
startdate=int(dt.datetime(2020,4,7).timestamp())

gen = api.search_submissions(
                             after=startdate,
                             subreddit='acvillager',
                             q='[LF]')
results = list(gen)

with open('raw.json', 'w') as rawfile:
    json.dump(results, rawfile, indent=4)

with open('data.json', 'w') as outfile:
    outlist = []
    test = []
    for each in results:
        if each.title.startswith('[LF]'):
            out = each.title.split('[FT]')
            blacklist = ['nmt', 'nmts', 'nook mile tickes', 'villagers', 'villager']
            test.append(each)
            if not any(x in out[0] for x in blacklist):
                outlist.append(each)
                print(out[0])
    json.dump(outlist, outfile, indent=4)



print('RAW length: ',len(results))
print('LF length: ',len(test))
print('Filtered length: ',len(outlist))
