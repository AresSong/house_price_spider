from urllib.request import urlopen
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from pprint import pprint
import re
from urllib.error import HTTPError
import time
from datetime import datetime
import json
import codecs
from sqlalchemy import create_engine

url = r"http://www.tki.org.nz/Schools/(page)/search-results?schoolName=&regionId=14&schoolTypeId=&schoolAuthId=&genderId=&medium=&boarding=&Search=Search"
url_prefix = r"http://www.tki.org.nz"
schools_general = list()
search_pages = set()
engine = create_engine(r"mssql+pyodbc://sa:123@localhost")

search_pages.add(url)

try:
    # html = urlopen(r"")
    html = urlopen(url)
except HTTPError as e:
    pass

bsObj = BeautifulSoup(html.read(), "html.parser")

## load urls of search pages
for a in bsObj.find("p", {"class": "page-list"}).find_all("a"):
    if  a.get("href").strip() != "" and a.get("href").strip() is not None:
        search_pages.add(url_prefix + a.get("href"))

## load all pages of search results
for page in search_pages:
    try:
        # html = urlopen(r"")
        html = urlopen(page)
    except HTTPError as e:
        pass
    bsObj = BeautifulSoup(html.read(), "html.parser")
    for school in bsObj.find_all("div", {"class": "findSchoolSearchResult"}):
        school_general = dict()
        # print(school.h3.a.get("href"))
        # print(school.h3.a.text)
        school_general["name"] = school.h3.a.text
        school_general["tki_url"] = url_prefix + school.h3.a.get("href").strip()
        for i in school.findChildren():
            if str(type(i)) != "<class 'bs4.element.NavigableString'>":
                if i.text.find("Address") >= 0:
                    school_general["address"] = i.text.strip()
                elif i.text.find("Type") >= 0:
                    school_general["type"] = i.text.strip()
                elif i.text.find("Gender") >= 0:
                    school_general["gender"] = i.text.strip()
                elif i.text.find("PHONE") >= 0:
                    school_general["phone"] = i.text.strip()
                elif i.text.find("EMAIL") >= 0:
                    school_general["email"] = i.text.strip()
                elif i.text.find("WEBSITE") >= 0:
                    school_general["website"] = i.text.strip()

        schools_general.append(school_general)
    #print(school)

pprint(schools_general)
pd.DataFrame(schools_general).to_sql(name="load_schools_general", con=engine, if_exists="append")

# ## load school details
schools_detail = list()
for school_general in schools_general:
    school_detail = dict()
    try:
        # html = urlopen(r"")
        html = urlopen(school_general["tki_url"])
    except HTTPError as e:
        pass
    bsObj = BeautifulSoup(html.read(), "html.parser")
    school_detail["decile"] = bsObj.find("span", {"id": "schoolDecile"}).text.strip()
    school_detail["authority"] = bsObj.find("span", {"id": "schoolAuthority"}).text.strip()
    school_detail["name"] = school_general["name"]

    schools_detail.append(school_detail)

pprint(schools_detail)
pd.DataFrame(schools_detail).to_sql(name="load_schools_detail", con=engine, if_exists="append")

## load schools population
schools_population = list()
for school in schools_general:
    school_population = pd.DataFrame()
    population_url = str(school["tki_url"]).replace("school?school","school/population/trends?school")
    #population_url = 'https://www.tki.org.nz/Schools/(page)/school/population/trends?school=3745&district=71&region=14'
    school_population = pd.read_html(population_url)[0]
    school_population["name"] = school["name"]
    school_population["population_url"] = population_url
    school_population.to_sql(name="load_schools_population", con=engine, if_exists="append")
    schools_population.append(school_population)

pprint(schools_population)
# pd.DataFrame(schools_population).to_sql(name="load_schools_population", con=engine, if_exists="append")

## load national standards
schools_national_standards = list()
for school in schools_general:
    school_national_standard = pd.DataFrame()
    column_name = ["category","well_below_no","well_below_percentage","below_no","below_percentage","at_no","at_percentage","above_no","above_percentage"]
    ## reading
    reading_url = str(school["tki_url"]).replace("school?school", "school/national/reading?school")
    #reading_url = "https://www.tki.org.nz/Schools/(page)/school/national/reading?school=3745&district=71&region=14"
    ##high school
    try:
        pd.read_html(reading_url)
    except ValueError as e:
        continue

    reading = pd.read_html(reading_url)[0]
    reading = reading.iloc[:,0:9]
    reading.columns = column_name
    reading["type"] = "reading"
    reading["name"] = school["name"]
    print(reading)
    ## writing
    writing_url = str(school["tki_url"]).replace("school?school", "school/national/writing?school")
    #writing_url = r"https://www.tki.org.nz/Schools/(page)/school/national/writing?school=3745&district=71&region=14"
    writing = pd.read_html(writing_url)[0]
    writing = writing.iloc[:,0:9]
    writing.columns = column_name
    writing["type"] = "writing"
    writing["name"] = school["name"]
    print(writing)
    ## mathematics
    mathematics_url = str(school["tki_url"]).replace("school?school", "school/national/writing?school")
    ## testing url
    # mathematics_url = r"https://www.tki.org.nz/Schools/(page)/school/national/mathematics?school=3745&district=71&region=14"
    mathematics = pd.read_html(mathematics_url)[0]
    mathematics = mathematics.iloc[:, 0:9]
    mathematics.columns = column_name
    mathematics["type"] = "mathematics"
    mathematics["name"] = school["name"]
    print(mathematics)
    #population_url = 'https://www.tki.org.nz/Schools/(page)/school/population/trends?school=3745&district=71&region=14'
    #school_population = pd.read_html(population_url)[0]
    #school_population["name"] = school["name"]
    #school_population["population_url"] = population_url
    reading.to_sql(name="load_schools_national_standards", con=engine, if_exists="append")
    writing.to_sql(name="load_schools_national_standards", con=engine, if_exists="append")
    mathematics.to_sql(name="load_schools_national_standards", con=engine, if_exists="append")
    schools_national_standards.append(reading)
    schools_national_standards.append(writing)
    schools_national_standards.append(mathematics)
    # break
pprint(schools_national_standards)
#pd.DataFrame(schools_national_standards).to_sql(name="load_schools_national_standards", con=engine, if_exists="append")


