# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 14:18:14 2020

@author: Mahanty
"""


import pandas as pd
import pyodbc
import random
# import plotly.graph_objects as go
from bs4 import BeautifulSoup, SoupStrainer
import requests
import time
import os
from shutil import copyfile
from openpyxl import load_workbook
from pandas import ExcelWriter
import csv
import urllib.request
import datetime

print_date=datetime.datetime.today().strftime('%m-%d-%Y')
parent_path = os.getcwd()
parent_path = parent_path.split('\\')
parent_path = parent_path[0] + '\\' + parent_path[1]

dest_dir = parent_path + "\\OUTPUT Files\\Basu Sir\\ESG\\WHO_esg\\"
if not os.path.isdir(dest_dir):
    os.makedirs(dest_dir)

user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]
user_agent_temp = random.choice(user_agent_list)
user_agent = {'User-agent': user_agent_temp}
urllib.request.urlretrieve(r'https://extranet.who.int/pqweb/content/prequalified-lists/medicines/export', dest_dir + print_date + '_medicine.csv')
print(dest_dir + ' ||  downloaded')
