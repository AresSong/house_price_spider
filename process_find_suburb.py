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
import glob
import os
from sqlalchemy import create_engine
import pyodbc




#Retrieve HTML string from the URL
#html = urlopen("http://www.pythonscraping.com/exercises/exercise1.html")

#addresses = pd.DataFrame(columns = ['street_no','street','city','suburb','postcode'])
addresses = list()

property_address = "45 Campbells Road Dunedin"
property_address = "1 - 114 Harbour Terrace Dunedin"
#property_address = "1 Forrester Avenue Dunedin"
street_no = ""
street_name = ""
suburb = ""
city = 'Dunedin'
postcode = ""

number = re.compile(r"[0-9]+")
alpha = re.compile(r"[0-9]+")

lookup_street_no = 0
while 1 == 1:
    lookup_street_no = property_address.find(" ",lookup_street_no+1)
    sub_property_address = property_address[lookup_street_no:]
    if number.search(sub_property_address) is None:
        street_no = property_address[0:lookup_street_no].strip().replace("-","/").replace(" ","")
        street_name = property_address[lookup_street_no:].replace(city,"").strip()
        break
    else:
        continue

print(street_no)
print(street_name)
full_street =  street_no + ' ' + street_name

#address = r'https://www.nzpost.co.nz/tools/address-postcode-finder/suggest/112%20Pine%20Hill%20Road%20Dunedin'
search_prefix = r'https://www.nzpost.co.nz/tools/address-postcode-finder/suggest/'
search_space = r'%20'
search_address = street_no + search_space + street_name + search_space + city
search_string = search_prefix + search_address
search_string = search_string.replace(' ',search_space)


print(search_string)

try:
    html = urlopen(search_string)
except HTTPError as e:
    pass

bsObj = BeautifulSoup(html.read(), "html.parser")

#print(html.read())
#print(bsObj.html)
time.sleep(10)

print(bsObj)

if (bsObj.find("div", { "class" : "suggestion" }) is not None and bsObj.find("div", { "class" : "suggestion" }).text.find('is not a complete address') > 0 )  :
    pass
    # for i in bsObj.findAll('a', href=True):
    #     print(i['href'])
else:
    count_address = 1
    for i in bsObj.find("p", {"class": "address-label-postal"}).contents:
        if str(type(i)) == "<class 'bs4.element.NavigableString'>":
            #print(i)
            if count_address == 1:
                pass
            elif count_address == 2:
                suburb = i.strip()
            elif count_address == 3:
                postcode = i.replace(city,"").strip()
            count_address = count_address + 1
        # print(count_address)
        # print(i)
        # print(type(i))

    # addresses.append(address)

print(street_no)
print(street_name)
print(suburb)
print(city)
print(postcode)

# addresses_pd = pd.DataFrame(addresses,columns = ['street_no','street','city','suburb','postcode'] )
#
# pprint(addresses_pd)
# addresses_pd.to_csv('C:\\Users\\ares\\PycharmProjects\\house_price_spider\\tst.csv')