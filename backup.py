#!/usr/bin/env python

import json
import requests
import time

def backup(user, outfile):
    headers = {'User-Agent': 'Reddit Backupper'}
    urltemplate = "http://www.reddit.com/user/{}.json?count={}&after={}"
    after = ""
    n = 25
    count = n

    data = []

    try:
        while 1:
            url = urltemplate.format(user, count, after)
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

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Backup a reddit user's data.")
    parser.add_argument('user', help='The user to backup')
    parser.add_argument('-o', dest="outfile",
                        help='The file to output (defaults to <user>.json)')

    args = parser.parse_args()
    fname = "{}.json".format(args.user) if not args.outfile else args.outfile
    fout = open(fname, 'w')

    backup(args.user, fout)
