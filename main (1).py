# import libraries
import hashlib
import random
import string
import json
import binascii
import rsa
import numpy as np
import pandas as pd
import pylab as pl
import logging
import datetime
import collections
# following imports are required by PKI
import Crypto
import Crypto.Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from base64 import b64decode,b64encode
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
transactions = []
last_block_hash = ""
last_transaction_index = 0
pp = ""
class Block:
   def __init__(self):
      self.verified_transactions = []
      self.previous_block_hash = ""
      #self.Nonce = ""
      self.proof_of_work=""
class Client:
   def __init__(self):
      random = Crypto.Random.new().read
      self._private_key = RSA.generate(1024, random)
      self._public_key = self._private_key.publickey()
      self._signer = PKCS1_v1_5.new(self._private_key)

   @property
   def identity(self):
      return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')
class Transaction:
   def __init__(self, sender, recipient, value):
      self.sender = sender
      self.recipient = recipient
      self.value = value
      self.time = datetime.datetime.now()

   def to_dict(self):
      if self.sender == "Genesis":
         identity = "Genesis"
      else:
         identity = self.sender.identity

      return collections.OrderedDict({
         'sender': identity,
         'recipient': self.recipient,
         'value': self.value,
         'time': self.time})

   def sign_transaction(self):
      private_key = self.sender._private_key
      signer = PKCS1_v1_5.new(private_key)
      h = SHA.new(str(self.to_dict()).encode('utf8'))
      return binascii.hexlify(signer.sign(h)).decode('ascii')

def display_transaction(transaction):
      dict = transaction.to_dict()
      print("sender: " + dict['sender'])
      print("recipient: " + dict['recipient'])
      print("value: " + str(dict['value']))
      print("time: " + str(dict['time']))


Piotr = Client()
Marcin = Client()
Tomasz = Client()
Paweł = Client()

t0 = Transaction (
   "Genesis",
   Piotr.identity,
   500.0
)

t2 = Transaction(
   Piotr,
   Marcin.identity,
   6.0
)
t2.sign_transaction()
transactions.append(t2)
t3 = Transaction(
   Tomasz,
   Paweł.identity,
   2.0
)
t3.sign_transaction()
transactions.append(t3)
t4 = Transaction(
   Marcin,
   Tomasz.identity,
   4.0
)
t4.sign_transaction()
transactions.append(t4)
t5 = Transaction(
   Paweł,
   Marcin.identity,
   7.0
)
t5.sign_transaction()
transactions.append(t5)
t6 = Transaction(
   Tomasz,
   Marcin.identity,
   3.0
)
t6.sign_transaction()
transactions.append(t6)
t7 = Transaction(
   Marcin,
   Piotr.identity,
   8.0
)
t7.sign_transaction()
transactions.append(t7)
t8 = Transaction(
   Marcin,
   Tomasz.identity,
   1.0
)
t8.sign_transaction()
transactions.append(t8)
t9 = Transaction(
   Paweł,
   Piotr.identity,
   5.0
)
t9.sign_transaction()
transactions.append(t9)
t10 = Transaction(
   Paweł,
   Tomasz.identity,
   3.0
)
t10.sign_transaction()
transactions.append(t10)

block0 = Block()
block0.previous_block_hash = None
Nonce = None
block0.proof_of_work = 0
block0.verified_transactions.append (t0)
digest = hash (block0)
last_block_hash = digest

CC = []
def dump_blockchain (self):
   print ("Number of blocks in the chain: " + str(len (self)))
   for x in range (len(CC)):
      block_temp = CC[x]
      print ("block # " + str(x))
      print("proof", block_temp.proof_of_work)
      for transaction in block_temp.verified_transactions:
         display_transaction (transaction)

'''for transaction in transactions:
   display_transaction(transaction)
   '''
CC.append (block0)



def sha256(message):
   return hashlib.sha256(message.encode('ascii')).hexdigest()

def mine(message, difficulty):
   assert difficulty >= 1
   prefix = '1' * difficulty
   k = 0
   global pp
   for i in range(100000):

      digest = sha256(str(hash(message)) + str(i))
      #print(prefix)
      if digest.startswith(prefix):
         print ("after " + str(i) + " iterations found nonce: "+ digest)
         pp = str(i)
         return digest
   return -1


def encrypt(message, key):
   return rsa.encrypt(message.encode('ascii'), key)

mine(last_block_hash, 2)

login = (input("write your login"))
password = (input("write your password "))

while(login !="admin" or password != "admin"):
      login = (input("write your login"))
      password = (input("write your password "))
while(1):



   option = int(input("What do you want to do [1]-mine/add block [2]-display: [3]-add transaction "))

   if option == 1:
      k = mine(last_block_hash,4)
      if k == -1:
         print("you failed")
      else:
         print("you can now add block [press enter]")

         block = Block()
         for i in range(2):
            temp_transaction = transactions[last_transaction_index]
            block.verified_transactions.append(temp_transaction)
            last_transaction_index += 1
            block.previous_block_hash = last_block_hash

            block.proof_of_work = k + " " + str(pp)
            digest = hash(block)

         CC.append(block)
         last_block_hash = digest

   if option == 2:
      dump_blockchain(CC)

   if option == 3:
      val = int(input("how much:"))
      t = Transaction(
         Paweł,
         Piotr.identity,
         val
      )
      t.sign_transaction()
      transactions.append(t)

   else:
      continue





