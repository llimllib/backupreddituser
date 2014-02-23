#!/usr/bin/env python

import json
import requests
import time

def backup(user, outfile, verbose=False):
    headers = {'User-Agent': 'Reddit Backupper'}
    urltemplate = "http://www.reddit.com/user/{}.json?count={}&after={}"
    after = ""
    n = 25
    count = n

    data = []

    try:
        while 1:
            url = urltemplate.format(user, count, after)
            if verbose:
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

    outfile.write(json.dumps(data, indent=4))
    outfile.close()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Backup a reddit user's data.")
    parser.add_argument('user', help='The user to backup')
    parser.add_argument('-o', dest="outfile",
                        help='The file to output (defaults to <user>.json)')
    parser.add_argument('-v', dest="verbose", action='store_true',
                        help='print out all URLs visited')

    args = parser.parse_args()
    fname = "{}.json".format(args.user) if not args.outfile else args.outfile
    fout = open(fname, 'w')

    backup(args.user, fout, args.verbose)
