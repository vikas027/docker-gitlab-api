#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Borrowed and slightly improved from https://gist.github.com/vitalyisaev2/215f890e75252cd36794221c2debf365
Script creates an 'admin' Personal Access Token for Gitlab API.
It spits out the token

Tested with GitLab Community Edition 10.8.4

Example: ./<script> <name-of-token> <expiry>
./<script> mytoken 2020-08-27

## Requirements :-
1) Python3
2) Sript needs below environment variables to be setup:
  - GITLAB_URL='http://<IP>:<port>'
  - GITLAB_ADMIN_USER='root'
  - GITLAB_ADMIN_PASSWD='5iveL!fe'

TO-DO:
A lot of improvements can be done on this script, will do that as time permits. Few of those are :-
- Use argparse to have arguments
- Parameterize Scopes - api, read_user, sudo, read_repository
- Convert this into a GoLang script to remove the dependencies and reduce the footprint of docker image
"""

# Import Modules
import os
import sys
import requests
import argparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# Variables
endpoint = os.environ['GITLAB_URL']
login = os.environ['GITLAB_ADMIN_USER']
password = os.environ['GITLAB_ADMIN_PASSWD']
scopes = {'personal_access_token[scopes][]': [
    'api', 'sudo', 'read_user', 'read_repository']}
root_route = urljoin(endpoint, "/")
sign_in_route = urljoin(endpoint, "/users/sign_in")
pat_route = urljoin(endpoint, "/profile/personal_access_tokens")


# Methods
def find_csrf_token(text):
    soup = BeautifulSoup(text, "lxml")
    token = soup.find(attrs={"name": "csrf-token"})
    param = soup.find(attrs={"name": "csrf-param"})
    data = {param.get("content"): token.get("content")}
    return data


def obtain_csrf_token():
    r = requests.get(root_route)
    token = find_csrf_token(r.text)
    return token, r.cookies


def sign_in(csrf, cookies):
    data = {
        "user[login]": login,
        "user[password]": password,
        "user[remember_me]": 0,
        "utf8": "✓"
    }
    data.update(csrf)
    r = requests.post(sign_in_route, data=data, cookies=cookies)
    token = find_csrf_token(r.text)
    return token, r.history[0].cookies


def obtain_personal_access_token(name, expires_at, csrf, cookies):
    data = {
        "personal_access_token[expires_at]": expires_at,
        "personal_access_token[name]": name,
        "utf8": "✓"
    }
    data.update(scopes)
    data.update(csrf)
    r = requests.post(pat_route, data=data, cookies=cookies)
    soup = BeautifulSoup(r.text, "lxml")
    token = soup.find('input', id='created-personal-access-token').get('value')
    return token


def main():
    # print(endpoint)
    csrf1, cookies1 = obtain_csrf_token()
    #print("root", csrf1, cookies1)
    csrf2, cookies2 = sign_in(csrf1, cookies1)
    #print("sign_in", csrf2, cookies2)

    name = sys.argv[1]
    expires_at = sys.argv[2]
    token = obtain_personal_access_token(name, expires_at, csrf2, cookies2)
    print(token)


if __name__ == "__main__":
    main()
