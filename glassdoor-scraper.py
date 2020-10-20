'''
Web scraper to get the salaries of Software Engineers using Glassdoor website.
Change the num_requests variable as per how many values you want. One request gives
20 values. Note that the website will give occasional errors because we are sending 
continuous requests.
'''

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd

url = "https://www.glassdoor.com/Salaries/software-engineer-salary-SRCH_KO0,17.htm"
num_requests = 200

def get_soup(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req)
    bs = BeautifulSoup(webpage.read(),'html.parser')
    return bs

def find_next_page_url(bs):
    next_page = bs.find("a", "pagination__ArrowStyle__nextArrow")
    next_page_link = str(next_page['href'])
    return next_page_link

def find_all_salaries(bs):
    salaries = bs.find_all("p", { "class" : "d-block d-md-none m-0" })
    salaries_list = []
    for tag in salaries:
        salary = str(tag.find("strong").contents)
        salaries_list.append(salary[2:-2])
        # print(salary[2:-2])
    return salaries_list

def get_url_and_salaries_list(url, writer):
    soup = get_soup(url)
    next_url = find_next_page_url(soup)
    salaries_list = find_all_salaries(soup) 
    for salary in salaries_list:
        salary_split = salary.split(",")
        salary  = "".join(salary_split)
        salary = salary[1:]
        writer.write(salary+"\n")
    return next_url

writer = open("sample_salaries_one.csv", "w")
writer.write("Salary\n")

for i in range(num_requests):
    print("Request number: ", i)
    next_url = get_url_and_salaries_list(url, writer)
    url = next_url

writer.close()
