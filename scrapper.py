from bs4 import BeautifulSoup
import requests
import csv
from itertools import zip_longest
import time

#initialize colomuns
companies = []
job_titles = []
skillss = []
mls = []
prices = []
mores = []
page = 1
while True:
    # request the page and get html
    html = requests.get(f'https://www.timesjobs.com/candidate/job-search.html?from=submit&actualTxtKeywords=Data%20Analyst&searchBy=0&rdoOperator=OR&searchType=personalizedSearch&luceneResultSize=25&postWeek=60&txtKeywords=0DQT0data%20analyst0DQT0&pDate=I&sequence={page}&startPage=1').text
    soup = BeautifulSoup(html, 'lxml')
    # go through all pages
    if (page > int(soup.find('span', id="totolResultCountsId").text) // 25):
        print("End of pages!")
        break

    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
    #exceptions here are an exemple to avoid some errors
    for job in jobs:
        company_ex = job.find('h3', class_='joblist-comp-name').text
        try:
            company = company_ex.replace(job.find('span', class_='comp-more').text , '').strip()
            companies.append(company)

        except AttributeError:
            companies.append(company_ex)
        job_title = job.find('h2').find('a').text.strip()
        job_titles.append(job_title)
        skills = job.find('span', class_='srp-skills').text.strip()
        skillss.append(skills)
        try:
            mobility = job.find('span', class_='jobs-status covid-icon clearfix').text.strip()
            location = job.find('ul', class_='top-jd-dtl clearfix').find('span').text.strip()
            ml = mobility + ' : ' + location
            mls.append(ml)
        except AttributeError:
            mobility = "Not specified"
            location = job.find('ul', class_='top-jd-dtl clearfix').find('span').text.strip()
            ml = mobility + ' : ' + location
            mls.append(ml)
        price = job.find('ul', class_='top-jd-dtl clearfix').findAll('li')[1].text.strip()
        prices.append(price)
        more = job.header.a['href']
        mores.append(more)

        # export to csv
        head = ["company", "job title", "skills", "mobility and location", "price", "more"]
        list = [companies, job_titles, skillss, mls, prices, mores]
        exported = zip_longest(*list)
        with open(r'WebScraping/csv_file.csv', 'w', encoding='utf-8') as f:
            wr = csv.writer(f, delimiter=";")
            wr.writerow(head)
            wr.writerows(exported)
    # switch pages
    page = page+1
    print("**Page switched**")
    # avoid being detected
    time.sleep(60)

