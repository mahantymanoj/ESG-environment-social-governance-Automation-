# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 14:24:21 2021

@author: Mahanty
"""


chromeDriverPath = r'C:\Program Files (x86)\Selenium Driver\chromedriver.exe'
from selenium import webdriver
import time

startDate = '08/23/2021'
endDate = '09/24/2021'


def FDA_EnforcementReport(startDate,endDate,chromeDriverPath):
    # Manoj - Website 1
    # FDA Access data download excel file -  U.S. Department of Health and Human Services: Enforcement Report

    driver = webdriver.Chrome(executable_path = chromeDriverPath)
    driver.get('https://www.accessdata.fda.gov/scripts/ires/index.cfm#tabNav_advancedSearch')

    dateTextBox1 = driver.find_element_by_xpath('//*[@id="classifiedFromDate"]')
    dateTextBox1.send_keys(startDate)

    dateTextBox2 = driver.find_element_by_xpath('//*[@id="classifiedToDate"]')
    dateTextBox2.send_keys(endDate)

    searchBtn = driver.find_element_by_xpath('//*[@id="btnSubmit"]')
    searchBtn.click()

    driver.implicitly_wait(5)

    cdvBtn = driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div/div[3]/div/form/div/div/div[3]/div[2]/div[3]/div/div/a[1]')
    # cdvBtn = driver.find_element_by_xpath('//*[@id="exportToCSV"]')
    cdvBtn.click()

    print('File Downloaded')


def FDA_MAUDE(startDate,endDate,chromeDriverPath):
    # Manoj - Website 2
    # FDA Access data download excel file - U.S. Department of Health and Human Services: MAUDE - Manufacturer and User Facility Device Experience

    driver = webdriver.Chrome(executable_path=chromeDriverPath)
    driver.get('https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/search.cfm')

    event = driver.find_element_by_xpath('//*[@id="EventType"]')
    event.send_keys('Death')

    dateStartBox = driver.find_element_by_xpath('//*[@id="ReportDateFrom"]')
    dateStartBox.send_keys(startDate)

    dateEndBox = driver.find_element_by_xpath('//*[@id="ReportDateTo"]')
    dateEndBox.send_keys()

    searchBtn = driver.find_element_by_xpath('//*[@id="BasicSearch"]/table/tbody/tr[7]/td/input')
    searchBtn.click()

    driver.implicitly_wait(20)

    csvBtn = driver.find_element_by_xpath('//*[@id="maudeform"]/span/span[2]/a[1]')
    csvBtn.click()
    print('File Downloaded')


def FDA_MedWatch(chromeDriverPath):
    # Pramod : Website 1
    # FDA Access data download excel file - # U.S. Department of Health and Human Services: MedWatch

    driver = webdriver.Chrome(executable_path=chromeDriverPath)
    driver.get('https://www.fda.gov/safety/medwatch-fda-safety-information-and-adverse-event-reporting-program')

    entries = driver.find_element_by_xpath('//*[@id="DataTables_Table_0_length"]/label/select')
    entries.send_keys('All')

    exportBtn = driver.find_element_by_xpath('//*[@id="DataTables_Table_0_wrapper"]/div[1]/div/div[2]/button/span')

    driver.implicitly_wait(5)
    exportBtn.click()

    print('File downloaded')


def FDA_WarningLetter(chromeDriverPath):
    # Pramod : Website 2
    # FDA Access data download excel file -  U.S. Department of Health and Human Services: Warning Letters

    driver = webdriver.Chrome(executable_path=chromeDriverPath)
    driver.get('https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-actions-and-activities/warning-letters')

    entries = driver.find_element_by_xpath('//*[@id="DataTables_Table_0_length"]/label/select')
    entries.send_keys('All')

    exportBtn = driver.find_element_by_xpath('//*[@id="DataTables_Table_0_wrapper"]/div[1]/div/div[2]/button/span')

    driver.implicitly_wait(10)

    exportBtn.click()

    print('File downloaded')
    
    
    

FDA_EnforcementReport(startDate,endDate,chromeDriverPath) # Manoj: Website 1
print('\n\n Website 1 ')

time.sleep(5)

FDA_MAUDE(startDate,endDate,chromeDriverPath) # Manoj: Website 2
print('\n\n Website 2 ')

# time.sleep(5)


##### Pramod task
# FDA_MedWatch(chromeDriverPath) # Pramod: Website 1
# print('\n\n Website 3 ')

# time.sleep(5)

# FDA_WarningLetter(chromeDriverPath) # Pramod : Website 2
# print('\n\n Website 4 ')

