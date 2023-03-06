from bs4 import BeautifulSoup
import requests
import csv
from itertools import zip_longest

page = 1
while True:
    html = requests.get(f'https://www.timesjobs.com/candidate/job-search.html?from=submit&actualTxtKeywords=data%20engineer&searchBy=0&rdoOperator=OR&searchType=personalizedSearch&txtLocation=morocco&luceneResultSize=25&postWeek=60&txtKeywords=data%20engineer&pDate=I&sequence={page}&startPage=1').text
    soup = BeautifulSoup(html, 'lxml')

    if (page > int(soup.find('span', id="totolResultCountsId").text) // 25):
        print("End of pages!")
        break

    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
    for job in jobs:
        company = job.find('h3', class_='joblist-comp-name').text.replace(job.find('span', class_='comp-more').text , '').strip()
        job_title = job.find('h2').find('a').text.strip()
        skills = job.find('span', class_='srp-skills').text.strip()
        mobility = job.find('span', class_='jobs-status covid-icon clearfix').text.strip()
        location = job.find('ul', class_='top-jd-dtl clearfix').find('span').text.strip()
        price = job.find('ul', class_='top-jd-dtl clearfix').findAll('li')[1].text.strip()
        more = job.header.a['href']
        ml = mobility + ' : ' + location
        '''
        print(company)
        print(job_title)
        print(skills)
        print(mobility + ' : ' + location)
        print(price)
        print(more)
        print("------------------")
        '''
        list = [company, job_title, skills, ml, price, more]
        exported = zip_longest(*list)
        with open(r'WebScraping/csv_file.csv', 'w', encoding='utf-8') as f:
            wr = csv.writer(f)
            wr.writerow(["company", "job title", "skills", "mobility and location", "price", "more"])
            wr.writerows(exported)

    page = page+1
    print("**Page switched**")
