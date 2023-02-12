# import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def extract(page,position):
    # headers = {'Users-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
    position = position.replace(" ","%20")
    url = f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={position}&location=United%20States&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start={page}'
    options = Options()
    options.headless = True  
    driver = webdriver.Chrome('C://Users//omkar//Downloads//CS242//jobSearchEngine-CS242-//chromedriver',options=options)  # Optional argument,

    driver.get(url)
    html_content = driver.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(html_content, 'html.parser')
    # soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup):
    options = Options()
    options.headless = True  
    driver = webdriver.Chrome('C://Users//omkar//Downloads//CS242//jobSearchEngine-CS242-//chromedriver',options=options)  # Optional argument,
    divs = soup.find_all('div', class_ = 'base-card')
    for item in divs:
        title = item.find('a').text.strip()
        company = item.find('h4', class_ = 'base-search-card__subtitle').text.strip()
        try:
            salary = item.find('span', class_ = 'job-search-card__salary-info').text.strip()
        except:
            salary = ''
        location = item.find('span', class_ = 'job-search-card__location').text.strip()
        try:
            hiringStatus = item.find('span', class_ = 'result-benefits__text').text.strip()
        except:
            hiringStatus = ''
        postedDate = item.find('time', class_ = 'job-search-card__listdate')
        if postedDate:
          postedDate = postedDate.attrs['datetime']
        else:
          postedDate = ''
        try:
            joblink=item.find('a', class_ = 'base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]')['href']
            try:
                driver.get(joblink)
                time.sleep(5)
                html_content = driver.page_source
                posting_soup = BeautifulSoup(html_content, 'html.parser')
                jobDescription = posting_soup.find('div', {'class':"description__text description__text--rich"}).text.strip()
            except:
                jobDescription = ''
                print(joblink)
        except:
            joblink=''
            jobDescription=''
        
        if title == "" or company == ""  or hiringStatus == "" or postedDate == "":
            continue
    # try:
    #     jobDescription= item.find('div',class_= "decorated-job-posting__details").text.strip()
    # except:
    #     jobDescription= ''
        job = {
            'title' : title,
            'company': company,
            'salary' : salary,
            'location': location,
            'hiringStatus': hiringStatus,
            'postedDate' : postedDate,
            'joblink' : joblink,
            'jobDescription' : jobDescription
        }
        joblist.append(job)
    return 

def get_job_postings(positions):
    global joblist
    joblist = []
    for position in positions:
        print(position)
        page = 0
        while True: 
            c = extract(page,position)
            transform(c)
            page += 25
            if not c.find_all('div', class_ = 'base-card'):
                break
    df = pd.DataFrame(joblist)
    df.to_csv('linkedinJobs4.csv')
    return

# positions = ['software engineer', 'data scientist', 'machine learning engineer', 'artificial intelligence engineer', -p
# 'big data engineer', 'devops engineer', 'full stack developer', 'front end developer', -a
# 'backend developer', 'mobile developer', 'cybersecurity analyst', 'systems engineer', -p
# 'network engineer', 'database administrator', 'product manager', 'program manager', -a
# 'project manager', 'ux designer', 'ui designer', 'graphic designer', 'web designer',
# 'digital marketer', 'content creator', 'technical writer', 'product analyst', 'business analyst',
# 'data analyst', 'information security analyst', 'cloud solutions architect', 'embedded systems engineer',
# 'electrical engineer', 'mechanical engineer']
positions=['backend developer', 'mobile developer', 'cybersecurity analyst', 'systems engineer']
get_job_postings(positions)
