# -*- coding: utf-8 -*-
"""
Created on Tue May 11 19:58:08 2021

@author: daiya
"""

# this is the function which is used to scrape the overview and review links from glassdoor.

def valid_company(number):

    Companylist = ['Company_Name','Ticker','Overview','Review']
    Valid_Company = pd.DataFrame(columns=Companylist)
    link = "https://www.glassdoor.com/Explore/browse-companies.htm?overall_rating_low=0&page={}&isHiringSurge=0".format(number)
    driver.get(link)
    time.sleep(2)
    # this part is for getting the overview page and review page link for single homepage
    all_id =driver.find_elements_by_class_name('justify-content-lg-end')
    
    source = driver.page_source
    
    cc =re.split(r'<a',source)
    
    mid = []
    for i in cc:
        tmp = re.split(r' ',i)
        mid = mid +tmp
    
    link_review = []
    for i in mid:
        tmp = re.search('href="\/Reviews.*',i) 
        if tmp != None:
            link_review.append(i)
            
    final_list = []
    for i in link_review:
        if i != 'href="/Reviews/index.htm"':
            tmp = 'https://www.glassdoor.com' + i[6:-1]
            final_list.append(tmp)
    
    
    link_overview = []
    for num in range(1,len(final_list)+1):
        try:
            overview = driver.find_element_by_xpath('//*[@id="ReactCompanyExplorePageContainer"]/div/div/div/div/div[2]/section[{}]/div/div[6]/div/a'.format(num)).get_attribute("href")
            link_overview.append(overview)
        except:
            continue
        
    total_list = []    
    for i in range(0,len(final_list)):
        tmp_ = final_list[i].split('Reviews')[1][1:-1]
        for j in range(0,len(link_overview)):
            if re.search(tmp_, link_overview[j]):
                tmpp = [final_list[i],link_overview[j]]
                total_list.append(tmpp)
        
    for i in range(0,len(total_list)):
        overview_link =  total_list[i][1]
        print(overview_link)
        driver.get(overview_link)
        time.sleep(1)
        try:
            Tickers = driver.find_element_by_xpath('//*[@id="EIOverviewContainer"]/div/div[1]/ul/li[5]/div').text
            Ticker =  re.split(r'\(',Tickers)[1][:-1]
        except:
            Ticker = 1
        
        if Ticker !=1:
          company_name = driver.find_element_by_xpath('//*[@id="DivisionsDropdownComponent"]').text
          data = [[company_name,Ticker,overview_link, total_list[i][0]]]
          tmp = pd.DataFrame(data,columns = Companylist)
          Valid_Company = Valid_Company.append(tmp)
        
        else:
            continue    

        
    name= str(random.randrange(0,1000000))+'.jpg'           
    os.chdir(r'C:\Users\daiya\OneDrive\Desktop\scrape project\test')  
    Valid_Company.to_csv('{}.csv'.format(name),index=False)           

