import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd

def extract(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
    url = f'https://www.glassdoor.com/Job/software-engineer-jobs-SRCH_KO0,17_IP{page}.htm?includeNoSalaryJobs=true&pgc=AB4AAIEAAAAAAAAAAAAAAAAAAffEJi8AAwAAAQAA'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    company_name = []
    for company in soup.findAll('div', {'class':'d-flex justify-content-between align-items-start'}):
        company_name.append(company.a.text.strip())
    
    job_title = []
    for job in soup.findAll('a', {'class':'jobLink css-1rd3saf eigr9kq2'}):
        job_title.append(job.span.text.strip())
    
    location = []
    for loc in soup.findAll('div', {'class': 'd-flex flex-wrap css-11d3uq0 e1rrn5ka2'}):
        location.append(loc.span.text.strip())
    
    salaryRange = []
    for sal in soup.findAll('div', {'class': "css-3g3psg pr-xxsm"}):
        salary = sal.span.text.strip()
        salaryRange.append(salary.split(" (")[0])
    
    postedDate = []
    for date in soup.findAll('div', {'class': 'd-flex align-items-end pl-std css-1vfumx3'}):
        age_string = date.text.strip()
        if 'd+' in age_string:
            posted_date = datetime.now() - timedelta(days=int(age_string.split('d')[0]))
        else:
            posted_date = datetime.now() - timedelta(days=int(age_string.split('d')[0]))
        postedDate.append(posted_date.strftime("%Y-%m-%d"))
        
    hiringStatus = ['Actively Hiring' for _ in range(len(job_title))]
    
    return list(zip(job_title, company_name, salaryRange, location, hiringStatus, postedDate))

def scrape_data():
    page = 1
    result = []
    while True:
        page_data = extract(page)
        if not page_data:
            break
        result.extend(page_data)
        page += 1
        
    return result


data = scrape_data()
df = pd.DataFrame(data, columns=['title', 'company', 'salary', 'location', 'hiringStatus', 'postedDate'])
df.to_csv('glassdoorJobs.csv')