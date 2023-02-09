import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract(page,position):
    headers = {'Users-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
    position = position.replace(" ","%20")
    url = f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={position}&location=United%20States&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start={page}'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup):
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
        if title == "" or company == ""  or hiringStatus == "" or postedDate == "":
            continue
        
        job = {
            'title' : title,
            'company': company,
            'salary' : salary,
            'location': location,
            'hiringStatus': hiringStatus,
            'postedDate' : postedDate
        }
        joblist.append(job)
    return 

def get_job_postings(positions):
    global joblist
    joblist = []
    for position in positions:
        page = 0
        while True: 
            c = extract(page,position)
            transform(c)
            page += 25
            if not c.find_all('div', class_ = 'base-card'):
                break
    df = pd.DataFrame(joblist)
    df.to_csv('linkedinJobs.csv')
    return

positions = ['software engineer', 'data scientist', 'machine learning engineer', 'artificial intelligence engineer',
'big data engineer', 'devops engineer', 'full stack developer', 'front end developer',
'backend developer', 'mobile developer', 'cybersecurity analyst', 'systems engineer',
'network engineer', 'database administrator', 'product manager', 'program manager',
'project manager', 'ux designer', 'ui designer', 'graphic designer', 'web designer',
'digital marketer', 'content creator', 'technical writer', 'product analyst', 'business analyst',
'data analyst', 'information security analyst', 'cloud solutions architect', 'embedded systems engineer',
'electrical engineer', 'mechanical engineer']
get_job_postings(positions)
