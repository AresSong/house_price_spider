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
testing_indicator = 0
search_pages.add(url)

## open initial search page
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


def load_school_general(url):
    try:
        # html = urlopen(r"")
        html = urlopen(url)
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

        return school_general

def load_school_detail(url):
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
    return school_detail

def load_school_population(url,sql_engine):
    school_population = pd.DataFrame()
    # population_url = 'https://www.tki.org.nz/Schools/(page)/school/population/trends?school=3745&district=71&region=14'
    school_population = pd.read_html(url)[0]
    school_population["name"] = school["name"]
    school_population["population_url"] = population_url
    school_population.to_sql(name="load_schools_population", con=sql_engine, if_exists="append")

## load all url and general info of school
for page in search_pages:
    schools_general.append(load_school_general(page))
    if testing_indicator == 1:
        break
pprint(schools_general)
pd.DataFrame(schools_general).to_sql(name="load_schools_general", con=engine, if_exists="append")

# ## load school details
schools_detail = list()
for school_general in schools_general:
    schools_detail.append(load_school_detail(school_general["tki_url"]))
    if testing_indicator == 1:
        break
pprint(schools_detail)
pd.DataFrame(schools_detail).to_sql(name="load_schools_detail", con=engine, if_exists="append")

## load schools population
for school in schools_general:
    population_url = str(school["tki_url"]).replace("school?school", "school/population/trends?school")
    load_school_population(population_url,engine)
    if testing_indicator == 1:
        break


def load_national_standard(url,sql_engine,table_no,column_name,type,school_name,table_name):
    try:
        loading_table = pd.read_html(reading_url)[table_no]
    except ValueError as e:
        pass
    loading_table = pd.read_html(reading_url)[table_no]
    loading_table = loading_table.iloc[:, 0:len(column_name)]
    loading_table.columns = column_name
    loading_table["type"] = type
    loading_table["name"] = school_name
    loading_table.to_sql(name=table_name, con=sql_engine, if_exists="append")

## load national standards
table_name = "load_schools_national_standards"
for school in schools_general:
    column_name = ["category","well_below_no","well_below_percentage","below_no","below_percentage","at_no","at_percentage","above_no","above_percentage"]

    ## reading
    reading_url = str(school["tki_url"]).replace("school?school", "school/national/reading?school")
    #reading_url = "http://www.tki.org.nz/Schools/(page)/school/national/reading?school=3745&district=71&region=14"
    load_national_standard(reading_url,engine,0,column_name,"reading",school["name"],table_name)

    ## writing
    writing_url = str(school["tki_url"]).replace("school?school", "school/national/writing?school")
    #writing_url = r"http://www.tki.org.nz/Schools/(page)/school/national/writing?school=3745&district=71&region=14"
    load_national_standard(writing_url, engine, 0, column_name, "writing", school["name"],table_name)

    ## mathematics
    mathematics_url = str(school["tki_url"]).replace("school?school", "school/national/writing?school")
    # mathematics_url = r"http://www.tki.org.nz/Schools/(page)/school/national/mathematics?school=3745&district=71&region=14"
    load_national_standard(mathematics_url, engine, 0, column_name, "mathematics", school["name"],table_name)
    if testing_indicator == 1:
        break
    # break

## load last three years national standards
table_name = "load_schools_national_standards_last_3_years"
for school in schools_general:
    column_name = ["category","2013_AtAbove_No","2013_AtAbove_percentage","2014_AtAbove_No"
                    ,"2014_AtAbove_percentage","2015_AtAbove_No","2015_AtAbove_percentage"]
    ## reading
    reading_url = str(school["tki_url"]).replace("school?school", "school/national/reading?school")
    # reading_url = "http://www.tki.org.nz/Schools/(page)/school/national/reading?school=3745&district=71&region=14"
    load_national_standard(reading_url, engine, 4, column_name, "reading", school["name"], table_name)

    ## writing
    writing_url = str(school["tki_url"]).replace("school?school", "school/national/writing?school")
    #writing_url = r"https://www.tki.org.nz/Schools/(page)/school/national/writing?school=3745&district=71&region=14"
    load_national_standard(writing_url, engine, 4, column_name, "writing", school["name"], table_name)

    ## mathematics
    mathematics_url = str(school["tki_url"]).replace("school?school", "school/national/mathematics?school")
    # mathematics_url = r"https://www.tki.org.nz/Schools/(page)/school/national/mathematics?school=3745&district=71&region=14"
    load_national_standard(mathematics_url, engine, 0, column_name, "mathematics", school["name"], table_name)

    if testing_indicator == 1:
        break

