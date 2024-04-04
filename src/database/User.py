import sys
import os
import bcrypt
import random
from urllib.parse import quote_plus
from time import ctime
import subprocess
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure
from datetime import date
import re

letters = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
capitals = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
numbers = (1,2,3,4,5,6,7,8,9,0)

class User():
    
    # initliser for the User class
    def __init__(self, fstatus, ffiscal_year, flifo_fifo):
        
        # sets the values for status, fiscal_year and lifo_fifo of the user
        self.status = fstatus
        self.fiscal_year = ffiscal_year
        self.lifo_fifo = flifo_fifo
        
        