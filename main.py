from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd

url = "https://www.glassdoor.com/Salaries/software-engineer-salary-SRCH_KO0,17.htm"
all_salaries = []

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

def get_url_and_salaries_list(url):
    soup = get_soup(url)
    next_url = find_next_page_url(soup)
    salaries_list = find_all_salaries(soup) 
    return (next_url, salaries_list)

for i in range(500):
    print("Request number: ", i)
    next_url, salaries_list = get_url_and_salaries_list(url)
    url = next_url
    all_salaries.extend(salaries_list)

print(all_salaries)