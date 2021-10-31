# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 14:16:43 2020

@author: Mahanty
"""

import pandas as pd
import pyodbc
import random
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
dest_dir = parent_path + "\\OUTPUT Files\\Basu Sir\\ESG\\fda_inspection_esg\\"

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

data_resp = requests.get('https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/inspection-classification-database',verify=False,headers = user_agent)
data_str = data_resp.text
soup = BeautifulSoup(data_str, 'html.parser')

elements = soup.findAll('a')
for element in elements:
    try:
        if element.img['alt'] =='New':
            print(element['href'])
            urllib.request.urlretrieve(r'https://www.fda.gov//' + element['href'], dest_dir + print_date + ' Inspection_Classification_DB.xlsx')
            print('https://www.fda.gov/' + element['href'])
            print(dest_dir + ' ||  downloaded')
    except:
        continue

