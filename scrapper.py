from bs4 import BeautifulSoup
import requests

html = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=data+engineer&txtLocation=morocco').text
soup = BeautifulSoup(html, 'lxml')

jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
for job in jobs:
    company = job.find('h3', class_='joblist-comp-name').text.replace(job.find('span', class_='comp-more').text , '').strip()
    job_title = job.find('h2').find('a').text.strip()
    skills = job.find('span', class_='srp-skills').text.strip()
    mobility = job.find('span', class_='jobs-status covid-icon clearfix').text.strip()
    location = job.find('ul', class_='top-jd-dtl clearfix').find('span').text.strip()
    price = job.find('ul', class_='top-jd-dtl clearfix').findAll('li')[1].text.strip()

    print(company)
    print(job_title)
    print(skills)
    print(mobility + ' : ' + location)
    print(price)
    print("------------------")
