from selenium import webdriver
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
import lxml
import re
import numpy as np
import pandas as pd
from sqlalchemy import create_engine


addresses = list()


## trademe Flat 9/19 Sheen Street
## trademe 65A+B Ascot Street
## trademe 46G Truby King Drive, Karitane, Waikouaiti 9471

property_address = "45 Campbells Road Dunedin"
property_address = "1 - 114 Harbour Terrace Dunedin"
property_address = "1 Forrester Avenue Dunedin"
property_address = "65A Ascot Street"
# property_address =  "1 Queen Street Mosgiel"
# property_address = "Flat 9/19 Sheen Street"

street_no = ""
street_name = ""
suburb = "" ##"Saint Kilda"
city = 'Dunedin'
postcode = ""

street_no_unified = ''
street_name_unified = ''
suburb_unified = ''
city_unified = ''
postcode_unified = ''

number = re.compile(r"[0-9]+")
alpha = re.compile(r"[0-9]+")

def suburb_clear(suburb_raw):
    suburb_cleared = suburb_raw
    return suburb_cleared

def street_clear(street_raw):
    lookup_street_no = 0
    while 1 == 1:
        lookup_street_no = street_raw.find(" ", lookup_street_no + 1)
        sub_property_address = street_raw[lookup_street_no:]
        if number.search(sub_property_address) is None:
            street_number_cleared = street_raw[0:lookup_street_no].strip().replace("-", "/").replace(" ", "")
            street_name_cleared = street_raw[lookup_street_no:].replace(city, "").strip()
            break
        else:
            continue
    ## remove flat from beginning of street no
    street_number_cleared = street_number_cleared.replace("Flat","").replace("flat","")

    return  street_number_cleared, street_name_cleared

engine = create_engine(r"mssql+pyodbc://sa:123@localhost")
suburb_mapping = pd.read_sql(r"SELECT * FROM [dbo].[suburb_mapping]",engine)

print(street_clear(property_address))
street_no, street_name = street_clear(property_address)


##format
# lookup_street_no = 0
# while 1 == 1:
#     lookup_street_no = property_address.find(" ",lookup_street_no+1)
#     sub_property_address = property_address[lookup_street_no:]
#     if number.search(sub_property_address) is None:
#         street_no = property_address[0:lookup_street_no].strip().replace("-","/").replace(" ","")
#         street_name = property_address[lookup_street_no:].replace(city,"").strip()
#         break
#     else:
#         continue

print(street_no)
print(street_name)
full_street =  street_no + ' ' + street_name

#address = r'https://www.nzpost.co.nz/tools/address-postcode-finder/suggest/112%20Pine%20Hill%20Road%20Dunedin'
search_prefix = r'https://www.nzpost.co.nz/tools/address-postcode-finder/suggest/'
search_space = r'%20'
search_address = street_no + search_space + street_name + search_space+ suburb + search_space + city
search_string = search_prefix + search_address
search_string = search_string.replace(' ',search_space)
print(search_string)

driver = webdriver.PhantomJS(executable_path=r'C:\Users\hosxh\Documents\phantomjs-2.1.1-windows\bin\phantomjs.exe')
driver.get(search_string)
# time.sleep(2)
#print(driver.find_element_by_id("content").text)
pageSource = driver.page_source
bsObj = BeautifulSoup(pageSource, "html.parser")


if (bsObj.find("div", { "class" : "suggestion" }) is not None and bsObj.find("div", { "class" : "suggestion" }).text.find('is not a complete address') > 0 )  :
    ## has multiple suggestions
    address_temp = ''
    address_temp = bsObj.find("div", {"class": "suggestion"}).ul.li.text.strip()
    street_no_unified = address_temp.split(",")[0].split(" ")[0].strip()
    street_name_unified = " ".join(address_temp.split(",")[0].split(" ")[1:]).strip()
    suburb_unified = address_temp.split(",")[1].strip()
    city_unified = address_temp.split(",")[2].split(" ")[1].strip()
    postcode_unified = address_temp.split(",")[2].split(" ")[2].strip()
    # print(bsObj.find("div", {"class": "suggestion"}).ul.li.text)
else:
    ## has one suggestion
    count_address = 1
    for i in bsObj.find("p", {"class": "address-label-postal"}).contents:
        if str(type(i)) != "<class 'bs4.element.NavigableString'>":
            if count_address == 2:
                street_no_unified = (i.text.strip().split()[0])
                street_name_unified = (i.text.strip().split()[1])
                # print("street: " + i.text)
            elif count_address == 4:
                suburb_unified = i.text.strip()
                # print("suburb: " + i.text)
                # suburb = i.strip()
            elif count_address == 5:
                city_unified = i.text.split()[0]
                postcode_unified = i.text.split()[1]
                # print(i.text.split())
                # postcode = i.replace(city,"").strip()
        count_address = count_address + 1
driver.close()

print("result: ")
print(street_no_unified)
print(street_name_unified)
print(suburb_unified)
print(city_unified)
print(postcode_unified)
