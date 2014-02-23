import json
import requests
import time

headers = {'User-Agent': 'Reddit Backupper'}
urltemplate = "http://www.reddit.com/user/llimllib.json?count={}&after={}"
after = ""
n = 25
count = n

data = []

try:
    while 1:
        url = urltemplate.format(count, after)
        print url
        r = requests.get(url, headers=headers).json()

        things = r["data"]["children"]
        data += things

        last_id = r["data"]["after"]
        if not last_id or last_id == after:
            break

        after = last_id
        count += n
        time.sleep(2)
except Exception as e:
    print e

fout = open("comments.json", 'w')
fout.write(json.dumps(data, indent=4))
fout.close()
