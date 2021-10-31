# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 14:21:48 2020

@author: Mahanty
"""


# Consumer Financial Protection Bureau
# CFPB website Data is available from 12/1/2011

fileType = 1 # 0) JSON 1) CSV
        
import requests, random, os
import datetime,calendar, json
import warnings
import pandas as pd
import scipy.io as sio
       
user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',]
user_agent = {'User-agent' : random.choice(user_agent_list)}


base_url = 'https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/?'
param_dic = {'date_received_max' : 'None', 'date_received_min' : 'None','searchField' : 'all', 
             'tab' : 'all', 'field' : 'all', 'format' : '', 'no_aggs' : 'true'}
param_dic['format'] ='json' if fileType==0 else 'csv'

dateList = list()
dateList.append(str(datetime.date(2011,12,31))) # cannot use from datetime import datetime
for i in range(2012,2021):
    for j in range(1,13):
        day = calendar.monthrange(i,j)
        day = day[1]
        dateList.append(str(datetime.date(i,j,day)))

today = datetime.datetime.today() #today date

# Download JSON or CSV file month wise from 12/1/2011 to to current last date

if os.path.exists(os.getcwd() + '\JSON') == False: 
    os.makedirs(os.getcwd() + '\JSON')
    
    
if os.path.exists(r'D:\Data\ESG\CFPB\Complaint-DB\CSV\Monthly') == False:
    os.makedirs(r'D:\Data\ESG\CFPB\Complaint-DB\CSV\Monthly')
    
from datetime import datetime,timedelta
A = ['2019-11-30']

for i in dateList:
    row = datetime.strptime(i,'%Y-%m-%d') # Last Calandar date
    year = str(row.year)
    month = row.month
    if month<10:
        month = '0' + str(month)
    else:
         month = str(month) 
    day = row.day
    if day<10:
        day = '0' + str(day)
    else:
         day = str(day)
    
    if row<today:
        startDate = row.replace(day=1) # Day:1 since it will consider from 1 day
        row+= timedelta(1) # Next month 1st day
        param_dic['date_received_max'] = str(row.year) + '-' + str(row.month) + '-' + str(row.day)
        param_dic['date_received_min'] = str(startDate.year) + '-' + str(startDate.month) + '-' + str(startDate.day)
        print(str(startDate) + '    ' + str(row) )
    else:
        break
        
    response = requests.get(url=base_url , params = param_dic,verify=False, headers = user_agent,
                            allow_redirects=True, stream = True)
    
            
    if fileType==0:
        with open(os.getcwd() + '\JSON\\' + year + month + '.json',"wb") as js:
            js.write(response.content) # downloading JSON file
    elif fileType==1:
        save_path = r'D:\Data\ESG\CFPB\Complaint-DB\CSV\Monthly\\' + year + month + '.csv'
        with open(save_path,"wb") as cs:
            cs.write(response.content)
            print(str(year + month + day) + ' Downloaded')


if fileType == 0: # Execute if JSON file are downloaded
    for i in range(0,len(dateList)):
        ## for loop for files monthly
        c_date = datetime.strptime(dateList[i],'%Y-%m-%d').strftime('%Y%m') # convert date format
        df = pd.DataFrame()
        with open(os.getcwd() +  '\JSON\\' + '20120131.json') as js:
            data = json.load(js)
            myKey = list(data[0]['_source'].keys()) # Keys from Dictionary,Variable data is a list and '_source' is a common key
            c_dateList = list()
            for dt in data:
                row = list()
                for k in myKey:
                    row.append(dt['_source'][k])
                c_dateList.append(row)

            df = pd.DataFrame(c_dateList,columns=myKey)
    #     with open(os.getcwd() +  '\JSON\\' + str(c_date) + '.csv') as file:
        df['date_received'] = pd.to_datetime(df['date_received']).dt.strftime('%Y%m%d') # Date format change to yyyymmdd
        df['date_sent_to_company'] = pd.to_datetime(df['date_sent_to_company']).dt.strftime('%Y%m%d')
        df.to_csv(r'D:\Data\ESG\CFPB\Complaint-DB\CSV\Excel\\' +  str(c_date) + '.csv',index=False)
        print(str(c_date) + ' Downloaded')


