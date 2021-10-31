# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 14:20:37 2020

@author: Mahanty
"""


# Run CFPB Monthly Update Code on 15 of month for Current Month. Code Update Prior Month DB and then download current month File

import requests, random, os, re
import datetime, urllib3, calendar, time
import pandas as pd
# from shutil import copyfile
from pathlib import Path
import dateutil.relativedelta
from bs4 import BeautifulSoup
import monthdelta

# --- Variable Declaration

fileType = 1 # 0) JSON 1) CSV
cutofDate = -7 # Prior 7 business date
updateMonth = ''


parent_path = os.getcwd()
parent_path = parent_path.split('\\')
parent_path = parent_path[0] + '\\' + parent_path[1]


csv_path = parent_path + '\\Data\\ESG\\CFPB\\Complaint-DB\\CSV\Monthly\\' # Read from Complaint DB
save_path = parent_path + '\\OUTPUT Files\\Basu Sir\\ESG\\CFPB\\' + datetime.datetime.today().strftime('%Y%m%d')

if os.path.exists(save_path)==False:
    os.makedirs(save_path)


user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',]

base_url = 'https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/?'


# Business Date Function
def businessDate(from_date, add_days):
    import datetime
    # Prior or Next Business Date
    if add_days>0: # Next business Date
        while add_days > 0:
            from_date += datetime.timedelta(days=1)
            weekday = from_date.weekday()
            if weekday >= 5: # sunday = 6
                continue
            add_days -= 1
    elif add_days<0: # Prior business Date
        while add_days < 0:
            from_date += datetime.timedelta(days=-1)
            weekday = from_date.weekday()
            if weekday >= 5: # sunday = 6
                continue
                
            add_days += 1
    return from_date

# csv_path = r'D:\Data\ESG\CFPB\Complaint-DB\CSV\Monthly\\'

# if os.path.exists(os.getcwd() + '\JSON\\') == False and fileType==0: os.makedirs(os.getcwd() + r'\JSON\\')
      
if os.path.exists(csv_path) == False: os.makedirs(csv_path)

if updateMonth == '':
   # updateMonth = datetime.datetime.today().strftime('%Y-%m')
    updateMonth = datetime.datetime.today()
   
else:
    updateMonth = pd.to_datetime(updateMonth)
    day = calendar.monthrange(updateMonth.year,updateMonth.month)
    updateMonth = updateMonth.replace(day = day[1])
    updateMonth = businessDate(updateMonth, cutofDate+1) # since download next date


filename = updateMonth.strftime('%Y-%m')

# Updating Last 12 Month Files
dateList = list()
today = updateMonth # today date as per update Month
dateList.append(str(updateMonth.strftime('%Y-%m-%d')))

for i in range(1,12):
    today = today - dateutil.relativedelta.relativedelta(months=1)
    day = calendar.monthrange(today.year,today.month)
    today = today.replace(day=day[1])
    dateList.append(str(today.strftime('%Y-%m-%d')))
    

# Update prior 12 month File and the download current month file

from datetime import datetime,timedelta
for i in dateList:
    row = datetime.strptime(i,'%Y-%m-%d')
    year = str(row.year)
    month = row.month
    day = row.day
    if month<10:
        month = '0' + str(month)
    else:
          month = str(month)
    
    if day<10:
        day = '0' + str(day)
    else:
          day = str(day)
            
    param_dic = {'dataNormalization' : 'None' ,'date_received_max' : 'None', 'date_received_min' : 'None',
              'searchField' : 'all', 'tab' : 'Map'}                    
            
    
    time.sleep(5) # slowing the crawler
    
    startDate = row.replace(day=1)
    row+= timedelta(1) # Next month 1st day
    param_dic['date_received_max'] = str(row.year) + '-' + str(row.month) + '-' + str(row.day)
    param_dic['date_received_min'] = str(startDate.year) + '-' + str(startDate.month) + '-' + str(startDate.day)
        
    user_agent = {'User-agent' : random.choice(user_agent_list)}        
    response = requests.get(url=base_url , params = param_dic,verify=False, headers = user_agent,
                            allow_redirects=True, stream = True)
    
    # finding number of HITS for range
    content = response.text
    contentSoup = BeautifulSoup(content,'lxml')
    contentSoup
    idx = content.find('hits')
    string = content[idx:idx+35]
    hits = re.findall('\d+',string)
    
    del param_dic['dataNormalization']
    param_dic['tab'] = 'all'
    param_dic['field'] = 'all'
    param_dic['format'] ='json' if fileType==0 else 'csv'
    param_dic['no_aggs'] = 'true'
    param_dic['size'] = str(hits[0])
    good_read = False
    while good_read == False:
        user_agent = {'User-agent' : random.choice(user_agent_list)}
        response = requests.get(url=base_url , params = param_dic,verify=False, headers = user_agent,
                                allow_redirects=True, stream = True)#
        
        if fileType==0:
            with open(os.getcwd() + '\JSON\\' + year + month + '.json',"wb") as js:
                js.write(response.content) # downloading JSON file
                urllib3.disable_warnings()
        elif fileType==1:
            with open(csv_path + year + month + '.csv',"wb") as cs:
                cs.write(response.content)
                urllib3.disable_warnings()
        filesize = Path(csv_path + year + month + '.csv').stat().st_size        
        if filesize>10:
            good_read = True
            print(str(year + month + day) + ' Downloaded')
            
print('Data Downloaded')

# Calculation Part

save_path +=  '\\CFPB_' + filename + '.xlsx'
writer = pd.ExcelWriter(save_path, engine='xlsxwriter')

manoj = [] # Variable stor date range

for j in range(0,5):
    dateList = list()
    
    today = updateMonth # consider run date
    today = today.replace(year=today.year-j) # Year-1/2/3/4
    year = today.year
    month = today.month
    
    if month<10:
        month = '0' + str(month)
    else:
        month = str(month)
    dateList.append(str(today.year) + month + '.csv')
    
    for i in range(1,13):
        today = today - monthdelta.monthdelta(1)
        month = today.month
        if month<10:
            month = '0' + str(month)
        dateList.append(str(today.year) + str(month)+'.csv')
    
        
    dateList.sort(reverse=True)
    csv_data = pd.DataFrame() # Initialized empty dataframe
    for file in dateList:
        df = pd.read_csv(csv_path + '\\' + file)
        csv_data = pd.concat([csv_data, df])
        print(file + ' ', end=' ')  

    print() # new line
    csv_data['Date received'] = pd.to_datetime(csv_data['Date received'])
    csv_data = csv_data.sort_values(by='Date received') # Sort by Date Received
    
    if j==0:
        dateSearch = pd.to_datetime(dateList[0][:-4] + '01') # fisrt date of the Month
        day = calendar.monthrange(dateSearch.year,dateSearch.month)
        lastDate = dateSearch.replace(day=day[1])
        dateSearch = businessDate(lastDate, cutofDate)
        
        csv_data = csv_data[(csv_data['Date received']<=dateSearch)]
        manoj.append(dateSearch)
        dateSearch = dateSearch.replace(year=(dateSearch.year)-1) # Roll over date - 1 year
        dateSearch = dateSearch.replace(day=(dateSearch.day)+1) # Roll over date +1 day
        csv_data = csv_data[(csv_data['Date received']>=dateSearch)]
        manoj.append(dateSearch)
        
        
    elif j>0:
        dateSearch = dateSearch.replace(day=(dateSearch.day)-1) # Roll over date +1 day
        
        csv_data = csv_data[(csv_data['Date received']<=dateSearch)]
        manoj.append(dateSearch)
        dateSearch = dateSearch.replace(year=(dateSearch.year)-1) # Roll over date - 1 year
        dateSearch = dateSearch.replace(day=(dateSearch.day)+1) # Roll over date +1 day
        csv_data = csv_data[(csv_data['Date received']>=dateSearch)]
        manoj.append(dateSearch)
        
    column=['Company Name','Total Complain','Monetary & Non-Monetary Relief',
                                    'Ratio of Monetary & Non-Monetary relief','Consumer Disputed','Ratio of Consumer Disputed']
    finalData = pd.DataFrame(columns=column) #Empty DataFrame
    companyName = csv_data.Company.unique() # List of Company

    for i in companyName:
        row = dict()
        d = csv_data[csv_data['Company']==i]
        row['Company Name'] = i        # Company Name
        row['Total Complain'] = len(d)      # Total Complain
        count = len(d[(d['Company response to consumer']==('Closed with non-monetary relief')) |
                    (d['Company response to consumer']=='Closed with monetary relief')])
        row['Monetary & Non-Monetary Relief'] = count     # Monetary and Non-Monetary Relief Count
        row['Ratio of Monetary & Non-Monetary relief'] = count/len(d) # Ratio of Monetary and Non- Monetary
        count = len(d[(d['Consumer disputed?']=='Yes')]) 
        row['Consumer Disputed'] = count # Consumer Dispute count
        row['Ratio of Consumer Disputed'] = count/len(d) # Ratio of Consumer Dispute
        if count==0:
            row['Consumer Disputed'] = 'N/A'
        row = pd.DataFrame.from_dict(row,orient='index')
        finalData=finalData.append(row.transpose())
    sheetname = dateList[0][:-4]   
    finalData.to_excel(writer, sheet_name = sheetname ,freeze_panes= (1,0) ,index=False)

writer.save()   

print('Completed....!')               



