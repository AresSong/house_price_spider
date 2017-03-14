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




def clear_suburb(suburb_raw):
    suburb_cleared = suburb_raw
    return suburb_cleared

def clear_street(street_raw,city,suburb_mapping):
    lookup_street_no = 0
    while 1 == 1:
        lookup_street_no = street_raw.find(" ", lookup_street_no + 1)
        print(lookup_street_no)
        sub_property_address = street_raw[lookup_street_no:]
        if number.search(sub_property_address) is None:
            street_number_cleared = street_raw[0:lookup_street_no].strip().replace("-", "/").replace(" ", "")
            street_name_cleared = street_raw[lookup_street_no:].replace(city, "").strip()
            break
        else:
            continue
    ## remove flat from beginning of street no
    street_number_cleared = street_number_cleared.replace("Flat","").replace("flat","")

    suburb_mapping_cleared = suburb_mapping[suburb_mapping['Origin'] != suburb_mapping['Mapped']]

    for index, row in suburb_mapping_cleared.iterrows():
        if street_name_cleared.endswith(row["Origin"]):
            street_name_cleared = street_name_cleared.replace(row["Origin"],row["Mapped"])

    return  street_number_cleared, street_name_cleared

def clear_city(city_raw,suburb_list):
    city_cleared = 'dunedin'
    for i in suburb_list:
        if city_raw.find(i) >= 0 and city_raw.find("dunedin") == -1:
            city_cleared = ''
            break
    return  city_cleared

def unify_address(property_address_raw, suburb_mapping):
    property_address = property_address_raw.lower()
    street_no = ""
    street_name = ""
    suburb = ""
    city = ""
    postcode = ""

    street_no_unified = ''
    street_name_unified = ''
    suburb_unified = ''
    city_unified = ''
    postcode_unified = ''

    city = clear_city(property_address, suburb_mapping["Origin"].values.tolist()) #return "" when there is suburb in street name
    street_no, street_name = clear_street(property_address,city,suburb_mapping)

    search_prefix = r'https://www.nzpost.co.nz/tools/address-postcode-finder/suggest/'
    search_space = r'%20'
    search_address = street_no + search_space + street_name + search_space + suburb + search_space + city
    search_string = search_prefix + search_address
    search_string = search_string.replace(' ', search_space)
    print(search_string)

    driver = webdriver.PhantomJS(executable_path=r'C:\Users\hosxh\Documents\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    driver.get(search_string)
    pageSource = driver.page_source
    bsObj = BeautifulSoup(pageSource, "html.parser")
    driver.close()

    if (bsObj.find("div", {"class": "suggestion"}) is not None and bsObj.find("div", {"class": "suggestion"}).text.find(
            'is not a complete address') > 0):
        ## has multiple suggestions
        address_temp = ''
        # print("multiple")
        address_temp = bsObj.find("div", {"class": "suggestion"}).ul.li.text.strip()
        street_no_unified = address_temp.split(",")[0].split(" ")[0].strip()
        street_name_unified = " ".join(address_temp.split(",")[0].split(" ")[1:]).strip()
        # print(address_temp)
        # print(city)
        if city != "": ## city == "" when address has suburb

            suburb_unified = address_temp.split(",")[1].strip()
            city_unified = address_temp.split(",")[2].split(" ")[1].strip()
            postcode_unified = r_postcode.findall(address_temp)[0]
        else:
            # print(address_temp)
            city_unified = "Dunedin" ## hardcode
            suburb_unified = address_temp.split(",")[1].strip()
            postcode_unified = r_postcode.findall(address_temp)[0] #address_temp.split(",")[2].split(" ")[2].strip()
        # print(bsObj.find("div", {"class": "suggestion"}).ul.li.text)
    elif (bsObj.find("div", {"class": "suggestion"}) is not None and bsObj.find("div", {"class": "suggestion"}).text.find(
            'is not a complete address') == -1 ):
        ## don't have a suggested address
        street_no_unified = ''
        street_name_unified = ''
        suburb_unified = ''
        city_unified = ''
        postcode_unified = ''
    else:
        ## has one suggestion
        # print("single")
        # print(city)
        if city  != "":
            count_address = 1
            for i in bsObj.find("p", {"class": "address-label-postal"}).contents:
                if str(type(i)) != "<class 'bs4.element.NavigableString'>":
                    if count_address == 2:
                        street_no_unified = (i.text.strip().split()[0])
                        street_name_unified = " ".join((i.text.strip().split()[1:]))
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
        else:

            city_unified = "Dunedin"  ## hardcode
            count_address = 1
            for i in bsObj.find("p", {"class": "address-label-postal"}).contents:
                if str(type(i)) != "<class 'bs4.element.NavigableString'>":
                    if count_address == 2:
                        street_no_unified = (i.text.strip().split()[0])
                        street_name_unified = " ".join((i.text.strip().split()[1:]))
                        # print("street: " + i.text)
                    elif count_address == 4:
                        # print(i.text)
                        suburb_unified = i.text.strip()
                count_address = count_address + 1
            postcode_unified = bsObj.find("p", {"class": "h2 postcode"}).text.strip()



    return property_address_raw,street_no_unified,street_name_unified,suburb_unified,city_unified,postcode_unified

## trademe Flat 9/19 Sheen Street
## trademe 65A+B Ascot Street
## trademe 46G Truby King Drive, Karitane, Waikouaiti 9471

# property_address = "45 Campbells Road Dunedin"
# property_address = "1 - 114 Harbour Terrace Dunedin"
# property_address = "1 Forrester Avenue Dunedin"
# property_address = "65A Ascot Street"
# property_address =  "1 Queen Street Mosgiel"
# property_address = "Flat 9/19 Sheen Street"


property_address = "ROW Russell Street Dunedin"
property_address = "1 - 100 Argyle Street Mosgiel"
property_address = "1 - 111 Balmacewen Road Dunedin"
property_address = "1 - 114 Harbour Terrace Dunedin"
# property_address = "1 - 118 Carroll Street Dunedin"
# property_address =  "ROW Russell Street Dunedin"
# property_address =  "14 Weka Street Saint Leonards"
# property_address ="18 Weka Street St Leonards"
property_address = "1/4 Elliffe Place Dunedin"
# property_address = property_address.lower()

number = re.compile(r"[0-9]+")
r_postcode = re.compile(r"[0-9]{4}")
alpha = re.compile(r"[0-9]+")

## testing
# engine = create_engine(r"mssql+pyodbc://sa:123@localhost")
# suburb_mapping = pd.read_sql(r"SELECT * FROM [dbo].[suburb_mapping]",engine)
# print(unify_address(property_address,suburb_mapping))
##


def unify_address_pandas(property_address, *args):
    suburb_mapping = args[0]
    try:
        unify_address_list = unify_address(property_address, suburb_mapping)
    except:
        unify_address_list = (property_address, '', '', '', '', '')
    # unify_address_list = unify_address(property_address, suburb_mapping)
    print(unify_address_list)
    return unify_address_list