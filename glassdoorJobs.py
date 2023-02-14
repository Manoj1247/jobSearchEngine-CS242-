from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def extract(page, job_position):
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
    global joblist
    company_name = []
    job_title = []
    location = []
    salaryRange = []
    postedDate = []
    jobLink = []
    jobDescription = []
    options = Options()
    # options.add_argument("--disable-extensions")
    # options.add_argument("--disable-gpu")
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options,
                              executable_path='/Users/manankumar/Documents/GitHub/jobSearchEngine-CS242-/chromedriver')  # Optional argument,
    # Optional argument,

    # Define the URL to scrape
    url = 'https://www.glassdoor.com/Job/united-states-' + job_position + '-jobs-SRCH_IL.0,13_IN1_KO14,' + str(
        14 + len(job_position) + 4) + '_IP' + str(page) + '.htm?'

    # Navigate to the URL
    driver.get(url)

    # Get the HTML content of the page
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    # if page==29:
    #   print(soup.prettify())
    for company in soup.findAll('div', {'class': 'd-flex justify-content-between align-items-start'}):
        company_name.append(company.a.text.strip())

    for job in soup.findAll('a', {'class': 'jobLink css-1rd3saf eigr9kq2'}):
        job_title.append(job.span.text.strip())
        try:
            url2 = 'https://www.glassdoor.com/' + job['href']
        except:
            url2 = ''
        jobLink.append(url2)

    for loc in soup.findAll('div', {'class': 'd-flex flex-wrap css-11d3uq0 e1rrn5ka2'}):
        location.append(loc.span.text.strip())

    for sal in soup.findAll('div', {'class': "css-3g3psg pr-xxsm"}):
        salary = sal.span.text.strip()
        salaryRange.append(salary.split(" (")[0])

    for date in soup.findAll('div', {'class': 'd-flex align-items-end pl-std css-1vfumx3'}):
        age_string = date.text.strip()
        if 'd+' in age_string:
            posted_date = datetime.now() - timedelta(days=int(age_string.split('d')[0]))
        if 'h' in age_string:
            posted_date = datetime.now()
        else:
            posted_date = datetime.now() - timedelta(days=int(age_string.split('d')[0]))
        postedDate.append(posted_date.strftime("%Y-%m-%d"))

    hiringStatus = ['Actively Hiring' for _ in range(len(job_title))]
    for url2 in jobLink:
        if len(url2):
            try:
                driver.get(url2)
                time.sleep(5)
                html_content = driver.page_source
                posting_soup = BeautifulSoup(html_content, 'html.parser')

                description = posting_soup.find('div', {'class': "desc css-58vpdc ecgq1xb5"}).text
            except:
                description = ''
                print(url2)
        else:
            description = ''
        jobDescription.append(description)

    joblist = list(
        zip(job_title, company_name, salaryRange, location, hiringStatus, postedDate, jobLink, jobDescription))
    return joblist


def scrape_data():
    page = 1
    global result
    result = []
    #job_positions = ['software-developer']
    job_positions= ['Human resources manager, information technology manager, marketing manager, sales manager, administrative assistant']
    # 'big data engineer', 'devops engineer', 'full stack developer', 'front end developer',
    # 'backend developer', 'mobile developer', 'cybersecurity analyst', 'systems engineer',
    # 'network engineer', 'database administrator']
    # 'product manager', 'program manager',
    # 'project manager', 'ux designer', 'ui designer', 'graphic designer', 'web designer',
    # 'digital marketer', 'content creator', 'technical writer', 'product analyst', 'business analyst',
    # 'data analyst', 'information security analyst', 'cloud solutions architect', 'embedded systems engineer',
    # 'electrical engineer', 'mechanical engineer']
    for job_position in job_positions:

        page = 1
        page_data = extract(page, job_position)
        while page_data:
            result.extend(page_data)
            page += 1
            page_data = extract(page, job_position)
            # time.sleep(3)

    return result


data = scrape_data()
# data=extract(1,'software-developer')
df = pd.DataFrame(data, columns=['title', 'company', 'salary', 'location', 'hiringStatus', 'postedDate', 'jobLink',
                                 'jobDescription'])
df.to_csv('glassdoorJobs.csv')