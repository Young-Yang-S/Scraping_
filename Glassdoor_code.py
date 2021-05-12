# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 21:51:05 2021

@author: daiya
"""

## (1) Install packages
pip install math

pip install pandas 

pip install selenium

pip install time

pip install json

pip install random

pip install re

pip install os

pip install json

pip install numpy

pip install pyautogui


## (2) Import packages
import math
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import socket
import random
import re
import os
import json
import numpy as np
import pyautogui 



# (3) Open Chrome 
pyautogui.size()
pyautogui.moveTo(90, 1050, duration = 1)
pyautogui.click(x = 100, y = 1050, clicks = 2,button = 'left')
pyautogui.moveTo(110, 1000, duration = 1)
pyautogui.click()
pyautogui.typewrite('chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\AutomationProfile')
time.sleep(1)
pyautogui.moveTo(100, 400, duration = 1)
pyautogui.click(100,400)
socket.setdefaulttimeout(30)  # set the max loading time 30
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_driver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver11.exe"
chrome_options.add_argument("user-agent= Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36")    
driver = webdriver.Chrome(chrome_driver,  chrome_options=chrome_options)
agent = driver.execute_script("return navigator.userAgent")




# (4) Main function


# this is to get alll the overview and review links for all companies
 
# Because I scrape the these two kinds of links over time, so I put them into different
# files, but alternatively we could run the method 2 code which reads the file which contains all the companies links.


file_name = []
for files in os.listdir(r"C:\Users\daiya\OneDrive\Desktop\scrape project\test\spyder"):
    file_name.append(files)

os.chdir(r'C:\Users\daiya\OneDrive\Desktop\scrape project\test\spyder')


company_list = pd.DataFrame()

for i in file_name:
    dd=pd.read_csv(i,encoding='ISO-8859-1')
    company_list= company_list.append(dd)



company_list.reset_index(inplace=True) 

del company_list['index']

company_list = company_list.drop_duplicates()

    
company_list = company_list.iloc[:,:]



# Method 2 
company_list = pd.read_csv('company_list.csv',encoding='ISO-8859-1')




# this is to get all the companies which haven't been finished properly (sometimes not all the reviews would be scraped by some reasons, those companies are listed in this incomplete file)
file_name3 = []
for files in os.listdir(r"C:\Users\daiya\OneDrive\Desktop\Scrape\Not_completed"):
    files = files.split(r'.')[0]
    file_name3.append(files)



# this is to get all the companies which have been finished
file_name2 = []
for files in os.listdir(r"C:\Users\daiya\OneDrive\Desktop\Scrape\Completed"):
    splitter = files.split(r'.')
    if len(splitter)==2:
        files = files.split(r'.')[0]
    else:
        print(splitter)
        files = splitter[0] + '.' + splitter[1]
    file_name2.append(files)


# For the companies which has a lot of reviews like more than 15K, it can't be scraped properly because of block from server, this is the drawback of this code
   
# here scrape function is to begin to scrape companies for the company_list dataframe
    
    
company_large = []

for i in range(0,company_list.shape[0]):
    if str(company_list.iloc[i,1]) not in file_name2 and str(company_list.iloc[i,1]) not in file_name3 and company_list.iloc[i,1] not in company_large :
        print(company_list.iloc[i,1])
        tick = scrape(company_list.iloc[i,2],company_list.iloc[i,3],driver)
        if type(tick) == list:
            print(tick[0])
            company_large.append(tick[1])





# (5) Function 
def scrape(overview_link,review_link,driver):
        
# this is to get single company overview page

# data needed : ticker, location (city and state)
# link = 'https://www.glassdoor.com/Overview/Working-at-Walt-Disney-Company-EI_IE717.11,30.htm' 
    link = overview_link
    driver.get(link)
    time.sleep(2) 

    company_name = driver.find_element_by_id('DivisionsDropdownComponent').text

    print(company_name)
    
    source = driver.page_source
    
    cc =re.split(r'<div',source)
    
    try:
        locations = driver.find_element_by_xpath('//*[@id="EIOverviewContainer"]/div/div[1]/ul/li[2]/div').text
        Headquarters_City = re.split(r',',locations)[0]
        Headquarters_State = re.split(r',',locations )[1]
    except:
        locations = driver.find_element_by_xpath('//*[@id="EIOverviewContainer"]/div/div[2]/ul/li[2]/div').text
        Headquarters_City = re.split(r',',locations)[0]
        Headquarters_State = re.split(r',',locations )[1]
    
    try:
        Tickers = driver.find_element_by_xpath('//*[@id="EIOverviewContainer"]/div/div[1]/ul/li[5]/div').text
        Ticker =  re.split(r'\(',Tickers)[1][:-1]
    
    except:
        Tickers = driver.find_element_by_xpath('//*[@id="EIOverviewContainer"]/div/div[2]/ul/li[5]/div').text
        Ticker =  re.split(r'\(',Tickers)[1][:-1]

  
    
    # this is for review for single company
    
    link = review_link
    link = link + '?filter.iso3Language=eng&filter.employmentStatus=REGULAR&filter.employmentStatus=FREELANCE&filter.employmentStatus=PART_TIME&filter.employmentStatus=INTERN&filter.employmentStatus=CONTRACT'
    driver.get(link)
    page_number = page_number1()
    
    if page_number > 500:
        note = 'Too large company'
        return [note, Ticker]
    
    single = single_page1(driver)
    sleep_time = random.uniform(2,3)
    time.sleep(sleep_time)
    print(page_number)
     
       
    # links 2 is used to check whether there is some missing pages for scraping
    links2 = ['a']
    
    
    count = 0
    

    try:  
        single,links2,count = click1(count,page_number,single,links2,driver)

    except:
        driver = correct(links2,driver,count)
        flag = True
        while flag:
            if count >= page_number:
                flag = False
            try:
                single,links2, count = click1(count,page_number,single,links2,driver)
            except:
                driver = correct(links2,driver,count)
        

    it = []
    for i in range(0,len(links2)):
        if i >0:
            link = links2[i]
            link = link + '?filter.iso3Language=eng&filter.employmentStatus=REGULAR&filter.employmentStatus=FREELANCE&filter.employmentStatus=PART_TIME&filter.employmentStatus=INTERN&filter.employmentStatus=CONTRACT'
            driver.get(link)
            try:
                tmp = single_page()
                single = single.append(tmp) 
                it.append(i)
            except:
                True

    sss = single.copy()
    
    numb = []
    for i in range(0,sss.shape[0]):
        for j in range(0,sss.shape[1]):
            if type(sss.iloc[i,j]) == list:
                numb.append([i,j])
    
    
    for i in range(0,len(numb)):
        sss.iloc[numb[i][0],numb[i][1]] = sss.iloc[numb[i][0],numb[i][1]][0]
    
    sss = sss.drop_duplicates()
    
    
    # this is to add three features from overview page 
    sss['Ticker'] = Ticker
    sss['Headquarters_City'] = Headquarters_City 
    sss['Headquarters_State'] = Headquarters_State
    sss['Company_name'] = company_name 
        
    single2 = sss[['Company_name', 'Ticker', 'Headquarters_State', 'Headquarters_City', 'Date','Covid_19',
                  'helpful','Overall_Score',  'Work_Score', 'Culture_Score',
                  'Diversity_Score','Career_Score','Compensation_Score','Senior_Manage_Score',
                  'Past','Current', 'Intern', 'Contract', 'Freelance','Position', 'evaluation','Full_time',
                  'Part_time','Less_than_a_year','more_than_a_year', 'more_than_3_years',
                 'more_than_5_years','more_than_8_years','more_than_10_years','Pros',
                 'Cons','Advice to Management']]
    


# this is to make sure we gent more than 98% of reviews for a company
    if page_number*10 <=450:
        percent = single2.shape[0]/ ((page_number-1)*10)
    
    else:
        percent = single2.shape[0]/ (page_number*10)
    
    print(percent)
    
    if percent > 0.98:
        os.chdir(r'C:\Users\daiya\OneDrive\Desktop\Scrape\Completed')  
        single2.to_csv('{}.csv'.format(Ticker) ,index=False)
        
        return Ticker
    
    else:
        os.chdir(r'C:\Users\daiya\OneDrive\Desktop\Scrape')  
        single2.to_csv('{}.csv'.format(Ticker) ,index=False)
        
        return 'No'
    

# correct is to restart chrome and continue to run if the request is blocked by the server, but this part doesn't work properly
def correct(links2,driver,count):
        print(3)
        print(links2)
        driver.close()
        driver.quit()
        pyautogui.size()
        pyautogui.moveTo(90, 1050, duration = 1)
        pyautogui.click(x = 100, y = 1050, clicks = 2,button = 'left')
        pyautogui.moveTo(110, 1000, duration = 1)
        pyautogui.click()
        pyautogui.typewrite('chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\AutomationProfile')
        pyautogui.moveTo(100, 400, duration = 1)
        pyautogui.click(100,400)
        socket.setdefaulttimeout(60)  # set the max loading time 60
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        chrome_driver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver11.exe"
        chrome_options.add_argument("user-agent= Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36")    
        driver = webdriver.Chrome(chrome_driver,  chrome_options=chrome_options)
        agent = driver.execute_script("return navigator.userAgent")
        if  links2[-1] == 'None':
            link = links2[-2]
            driver.get(link)
            
        link = links2[-1]
        driver.get(link)
        return driver


def click1(count,page_number,single,links2,driver):
        for i in range (count,page_number):
            try:
                try:
                    driver.find_element_by_xpath('//*[@id="NodeReplace"]/main/div/div[1]/div/div[7]/div/div[1]/button[7]').click()
                except:
                    driver.find_element_by_xpath('//*[@id="NodeReplace"]/main/div/div[1]/div/div[6]/div/div[1]/button[7]').click()

            except:
                try:
                    driver.find_element_by_xpath('//*[@id="NodeReplace"]/main/div/div[1]/div/div[8]/div/div[1]/button[7]').click()
                except:
                    try:
                        driver.find_element_by_xpath('//*[@id="NodeReplace"]/main/div/div[1]/div/div[7]/div/div[1]/button[7]').click()
                    except:
                        try:
                             driver.find_element_by_xpath('//*[@id="NodeReplace"]/main/div/div[1]/div/div[5]/div/div[1]/button[7]').click()
                        except:
                            print('Next botton not found')
                            time.sleep(10)
            try:
                sleep_time = random.uniform(2,3)
                time.sleep(sleep_time)
                tmp = single_page1(driver)
                print('Finished Page {} out of '.format(count+1) + str(page_number))
                single = single.append(tmp) 
                count =count + 1

            except:
                links2.append(driver.current_url)
                time.sleep(10)
                print(2)  
                
        return(single,links2,count)
        

def page_number1():
    # get page number 
    number = math.ceil(int(driver.find_element_by_class_name('paginationFooter').text.split(' ')[-3].split('.')[0].replace(',', ''))/10)
    return number


def single_page1(driver):
    # get the id for every review in single page 
    print('Begin a new page!')

    time.sleep(1)
    review_link = driver.find_elements_by_class_name('empReview')
    for i in review_link:
        ids = i.get_attribute("id")
        try:
           driver.find_element_by_xpath('//*[@id= "{}"]/div/div[2]/div[2]/div[2]/div[2]'.format(ids)).click()
           time.sleep(0.5)
        except:
            True        
    # get review for single company
    review_list=['Work_Score', 'Culture_Score','Diversity_Score',
                 'Career_Score','Compensation_Score','Senior_Manage_Score',
                 'Date','Overall_Score',
                 'Current','Past', 'Intern' , 'Contract', 'Freelance',
                 'Position','evaluation','Full_time','Part_time',
                 'Less_than_a_year','more_than_a_year', 'more_than_3_years',
                 'more_than_5_years','more_than_8_years','more_than_10_years'
                 'Pros','Cons','Advice to Management','helpful', 'Covid_19']
    
    evaluation_list = [ 'approves of ceo', 'positive outlook', ' positive outlook', 'no opinion of ceo', 'disapproves of ceo',
 'recommends', ' no opinion of ceo', 'negative outlook', ' negative outlook', ' neutral outlook', "doesn't recommend",
  'neutral outlook', ' disapproves of ceo', ' approves of ceo']

    review_table = pd.DataFrame(columns=review_list)

    # this part is to get the sub scores (five)
    
    source = driver.page_source
    
    keep = []
    splitted =source
    for i in review_link:
        ids = i.get_attribute("id")
        tmp = re.split(ids,splitted)
        keep.append(tmp[0])
        nextt = tmp[1]
        splitted = nextt
        
    keep.append(nextt)
    keep = keep[1:]
    

    for i in range(0,len(review_link)):

        subev =re.split(r'undecorated',keep[i])
        if len(subev) >1:
            if re.search('minor',subev[1]):  
                subdetail = re.split(r'<\/ul>',subev[1])[0]
                detail = re.split(r'minor',subdetail)[1:]
                
                Work_Score = None
                Culture_Score = None
                Diversity_Score = None
                Career_Score = None
                Compensation_Score = None
                Senior_Manage_Score = None
                
                
                for j in detail:
                    if re.search('Life Balance',j):
                       Work_Score = re.split(r'title=',j)[1][1:4]
                       
                    elif re.search('Culture',j):
                       Culture_Score = re.split(r'title=',j)[1][1:4]
                    
                    elif re.search('Diversity',j):
                       Diversity_Score = re.split(r'title=',j)[1][1:4]
                    
                    elif re.search('Career',j):
                       Career_Score = re.split(r'title=',j)[1][1:4]
                       
                    elif re.search('Compensation',j):
                       Compensation_Score = re.split(r'title=',j)[1][1:4]
                    
                    elif re.search('Management',j):
                       Senior_Manage_Score  = re.split(r'title=',j)[1][1:4]
                    
                    else:
                        True
               
                sub_evaluation = {}
                sub_evaluation['Work_Score'] = Work_Score
                sub_evaluation['Culture_Score'] = Culture_Score
                sub_evaluation['Diversity_Score'] = Diversity_Score
                sub_evaluation['Career_Score'] = Career_Score
                sub_evaluation['Compensation_Score'] = Compensation_Score
                sub_evaluation['Senior_Manage_Score'] = Senior_Manage_Score
                

        else:
                Work_Score = None
                Culture_Score = None
                Diversity_Score = None
                Career_Score = None
                Compensation_Score = None
                Senior_Manage_Score = None   
                
                sub_evaluation = {}
                sub_evaluation['Work_Score'] = Work_Score
                sub_evaluation['Culture_Score'] = Culture_Score
                sub_evaluation['Diversity_Score'] = Diversity_Score
                sub_evaluation['Career_Score'] = Career_Score
                sub_evaluation['Compensation_Score'] = Compensation_Score
                sub_evaluation['Senior_Manage_Score'] = Senior_Manage_Score
        
# this part is to revise the format of each review, some review lacks of certain part which
# can cause some problems when scraping, key thing here is to add the missing part to make format general
         
        source = review_link[i].text.split('\n')
        
        # this could be modified
        try:
            if source[0].split('|')[1] == ' Division of Intuit':
                source = source[1:]
        
        except:
            True
            
        check = source[1].split(' ')
        check2 = source[2].split(' ')
        end = []
        for i in range(0,len(source)):
            if ('work' in source[i].lower().split()) or  ('worked' in source[i].lower().split()) or ('working' in source[i].lower().split()):
                end.append(i)
            
            if source[i] == '★★★★★':
                start = i 
                
        end = min(end)
        if re.search('Employee',source[start+1]):
            if source[start+2] == source[end]:
                empty = 'NULL'
                first = source[:start+2]
                first.append(empty)
                source = first + source[end:]
            else:
                True
                
        if source[start+1] == source[end]:
            empty = 'Employee'
            empty2 = 'NULL'
            first = source[:start+1]
            first.append(empty)
            first.append(empty2)
            source = first + source[end:]
        
# because of different length of review, this part divides it into different part to scrape
# whereas, here is the leason, actually next time when scraping the data, firstly you need to 
# quickly review all the possible format of scraping data, then preprocessing them to make it to a
# general format, then handle them for once. In this file, I wrongly divided them into different part
# then use divide and conqure method which is really fool! Tedious and easy to generate errors
            
        if 'COVID-19' not in check:
            if 'Helpful' not in check:
                sub_evaluation['Date']= source[0]
                sub_evaluation['Overall_Score'] = source[2]
# data and score                
                employee = re.split('-',source[4])[0]
                if re.search('Former',employee):
                    Past_Employee = employee.split(' ')[0]
                    Current_Employee = None
                    
                elif re.search('Current',employee):
                    Past_Employee = None
                    Current_Employee = employee.split(' ')[0]
                else:
                    Current_Employee = None
                    Past_Employee = None

                sub_evaluation['Current']=Current_Employee
                sub_evaluation['Past'] = Past_Employee
          
                if re.search('Contractor',employee):
                    contractor =  employee.split(' ')[1]
                    intern = None
                    freelance = None
                    
                elif re.search('Freelancer',employee): 
                    contractor = None
                    intern = None
                    freelance =  employee.split(' ')[1]
                
                elif re.search('Intern',employee): 
                    contractor = None
                    intern = employee.split(' ')[1]
                    freelance = None
                
                else:
                    contractor = None
                    intern = None
                    freelance = None
                
                sub_evaluation['Contract']= contractor
                sub_evaluation['Freelance'] = freelance
                sub_evaluation['Intern'] = intern
                
                
# employee type                    
                positionn = re.split('-',source[4])
                
                if len(positionn) >1 :
                    positiontest = re.split('-',source[4])[1].split(' in ')
                    position = positiontest[0]
                
                else:
                    if re.search('in ',source[4]):
                        positionn1 = re.split('in',source[4])
                        if  len(positionn1) > 1:
                            position = positionn1[0]
                        else:
                            position = None
                    else:
                        if source[4].lower() not in evaluation_list: 
                            position = source[4]
                        else:
                            position = None
                            source = source[:4] + ['1'] + source[4:]
                
                sub_evaluation['Position'] = position 
         
# position                
                if ('work' in source[5].lower().split()) or  ('worked' in source[5].lower().split()) or ('working' in source[5].lower().split()):
                    sub_evaluation['evaluation'] = 'None'
                    if re.search('part',source[5]):
                        part_time = 'part time'
                        full_time = None
                        
                    elif re.search('full',source[5]):
                        part_time = None
                        full_time = 'full time'
                    
                    else:
                        full_time = None
                        part_time = None
                    
                    time_length = re.split(r'for ',source[5])
                    if len(time_length) >1:
                                 if re.split(r' ', time_length[1])[2] == 'a':
                                     if re.split(r' ', time_length[1])[0] == 'less':
                                         less_than_a_year = 'less than a year'
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                                     else:
                                         less_than_a_year =  None
                                         more_than_a_year =  'More than a year'
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                                         
                                 elif re.split(r' ', time_length[1])[2] == '3':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = 'More than 3 years'
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                                
                                 elif re.split(r' ', time_length[1])[2] == '5':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = 'More than 5 years'
                                         more_than_8_years = None
                                         more_than_10_years = None
                                         
                                 elif re.split(r' ', time_length[1])[2] == '8':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = 'More than 8 years'
                                         more_than_10_years = None
                                 
                                 elif re.split(r' ', time_length[1])[2:4][0] == '10':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = 'More than 10 years'
                                         
                                 else:
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                                 
                                 
                    else:
                                
                                less_than_a_year = None
                                more_than_a_year =  None
                                more_than_3_years = None
                                more_than_5_years = None
                                more_than_8_years = None
                                more_than_10_years = None
                                
                
                else:
                    if ('work' in source[6].lower().split()) or  ('worked' in source[6].lower().split()) or ('working' in source[6].lower().split()): 
                        sub_evaluation['evaluation'] = source[5]
                        if re.search('part',source[6]):
                             part_time = 'part time'
                             full_time = None
                        
                        elif re.search('full',source[6]):
                            part_time = None
                            full_time = 'full time'
                    
                        else:
                            full_time = None
                            part_time = None
                        
                        time_length = re.split(r'for ',source[6])
                        if len(time_length) >1:
                                 if re.split(r' ', time_length[1])[2] == 'a':
                                     if re.split(r' ', time_length[1])[0] == 'less':
                                         less_than_a_year = 'less than a year'
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                                     else:
                                         less_than_a_year =  None
                                         more_than_a_year =  'More than a year'
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                                         
                                 elif re.split(r' ', time_length[1])[2] == '3':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = 'More than 3 years'
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                                
                                 elif re.split(r' ', time_length[1])[2] == '5':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = 'More than 5 years'
                                         more_than_8_years = None
                                         more_than_10_years = None
                                         
                                 elif re.split(r' ', time_length[1])[2] == '8':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_10_years = None
                                         more_than_8_years = 'More than 8 years'
                                                
                                 elif re.split(r' ', time_length[1])[2:4][0] == '10':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = 'More than 10 years'
                                         
                                 else:
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                        else:
                                
                                less_than_a_year = None
                                more_than_a_year =  None
                                more_than_3_years = None
                                more_than_5_years = None
                                more_than_8_years = None
                                more_than_10_years = None
                            
                    else:
                        if ('work' in source[7].lower().split()) or  ('worked' in source[7].lower().split()) or ('working' in source[7].lower().split()):
                            evaluation = []
                            evaluation.append(source[5])
                            evaluation.append(source[6])
                            evaluation = ', '.join(evaluation)
                            sub_evaluation['evaluation']=evaluation
                            if re.search('part',source[7]):
                                part_time = 'part time'
                                full_time = None
                        
                            elif re.search('full',source[7]):
                                part_time = None
                                full_time = 'full time'
                    
                            else:
                                full_time = None
                                part_time = None
                                
                            time_length = re.split(r'for ',source[7])
                            if len(time_length) >1:
                                 if re.split(r' ', time_length[1])[2] == 'a':
                                     if re.split(r' ', time_length[1])[0] == 'less':
                                         less_than_a_year = 'less than a year'
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                                     else:
                                         less_than_a_year =  None
                                         more_than_a_year =  'More than a year'
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                                         
                                 elif re.split(r' ', time_length[1])[2] == '3':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = 'More than 3 years'
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                                
                                 elif re.split(r' ', time_length[1])[2] == '5':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = 'More than 5 years'
                                         more_than_8_years = None
                                         more_than_10_years = None
                                         
                                 elif re.split(r' ', time_length[1])[2] == '8':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_10_years = None
                                         more_than_8_years = 'More than 8 years'
                                
                                 elif re.split(r' ', time_length[1])[2:4][0] == '10':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = 'More than 10 years'
                                 else:
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                            else:
                                
                                less_than_a_year = None
                                more_than_a_year =  None
                                more_than_3_years = None
                                more_than_5_years = None
                                more_than_8_years = None
                                more_than_10_years = None
                            
                                
                        else:
                            evaluation = []
                            evaluation.append(source[5])
                            evaluation.append(source[6])
                            evaluation.append(source[7])
                            evaluation = ', '.join(evaluation)
                            sub_evaluation['evaluation'] = evaluation
                            if re.search('part',source[8]):
                                part_time = 'part time'
                                full_time = None
                        
                            elif re.search('full',source[8]):
                                part_time = None
                                full_time = 'full time'
                    
                            else:
                                full_time = None
                                part_time = None
                            
                            
                            time_length = re.split(r'for ',source[8])
                            if len(time_length)>1:
                                 if re.split(r' ', time_length[1])[2] == 'a':
                                     if re.split(r' ', time_length[1])[0] == 'less':
                                         less_than_a_year = 'less than a year'
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                                         
                                     else:
                                         less_than_a_year =  None
                                         more_than_a_year =  'More than a year'
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                                         
                                         
                                 elif re.split(r' ', time_length[1])[2] == '3':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = 'More than 3 years'
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                                
                                 elif re.split(r' ', time_length[1])[2] == '5':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = 'More than 5 years'
                                         more_than_8_years = None
                                         more_than_10_years = None
                                         
                                 elif re.split(r' ', time_length[1])[2] == '8':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = 'More than 8 years'
                                         more_than_10_years = None
                                         
                                
                                 elif re.split(r' ', time_length[1])[2:4][0] == '10':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = 'More than 10 years'
                                         
                                         
                                 else:
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                            else:
                                
                                less_than_a_year = None
                                more_than_a_year =  None
                                more_than_3_years = None
                                more_than_5_years = None
                                more_than_8_years = None
                                more_than_10_years = None
                            
                                
                                
                sub_evaluation['Full_time'] = full_time
                sub_evaluation['Part_time'] = part_time
                
                sub_evaluation['Less_than_a_year'] = less_than_a_year
                sub_evaluation['more_than_a_year'] = more_than_a_year
                sub_evaluation['more_than_3_years'] = more_than_3_years
                sub_evaluation['more_than_5_years'] = more_than_5_years
                sub_evaluation['more_than_8_years'] = more_than_8_years
                sub_evaluation['more_than_10_years'] = more_than_10_years
                
# evaluation, part time or full time, length for working
                       
                for i in range(0,len(source)):
                    if source[i] == 'Pros':
                        pros = []
                        for i in range(source.index('Pros')+1,source.index('Cons')):
                            pros.append(source[i])
                        pros = ' '.join(pros)
                        sub_evaluation['Pros'] = pros
                        
            
                if 'Advice to Management' in source:
                   cons = [] 
                   for i in range(source.index('Cons')+1,source.index('Advice to Management')):
                        cons.append(source[i])
                   cons = ' '.join(cons)
                   sub_evaluation['Cons'] = cons
                   
                else:  
                    value=0
                    for i in range(0,len(source)):
                        check = source[i].split(' ')
                        if 'Helpful' in check:  
                            if i > value:
                                value = i
                    cons = []
                    for i in range(source.index('Cons')+1,value):
                        cons.append(source[i])
                    cons = ' '.join(cons)
                    sub_evaluation['Cons'] = cons
        
                if 'Advice to Management' in source:
                    sub_evaluation['Advice to Management'] = source[source.index('Advice to Management')+1]
                else:
                    sub_evaluation['Advice to Management'] = 'None'
                
                sub_evaluation['helpful'] = None
                sub_evaluation['Covid_19'] = None
# pros and cons, adive to management and helpful, covid_19

# append each review to final table
                
                for k in sub_evaluation:
                    sub_evaluation[k] = [sub_evaluation[k]]
        
                tmp = pd.DataFrame.from_dict(sub_evaluation)
                

                review_table = review_table.append(tmp)

            else:
                sub_evaluation['helpful'] = check[1]
                sub_evaluation['Covid_19'] = None
                source.remove(source[1])
                sub_evaluation['Date']= source[0]
                sub_evaluation['Overall_Score'] = source[2]
                
                
                employee = re.split('-',source[4])[0]
                if re.search('Former',employee):
                    Past_Employee = employee.split(' ')[0]
                    Current_Employee = None
                    
                elif re.search('Current',employee):
                    Past_Employee = None
                    Current_Employee = employee.split(' ')[0]
                else:
                    Current_Employee = None
                    Past_Employee = None

                sub_evaluation['Current']=Current_Employee
                sub_evaluation['Past'] = Past_Employee
                
                if re.search('Contractor',employee):
                    contractor =  employee.split(' ')[1]
                    intern = None
                    freelance = None
                    
                elif re.search('Freelancer',employee): 
                    contractor = None
                    intern = None
                    freelance =  employee.split(' ')[1]
                
                elif re.search('Intern',employee): 
                    contractor = None
                    intern = employee.split(' ')[1]
                    freelance = None
                
                else:
                    contractor = None
                    intern = None
                    freelance = None
                
                sub_evaluation['Contract']= contractor
                sub_evaluation['Freelance'] = freelance
                sub_evaluation['Intern'] = intern
            
            
                positionn = re.split('-',source[4])
                
                if len(positionn) >1 :
                    positiontest = re.split('-',source[4])[1].split(' in ')
                    position = positiontest[0]
                
                else:
                    if re.search('in ',source[4]):
                        positionn1 = re.split('in',source[4])
                        if  len(positionn1) > 1:
                            position = positionn1[0]
                        else:
                            position = None
                    else:
                        if source[4].lower() not in evaluation_list: 
                            position = source[4]
                        else:
                            position = None
                            source = source[:4] + ['1'] + source[4:]
                
                sub_evaluation['Position'] = position 
                
                
                if ('work' in source[5].lower().split()) or  ('worked' in source[5].lower().split()) or ('working' in source[5].lower().split()):
                    sub_evaluation['evaluation'] = 'None'
                    if re.search('part',source[5]):
                        part_time = 'part time'
                        full_time = None
                        
                    elif re.search('full',source[5]):
                        part_time = None
                        full_time = 'full time'
                    
                    else:
                        full_time = None
                        part_time = None
                    
                    time_length = re.split(r'for ',source[5])
                    if len(time_length) >1:
                                 if re.split(r' ', time_length[1])[2] == 'a':
                                     if re.split(r' ', time_length[1])[0] == 'less':
                                         less_than_a_year = 'less than a year'
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                                     else:
                                         less_than_a_year =  None
                                         more_than_a_year =  'More than a year'
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                                         
                                 elif re.split(r' ', time_length[1])[2] == '3':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = 'More than 3 years'
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                                
                                 elif re.split(r' ', time_length[1])[2] == '5':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = 'More than 5 years'
                                         more_than_8_years = None
                                         more_than_10_years = None
                                         
                                 elif re.split(r' ', time_length[1])[2] == '8':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = 'More than 8 years'
                                         more_than_10_years = None
                                 
                                 elif re.split(r' ', time_length[1])[2:4][0] == '10':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = 'More than 10 years'
                                         
                                 else:
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                                 
                                 
                    else:
                                
                                less_than_a_year = None
                                more_than_a_year =  None
                                more_than_3_years = None
                                more_than_5_years = None
                                more_than_8_years = None
                                more_than_10_years = None
                                
                
                else:
                    if ('work' in source[6].lower().split()) or  ('worked' in source[6].lower().split()) or ('working' in source[6].lower().split()): 
                        sub_evaluation['evaluation'] = source[5]
                        if re.search('part',source[6]):
                             part_time = 'part time'
                             full_time = None
                        
                        elif re.search('full',source[6]):
                            part_time = None
                            full_time = 'full time'
                    
                        else:
                            full_time = None
                            part_time = None
                        
                        time_length = re.split(r'for ',source[6])
                        if len(time_length) >1:
                                 if re.split(r' ', time_length[1])[2] == 'a':
                                     if re.split(r' ', time_length[1])[0] == 'less':
                                         less_than_a_year = 'less than a year'
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                                     else:
                                         less_than_a_year =  None
                                         more_than_a_year =  'More than a year'
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                                         
                                 elif re.split(r' ', time_length[1])[2] == '3':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = 'More than 3 years'
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                                
                                 elif re.split(r' ', time_length[1])[2] == '5':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = 'More than 5 years'
                                         more_than_8_years = None
                                         more_than_10_years = None
                                         
                                 elif re.split(r' ', time_length[1])[2] == '8':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_10_years = None
                                         more_than_8_years = 'More than 8 years'
                                                
                                 elif re.split(r' ', time_length[1])[2:4][0] == '10':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = 'More than 10 years'
                                         
                                 else:
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                        else:
                                
                                less_than_a_year = None
                                more_than_a_year =  None
                                more_than_3_years = None
                                more_than_5_years = None
                                more_than_8_years = None
                                more_than_10_years = None
                            
                    else:
                        if ('work' in source[7].lower().split()) or  ('worked' in source[7].lower().split()) or ('working' in source[7].lower().split()):
                            evaluation = []
                            evaluation.append(source[5])
                            evaluation.append(source[6])
                            evaluation = ', '.join(evaluation)
                            sub_evaluation['evaluation']=evaluation
                            if re.search('part',source[7]):
                                part_time = 'part time'
                                full_time = None
                        
                            elif re.search('full',source[7]):
                                part_time = None
                                full_time = 'full time'
                    
                            else:
                                full_time = None
                                part_time = None
                                
                            time_length = re.split(r'for ',source[7])
                            if len(time_length) >1:
                                 if re.split(r' ', time_length[1])[2] == 'a':
                                     if re.split(r' ', time_length[1])[0] == 'less':
                                         less_than_a_year = 'less than a year'
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                                     else:
                                         less_than_a_year =  None
                                         more_than_a_year =  'More than a year'
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                                         
                                 elif re.split(r' ', time_length[1])[2] == '3':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = 'More than 3 years'
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                                
                                 elif re.split(r' ', time_length[1])[2] == '5':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = 'More than 5 years'
                                         more_than_8_years = None
                                         more_than_10_years = None
                                         
                                 elif re.split(r' ', time_length[1])[2] == '8':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_10_years = None
                                         more_than_8_years = 'More than 8 years'
                                
                                 elif re.split(r' ', time_length[1])[2:4][0] == '10':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = 'More than 10 years'
                                 else:
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                            else:
                                
                                less_than_a_year = None
                                more_than_a_year =  None
                                more_than_3_years = None
                                more_than_5_years = None
                                more_than_8_years = None
                                more_than_10_years = None
                            
                                
                        else:
                            evaluation = []
                            evaluation.append(source[5])
                            evaluation.append(source[6])
                            evaluation.append(source[7])
                            evaluation = ', '.join(evaluation)
                            sub_evaluation['evaluation'] = evaluation
                            if re.search('part',source[8]):
                                part_time = 'part time'
                                full_time = None
                        
                            elif re.search('full',source[8]):
                                part_time = None
                                full_time = 'full time'
                    
                            else:
                                full_time = None
                                part_time = None
                            
                            
                            time_length = re.split(r'for ',source[8])
                            if len(time_length)>1:
                                 if re.split(r' ', time_length[1])[2] == 'a':
                                     if re.split(r' ', time_length[1])[0] == 'less':
                                         less_than_a_year = 'less than a year'
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                                         
                                     else:
                                         less_than_a_year =  None
                                         more_than_a_year =  'More than a year'
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                                         
                                         
                                 elif re.split(r' ', time_length[1])[2] == '3':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = 'More than 3 years'
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                                
                                 elif re.split(r' ', time_length[1])[2] == '5':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = 'More than 5 years'
                                         more_than_8_years = None
                                         more_than_10_years = None
                                         
                                 elif re.split(r' ', time_length[1])[2] == '8':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = 'More than 8 years'
                                         more_than_10_years = None
                                         
                                
                                 elif re.split(r' ', time_length[1])[2:4][0] == '10':
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = 'More than 10 years'
                                         
                                         
                                 else:
                                         less_than_a_year = None
                                         more_than_a_year =  None
                                         more_than_3_years = None
                                         more_than_5_years = None
                                         more_than_8_years = None
                                         more_than_10_years = None
                            else:
                                
                                less_than_a_year = None
                                more_than_a_year =  None
                                more_than_3_years = None
                                more_than_5_years = None
                                more_than_8_years = None
                                more_than_10_years = None
                            
                                
                                
                sub_evaluation['Full_time'] = full_time
                sub_evaluation['Part_time'] = part_time
                
                sub_evaluation['Less_than_a_year'] = less_than_a_year
                sub_evaluation['more_than_a_year'] = more_than_a_year
                sub_evaluation['more_than_3_years'] = more_than_3_years
                sub_evaluation['more_than_5_years'] = more_than_5_years
                sub_evaluation['more_than_8_years'] = more_than_8_years
                sub_evaluation['more_than_10_years'] = more_than_10_years
                
                       
                for i in range(0,len(source)):
                    if source[i] == 'Pros':
                        pros = []
                        for i in range(source.index('Pros')+1,source.index('Cons')):
                            pros.append(source[i])
                        pros = ' '.join(pros)
                        sub_evaluation['Pros'] = pros
                        
            
                if 'Advice to Management' in source:
                   cons = [] 
                   for i in range(source.index('Cons')+1,source.index('Advice to Management')):
                        cons.append(source[i])
                   cons = ' '.join(cons)
                   sub_evaluation['Cons'] = cons
                   
                else:  
                    value=0
                    for i in range(0,len(source)):
                        check = source[i].split(' ')
                        if 'Helpful' in check:  
                            if i > value:
                                value = i
                    cons = []
                    for i in range(source.index('Cons')+1,value):
                        cons.append(source[i])
                    cons = ' '.join(cons)
                    sub_evaluation['Cons'] = cons
        
                if 'Advice to Management' in source:
                    sub_evaluation['Advice to Management'] = source[source.index('Advice to Management')+1]
                else:
                    sub_evaluation['Advice to Management'] = 'None'
                
                
                for k in sub_evaluation:
                    sub_evaluation[k] = [sub_evaluation[k]]
        
                tmp = pd.DataFrame.from_dict(sub_evaluation)
    
                review_table = review_table.append(tmp)

                
        else:
            if 'Helpful' not in check2:
                    sub_evaluation['helpful'] = None
                    sub_evaluation['Covid_19'] = 'Covid_19'
                    source.remove(source[1])
                    sub_evaluation['Date']= source[0]
                    sub_evaluation['Overall_Score'] = source[2]
                    
                    employee = re.split('-',source[4])[0]
                    if re.search('Former',employee):
                        Past_Employee = employee.split(' ')[0]
                        Current_Employee = None

                    elif re.search('Current',employee):
                        Past_Employee = None
                        Current_Employee = employee.split(' ')[0]
                    else:
                        Current_Employee = None
                        Past_Employee = None

                    sub_evaluation['Current']=Current_Employee
                    sub_evaluation['Past'] = Past_Employee

                    if re.search('Contractor',employee):
                        contractor =  employee.split(' ')[1]
                        intern = None
                        freelance = None

                    elif re.search('Freelancer',employee): 
                        contractor = None
                        intern = None
                        freelance =  employee.split(' ')[1]

                    elif re.search('Intern',employee): 
                        contractor = None
                        intern = employee.split(' ')[1]
                        freelance = None

                    else:
                        contractor = None
                        intern = None
                        freelance = None

                    sub_evaluation['Contract']= contractor
                    sub_evaluation['Freelance'] = freelance
                    sub_evaluation['Intern'] = intern

                    positionn = re.split('-',source[4])

                    if len(positionn) >1 :
                        positiontest = re.split('-',source[4])[1].split(' in ')
                        position = positiontest[0]

                    else:
                        if re.search('in ',source[4]):
                            positionn1 = re.split('in',source[4])
                            if  len(positionn1) > 1:
                                position = positionn1[0]
                            else:
                                position = None
                        else:
                            if source[4].lower() not in evaluation_list: 
                                position = source[4]
                            else:
                                position = None
                                source = source[:4] + ['1'] + source[4:]

                    sub_evaluation['Position'] = position 
                    
                    
                    if ('work' in source[5].lower().split()) or  ('worked' in source[5].lower().split()) or ('working' in source[5].lower().split()):
                        sub_evaluation['evaluation'] = 'None'
                        if re.search('part',source[5]):
                            part_time = 'part time'
                            full_time = None
                            
                        elif re.search('full',source[5]):
                            part_time = None
                            full_time = 'full time'
                        
                        else:
                            full_time = None
                            part_time = None
                        
                        time_length = re.split(r'for ',source[5])
                        if len(time_length) >1:
                                     if re.split(r' ', time_length[1])[2] == 'a':
                                         if re.split(r' ', time_length[1])[0] == 'less':
                                             less_than_a_year = 'less than a year'
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                                         else:
                                             less_than_a_year =  None
                                             more_than_a_year =  'More than a year'
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                                             
                                     elif re.split(r' ', time_length[1])[2] == '3':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = 'More than 3 years'
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                                    
                                     elif re.split(r' ', time_length[1])[2] == '5':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = 'More than 5 years'
                                             more_than_8_years = None
                                             more_than_10_years = None
                                             
                                     elif re.split(r' ', time_length[1])[2] == '8':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = 'More than 8 years'
                                             more_than_10_years = None
                                     
                                     elif re.split(r' ', time_length[1])[2:4][0] == '10':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = 'More than 10 years'
                                             
                                     else:
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                                     
                                     
                        else:
                                    
                                    less_than_a_year = None
                                    more_than_a_year =  None
                                    more_than_3_years = None
                                    more_than_5_years = None
                                    more_than_8_years = None
                                    more_than_10_years = None
                                    
                    
                    else:
                        if ('work' in source[6].lower().split()) or  ('worked' in source[6].lower().split()) or ('working' in source[6].lower().split()): 
                            sub_evaluation['evaluation'] = source[5]
                            if re.search('part',source[6]):
                                 part_time = 'part time'
                                 full_time = None
                            
                            elif re.search('full',source[6]):
                                part_time = None
                                full_time = 'full time'
                        
                            else:
                                full_time = None
                                part_time = None
                            
                            time_length = re.split(r'for ',source[6])
                            if len(time_length) >1:
                                     if re.split(r' ', time_length[1])[2] == 'a':
                                         if re.split(r' ', time_length[1])[0] == 'less':
                                             less_than_a_year = 'less than a year'
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                                         else:
                                             less_than_a_year =  None
                                             more_than_a_year =  'More than a year'
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                                             
                                     elif re.split(r' ', time_length[1])[2] == '3':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = 'More than 3 years'
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                                    
                                     elif re.split(r' ', time_length[1])[2] == '5':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = 'More than 5 years'
                                             more_than_8_years = None
                                             more_than_10_years = None
                                             
                                     elif re.split(r' ', time_length[1])[2] == '8':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_10_years = None
                                             more_than_8_years = 'More than 8 years'
                                                    
                                     elif re.split(r' ', time_length[1])[2:4][0] == '10':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = 'More than 10 years'
                                             
                                     else:
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                            else:
                                    
                                    less_than_a_year = None
                                    more_than_a_year =  None
                                    more_than_3_years = None
                                    more_than_5_years = None
                                    more_than_8_years = None
                                    more_than_10_years = None
                                
                        else:
                            if ('work' in source[7].lower().split()) or  ('worked' in source[7].lower().split()) or ('working' in source[7].lower().split()):
                                evaluation = []
                                evaluation.append(source[5])
                                evaluation.append(source[6])
                                evaluation = ', '.join(evaluation)
                                sub_evaluation['evaluation']=evaluation
                                if re.search('part',source[7]):
                                    part_time = 'part time'
                                    full_time = None
                            
                                elif re.search('full',source[7]):
                                    part_time = None
                                    full_time = 'full time'
                        
                                else:
                                    full_time = None
                                    part_time = None
                                    
                                time_length = re.split(r'for ',source[7])
                                if len(time_length) >1:
                                     if re.split(r' ', time_length[1])[2] == 'a':
                                         if re.split(r' ', time_length[1])[0] == 'less':
                                             less_than_a_year = 'less than a year'
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                                         else:
                                             less_than_a_year =  None
                                             more_than_a_year =  'More than a year'
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                                             
                                     elif re.split(r' ', time_length[1])[2] == '3':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = 'More than 3 years'
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                                    
                                     elif re.split(r' ', time_length[1])[2] == '5':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = 'More than 5 years'
                                             more_than_8_years = None
                                             more_than_10_years = None
                                             
                                     elif re.split(r' ', time_length[1])[2] == '8':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_10_years = None
                                             more_than_8_years = 'More than 8 years'
                                    
                                     elif re.split(r' ', time_length[1])[2:4][0] == '10':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = 'More than 10 years'
                                     else:
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                                else:
                                    
                                    less_than_a_year = None
                                    more_than_a_year =  None
                                    more_than_3_years = None
                                    more_than_5_years = None
                                    more_than_8_years = None
                                    more_than_10_years = None
                                
                                    
                            else:
                                evaluation = []
                                evaluation.append(source[5])
                                evaluation.append(source[6])
                                evaluation.append(source[7])
                                evaluation = ', '.join(evaluation)
                                sub_evaluation['evaluation'] = evaluation
                                if re.search('part',source[8]):
                                    part_time = 'part time'
                                    full_time = None
                            
                                elif re.search('full',source[8]):
                                    part_time = None
                                    full_time = 'full time'
                        
                                else:
                                    full_time = None
                                    part_time = None
                                
                                
                                time_length = re.split(r'for ',source[8])
                                if len(time_length)>1:
                                     if re.split(r' ', time_length[1])[2] == 'a':
                                         if re.split(r' ', time_length[1])[0] == 'less':
                                             less_than_a_year = 'less than a year'
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                                             
                                         else:
                                             less_than_a_year =  None
                                             more_than_a_year =  'More than a year'
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                                             
                                             
                                     elif re.split(r' ', time_length[1])[2] == '3':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = 'More than 3 years'
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                                    
                                     elif re.split(r' ', time_length[1])[2] == '5':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = 'More than 5 years'
                                             more_than_8_years = None
                                             more_than_10_years = None
                                             
                                     elif re.split(r' ', time_length[1])[2] == '8':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = 'More than 8 years'
                                             more_than_10_years = None
                                             
                                    
                                     elif re.split(r' ', time_length[1])[2:4][0] == '10':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = 'More than 10 years'
                                             
                                             
                                     else:
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                                else:
                                    
                                    less_than_a_year = None
                                    more_than_a_year =  None
                                    more_than_3_years = None
                                    more_than_5_years = None
                                    more_than_8_years = None
                                    more_than_10_years = None
                                
                                    
                                    
                    sub_evaluation['Full_time'] = full_time
                    sub_evaluation['Part_time'] = part_time
                    
                    sub_evaluation['Less_than_a_year'] = less_than_a_year
                    sub_evaluation['more_than_a_year'] = more_than_a_year
                    sub_evaluation['more_than_3_years'] = more_than_3_years
                    sub_evaluation['more_than_5_years'] = more_than_5_years
                    sub_evaluation['more_than_8_years'] = more_than_8_years
                    sub_evaluation['more_than_10_years'] = more_than_10_years
                    
                           
                    for i in range(0,len(source)):
                        if source[i] == 'Pros':
                            pros = []
                            for i in range(source.index('Pros')+1,source.index('Cons')):
                                pros.append(source[i])
                            pros = ' '.join(pros)
                            sub_evaluation['Pros'] = pros
                            
                
                    if 'Advice to Management' in source:
                       cons = [] 
                       for i in range(source.index('Cons')+1,source.index('Advice to Management')):
                            cons.append(source[i])
                       cons = ' '.join(cons)
                       sub_evaluation['Cons'] = cons
                       
                    else:  
                        value=0
                        for i in range(0,len(source)):
                            check = source[i].split(' ')
                            if 'Helpful' in check:  
                                if i > value:
                                    value = i
                        cons = []
                        for i in range(source.index('Cons')+1,value):
                            cons.append(source[i])
                        cons = ' '.join(cons)
                        sub_evaluation['Cons'] = cons
            
                    if 'Advice to Management' in source:
                        sub_evaluation['Advice to Management'] = source[source.index('Advice to Management')+1]
                    else:
                        sub_evaluation['Advice to Management'] = 'None'
                    
    
                    for k in sub_evaluation:
                        sub_evaluation[k] = [sub_evaluation[k]]
            
                    tmp = pd.DataFrame.from_dict(sub_evaluation)

                    review_table = review_table.append(tmp)

            
            else:
                    sub_evaluation['helpful'] = check2
                    sub_evaluation['Covid_19'] = 'Covid_19'
                    source.remove(source[1])
                    source.remove(source[1])
                    sub_evaluation['Date']= source[0]
                    sub_evaluation['Overall_Score'] = source[2]
                    
                    employee = re.split('-',source[4])[0]
                    if re.search('Former',employee):
                        Past_Employee = employee.split(' ')[0]
                        Current_Employee = None

                    elif re.search('Current',employee):
                        Past_Employee = None
                        Current_Employee = employee.split(' ')[0]
                    else:
                        Current_Employee = None
                        Past_Employee = None

                    sub_evaluation['Current']=Current_Employee
                    sub_evaluation['Past'] = Past_Employee

                    if re.search('Contractor',employee):
                        contractor =  employee.split(' ')[1]
                        intern = None
                        freelance = None

                    elif re.search('Freelancer',employee): 
                        contractor = None
                        intern = None
                        freelance =  employee.split(' ')[1]

                    elif re.search('Intern',employee): 
                        contractor = None
                        intern = employee.split(' ')[1]
                        freelance = None

                    else:
                        contractor = None
                        intern = None
                        freelance = None

                    sub_evaluation['Contract']= contractor
                    sub_evaluation['Freelance'] = freelance
                    sub_evaluation['Intern'] = intern
                        
                    positionn = re.split('-',source[4])

                    if len(positionn) >1 :
                        positiontest = re.split('-',source[4])[1].split(' in ')
                        position = positiontest[0]

                    else:
                        if re.search('in ',source[4]):
                            positionn1 = re.split('in',source[4])
                            if  len(positionn1) > 1:
                                position = positionn1[0]
                            else:
                                position = None
                        else:
                            if source[4].lower() not in evaluation_list: 
                                position = source[4]
                            else:
                                position = None
                                source = source[:4] + ['1'] + source[4:]

                    sub_evaluation['Position'] = position 

                    
                    if ('work' in source[5].lower().split()) or  ('worked' in source[5].lower().split()) or ('working' in source[5].lower().split()):
                        sub_evaluation['evaluation'] = 'None'
                        if re.search('part',source[5]):
                            part_time = 'part time'
                            full_time = None
                            
                        elif re.search('full',source[5]):
                            part_time = None
                            full_time = 'full time'
                        
                        else:
                            full_time = None
                            part_time = None
                        
                        time_length = re.split(r'for ',source[5])
                        if len(time_length) >1:
                                     if re.split(r' ', time_length[1])[2] == 'a':
                                         if re.split(r' ', time_length[1])[0] == 'less':
                                             less_than_a_year = 'less than a year'
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                                         else:
                                             less_than_a_year =  None
                                             more_than_a_year =  'More than a year'
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                                             
                                     elif re.split(r' ', time_length[1])[2] == '3':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = 'More than 3 years'
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                                    
                                     elif re.split(r' ', time_length[1])[2] == '5':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = 'More than 5 years'
                                             more_than_8_years = None
                                             more_than_10_years = None
                                             
                                     elif re.split(r' ', time_length[1])[2] == '8':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = 'More than 8 years'
                                             more_than_10_years = None
                                     
                                     elif re.split(r' ', time_length[1])[2:4][0] == '10':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = 'More than 10 years'
                                             
                                     else:
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                                     
                                     
                        else:
                                    
                                    less_than_a_year = None
                                    more_than_a_year =  None
                                    more_than_3_years = None
                                    more_than_5_years = None
                                    more_than_8_years = None
                                    more_than_10_years = None
                                    
                    
                    else:
                        if ('work' in source[6].lower().split()) or  ('worked' in source[6].lower().split()) or ('working' in source[6].lower().split()): 
                            sub_evaluation['evaluation'] = source[5]
                            if re.search('part',source[6]):
                                 part_time = 'part time'
                                 full_time = None
                            
                            elif re.search('full',source[6]):
                                part_time = None
                                full_time = 'full time'
                        
                            else:
                                full_time = None
                                part_time = None
                            
                            time_length = re.split(r'for ',source[6])
                            if len(time_length) >1:
                                     if re.split(r' ', time_length[1])[2] == 'a':
                                         if re.split(r' ', time_length[1])[0] == 'less':
                                             less_than_a_year = 'less than a year'
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                                         else:
                                             less_than_a_year =  None
                                             more_than_a_year =  'More than a year'
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                                             
                                     elif re.split(r' ', time_length[1])[2] == '3':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = 'More than 3 years'
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                                    
                                     elif re.split(r' ', time_length[1])[2] == '5':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = 'More than 5 years'
                                             more_than_8_years = None
                                             more_than_10_years = None
                                             
                                     elif re.split(r' ', time_length[1])[2] == '8':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_10_years = None
                                             more_than_8_years = 'More than 8 years'
                                                    
                                     elif re.split(r' ', time_length[1])[2:4][0] == '10':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = 'More than 10 years'
                                             
                                     else:
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                            else:
                                    
                                    less_than_a_year = None
                                    more_than_a_year =  None
                                    more_than_3_years = None
                                    more_than_5_years = None
                                    more_than_8_years = None
                                    more_than_10_years = None
                                
                        else:
                            if ('work' in source[7].lower().split()) or  ('worked' in source[7].lower().split()) or ('working' in source[7].lower().split()):
                                evaluation = []
                                evaluation.append(source[5])
                                evaluation.append(source[6])
                                evaluation = ', '.join(evaluation)
                                sub_evaluation['evaluation']=evaluation
                                if re.search('part',source[7]):
                                    part_time = 'part time'
                                    full_time = None
                            
                                elif re.search('full',source[7]):
                                    part_time = None
                                    full_time = 'full time'
                        
                                else:
                                    full_time = None
                                    part_time = None
                                    
                                time_length = re.split(r'for ',source[7])
                                if len(time_length) >1:
                                     if re.split(r' ', time_length[1])[2] == 'a':
                                         if re.split(r' ', time_length[1])[0] == 'less':
                                             less_than_a_year = 'less than a year'
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                                         else:
                                             less_than_a_year =  None
                                             more_than_a_year =  'More than a year'
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                                             
                                     elif re.split(r' ', time_length[1])[2] == '3':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = 'More than 3 years'
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                                    
                                     elif re.split(r' ', time_length[1])[2] == '5':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = 'More than 5 years'
                                             more_than_8_years = None
                                             more_than_10_years = None
                                             
                                     elif re.split(r' ', time_length[1])[2] == '8':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_10_years = None
                                             more_than_8_years = 'More than 8 years'
                                    
                                     elif re.split(r' ', time_length[1])[2:4][0] == '10':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = 'More than 10 years'
                                     else:
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                                else:
                                    
                                    less_than_a_year = None
                                    more_than_a_year =  None
                                    more_than_3_years = None
                                    more_than_5_years = None
                                    more_than_8_years = None
                                    more_than_10_years = None
                                
                                    
                            else:
                                evaluation = []
                                evaluation.append(source[5])
                                evaluation.append(source[6])
                                evaluation.append(source[7])
                                evaluation = ', '.join(evaluation)
                                sub_evaluation['evaluation'] = evaluation
                                if re.search('part',source[8]):
                                    part_time = 'part time'
                                    full_time = None
                            
                                elif re.search('full',source[8]):
                                    part_time = None
                                    full_time = 'full time'
                        
                                else:
                                    full_time = None
                                    part_time = None
                                
                                
                                time_length = re.split(r'for ',source[8])
                                if len(time_length)>1:
                                     if re.split(r' ', time_length[1])[2] == 'a':
                                         if re.split(r' ', time_length[1])[0] == 'less':
                                             less_than_a_year = 'less than a year'
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                                             
                                         else:
                                             less_than_a_year =  None
                                             more_than_a_year =  'More than a year'
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                                             
                                             
                                     elif re.split(r' ', time_length[1])[2] == '3':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = 'More than 3 years'
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                                    
                                     elif re.split(r' ', time_length[1])[2] == '5':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = 'More than 5 years'
                                             more_than_8_years = None
                                             more_than_10_years = None
                                             
                                     elif re.split(r' ', time_length[1])[2] == '8':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = 'More than 8 years'
                                             more_than_10_years = None
                                             
                                    
                                     elif re.split(r' ', time_length[1])[2:4][0] == '10':
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = 'More than 10 years'
                                             
                                             
                                     else:
                                             less_than_a_year = None
                                             more_than_a_year =  None
                                             more_than_3_years = None
                                             more_than_5_years = None
                                             more_than_8_years = None
                                             more_than_10_years = None
                                else:
                                    
                                    less_than_a_year = None
                                    more_than_a_year =  None
                                    more_than_3_years = None
                                    more_than_5_years = None
                                    more_than_8_years = None
                                    more_than_10_years = None
                                
                                    
                                    
                    sub_evaluation['Full_time'] = full_time
                    sub_evaluation['Part_time'] = part_time
                    
                    sub_evaluation['Less_than_a_year'] = less_than_a_year
                    sub_evaluation['more_than_a_year'] = more_than_a_year
                    sub_evaluation['more_than_3_years'] = more_than_3_years
                    sub_evaluation['more_than_5_years'] = more_than_5_years
                    sub_evaluation['more_than_8_years'] = more_than_8_years
                    sub_evaluation['more_than_10_years'] = more_than_10_years
                    
                           
                    for i in range(0,len(source)):
                        if source[i] == 'Pros':
                            pros = []
                            for i in range(source.index('Pros')+1,source.index('Cons')):
                                pros.append(source[i])
                            pros = ' '.join(pros)
                            sub_evaluation['Pros'] = pros
                            
                
                    if 'Advice to Management' in source:
                       cons = [] 
                       for i in range(source.index('Cons')+1,source.index('Advice to Management')):
                            cons.append(source[i])
                       cons = ' '.join(cons)
                       sub_evaluation['Cons'] = cons
                       
                    else:  
                        value=0
                        for i in range(0,len(source)):
                            check = source[i].split(' ')
                            if 'Helpful' in check:  
                                if i > value:
                                    value = i
                        cons = []
                        for i in range(source.index('Cons')+1,value):
                            cons.append(source[i])
                        cons = ' '.join(cons)
                        sub_evaluation['Cons'] = cons
            
                    if 'Advice to Management' in source:
                        sub_evaluation['Advice to Management'] = source[source.index('Advice to Management')+1]
                    else:
                        sub_evaluation['Advice to Management'] = 'None'
                    
                    
                    for k in sub_evaluation:
                        sub_evaluation[k] = [sub_evaluation[k]]
            
                    tmp = pd.DataFrame.from_dict(sub_evaluation)
 
                    review_table = review_table.append(tmp)
    
    return review_table