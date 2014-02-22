#import praw
#import json
#from pprint import pformat as pf
#
#r = praw.Reddit(user_agent='backupcomments')
#r.config.store_json_result = True
#me = r.get_redditor("llimllib")
#comments = me.get_comments(count=25)
#fout = open("comments.json", 'w')
#fout.write("[\n")
#for comment in comments:
#    print comment
#    fout.write(json.dumps(comment.json_dict, indent=4))
#    fout.write(",\n")
#fout.write('"null"]')
#fout.close()

import json
import requests
import time

headers = {'User-Agent': 'Reddit Backupper'}
urltemplate = "http://www.reddit.com/user/llimllib.json?count={}&after={}"
after = ""
n = 25
count = n

fout = open("comments.json", 'w')
data = []

while 1:
    url = urltemplate.format(count, after)
    print url
    r = requests.get(url, headers=headers).json()

    fout.write(json.dumps(r.json(), indent=4))
    fout.write(",")

    last_id = r.json()["data"]["children"][-1]["data"]["name"]
    if last_id == after:
        from pprint import pprint as pp
        pp(r.json()["data"]["children"][-1])
        print last_id, after
        break
    after = last_id
    count += n
    time.sleep(2)

fout.write('""]')
fout.close()
