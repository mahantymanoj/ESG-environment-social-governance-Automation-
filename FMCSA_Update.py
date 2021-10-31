# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 14:22:22 2021

@author: Mahanty
"""


# FMCSA Data download
from Fmcsa_function import Fmcsa_table_parser
import requests, random, re, math
from bs4 import BeautifulSoup
from shutil import copyfile
from openpyxl import load_workbook
import pandas as pd
import datetime
import os


def Fmcsa_table_parser(table,pd,re):
    '''Function Parse the HTML data content to Data Frame'''
    table_row = table.find_all('tr')
    table_column = table_row[0].find_all('th')
    total_rows = len(table_row)
    # total_columns = len(table_column)+1 # since first row has one empty td which is variable name
    column_names = list(' ') # first cell is blank as per table structure
    pattern = '^\s+' 
    for th in table_column:
        cell = th.get_text()
        cell = cell.replace('\r','')
        cell = cell.replace('\n','')
        cell = re.sub(pattern,'',cell)
        column_names.append(cell)
            
    df = pd.DataFrame(columns=column_names,index=range(0,total_rows))
    rowIndex = 0
    trIndex = 0
    for row in table.find_all('tr'):
        columnIndex = 0
        td_data = row.find_all('td')
        th_data = row.find_all('th')
        if trIndex == 0:
            trIndex+=1 # rowIndex=trIndex 0 is header of the table which is column name defined for df, 
                       # skip 1st tr since it is table header
            pass 
        elif rowIndex == 0:        
            for td in td_data:
                cell = td.get_text()
                cell = cell.replace('\r','')
                cell = cell.replace('\n','')
                cell = re.sub(pattern,'',cell)
                df.iat[rowIndex,columnIndex] = cell
                columnIndex+=1
    
            for th in th_data:
                cell = th.get_text()
                cell = cell.replace('\r','')
                cell = cell.replace('\n','')
                cell = re.sub(pattern,'',cell)
                df.iat[rowIndex,columnIndex] = cell
                columnIndex+=1
            rowIndex+=1
        else:
            for th in th_data:
                cell = th.get_text()
                cell = cell.replace('\r','')
                cell = cell.replace('\n','')
                cell = re.sub(pattern,'',cell)
                df.iat[rowIndex,columnIndex] = cell
                columnIndex+=1
            
            for td in td_data:
                cell = td.get_text()
                cell = cell.replace('\r','')
                cell = cell.replace('\n','')
                cell = re.sub(pattern,'',cell)
                df.iat[rowIndex,columnIndex] = cell
                columnIndex+=1
            rowIndex+=1
            
    return df

parent_path = os.getcwd()
parent_path = parent_path.split('\\')
parent_path = parent_path[0] + '\\' + parent_path[1]
save_path = parent_path + "\\OUTPUT Files\\Basu Sir\\ESG\FMCSA\\" + str(datetime.datetime.now().strftime('%Y%m%d')) + '\\'

if not os.path.exists(save_path):
    os.makedirs(save_path)

# 0) 60 month data 1) Historic Data

historicData = 1



if historicData == 0:
    # source_template = r'D:\Python\Jupyter\FMCSA_Template.xlsx'
    source_template = parent_path + '\\Excel Template\FMCSA_Template.xlsx'
else:
    # source_template = r'D:\Python\Jupyter\FMCSA_Template - History.xlsx'
    source_template = parent_path + '\\Excel Template\FMCSA_Template - History.xlsx'


# dot_filename = r'D:\Data\ESG\FMCSA\FMCSA List.csv'
dot_filename = parent_path + '\\Data\ESG\FMCSA\FMCSA List.csv'

# raw = pd.read_excel(dot_filename)
raw = pd.read_csv(dot_filename)
raw = raw[['DOT NAME', 'CARRIER ID']]
raw = raw.dropna()  # remove NaN row which is tagged as not required
dotList = raw['CARRIER ID']

user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',]

for USDot in dotList:
    USDot = math.floor(USDot) # convert to Natural number from real Decimal number
    print(str(USDot))
    base_url = 'https://ai.fmcsa.dot.gov/SMS/Carrier/' + str(USDot) + '/History.aspx'
    user_agent = {'User-agent' : random.choice(user_agent_list)}    
    response = requests.get(url=base_url, verify=False, headers = user_agent,
                        allow_redirects=True, stream=True)
    content = response.text
    soup = BeautifulSoup(content, 'html.parser') # BeautifulSoup HTML parser
    table_tag = soup.find('table', class_='smsEvents')
    table = table_tag
    df = Fmcsa_table_parser(table, pd, re)
    if historicData == 0:
        size = df.shape
        df = df.iloc[:, list([0] + list(range(size[1]-60, size[1])))]
    save_at = save_path + str(USDot) + '.xlsx'
    
    # save Dataframe to template file
    copyfile(source_template, save_at) # Copy template file
    wb = load_workbook(save_at)
    writer = pd.ExcelWriter(save_at, engine='openpyxl') 
    writer.book = wb
    writer.sheets = dict((ws.title, ws) for ws in wb.worksheets)
    df.to_excel(writer, sheet_name='Target', index=False)
    writer.save()
        
    # df.to_csv(save_at, index=False)

print('Done..!!!!')
print(r"S:\Equities - TV India\Team Leads\Naveen\ESG-Automation Data\Materials Team-FMCSA ")