from urllib.request import urlopen
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from pprint import pprint
import re
from urllib.error import HTTPError
from selenium import webdriver
import time
from datetime import datetime
import json
import codecs

listings = list()


#Retrieve HTML string from the URL

url = r"http://www.realestate.co.nz/residential/all/otago/dunedin-city"
url_prefix = r'http://www.realestate.co.nz'


url_listings = list()

while(1 == 1):
    try:
        # html = urlopen(r"")
        html = urlopen(url)
    except HTTPError as e:
        pass

    bsObj = BeautifulSoup(html.read(), "html.parser")

    for title in bsObj.find_all("div",{"class":"listDescription"}):
        #print(title.a.get('href'))
        url_listings.append(url_prefix + title.h3.a.get('href'))
        #count = count + 1

    #print(count)

    if bsObj.find('a',{"class":"linkButton brandColour alignRight"}, href=True) is None:
        #print('No next page')
        break
    else:
        url = url_prefix + bsObj.find('a', {"class": "linkButton brandColour alignRight"}, href=True).get('href')

pprint(url_listings)
print(len(url_listings))

count = 1 # only use for testing

for url_listing in url_listings:
    listing = dict()
    # url_listing = r'http://www.realestate.co.nz/2911775'
    try:
        # html = urlopen(r"")
        html_listing = urlopen(url_listing)
    except HTTPError as e:
        pass

    bsObj_listing = BeautifulSoup(html_listing.read(), "html.parser")

    ##title block
    title = ''
    price = ''
    listed_datetime = ''
    title = bsObj_listing.find("div",{"class":"headerDetails listDetailsHead"}).h1.text.strip()
    price = bsObj_listing.find("div",{"class":"headerDetails listDetailsHead"}).h2.text.strip()
    listed_datetime = bsObj_listing.find("div",{"class":"headerDetails listDetailsHead"}).h4.text.strip()
    listed_datetime = listed_datetime[listed_datetime.find("Listed"):]
    address_count = 1
    street = ''
    suburb = ''
    for t in bsObj_listing.find("div",{"class":"headerDetails listDetailsHead"}).h3.children:
        if str(type(t)) != "<class 'bs4.element.NavigableString'>":
            if address_count == 1:
                street = t.text.strip()
            elif address_count == 2:
                suburb = t.text.strip()
            address_count = address_count + 1

    ##agent part
    seller = ''
    seller = bsObj_listing.find("div",{"class":"topRight agencyDetailsBox"}).h5.text.strip()

    ##house attribute
    bedrooms = ''
    bathrooms = ''
    landArea  = ''
    carParks = ''
    floorArea = ''
    ensuites = ''
    property_type = ''
    property_type = bsObj_listing.find("div", {"class": "sideKeyFeatures"}).h4.text.strip()
    for h in bsObj_listing.find("div",{"class":"sideKeyFeatures"}).descendants:
        if str(type(h)) != "<class 'bs4.element.NavigableString'>" and h.get("class") is not None:
            if len(h.get("class")) == 1:
                if h.get("class")[0] == "bedrooms":
                    bedrooms = h.text.strip()
                elif h.get("class")[0] == "bathrooms":
                    bathrooms = h.text.strip()
                elif h.get("class")[0] == "landArea":
                    landArea = h.text.strip()
                elif h.get("class")[0] == "carParks":
                    carParks = h.text.strip()
                elif h.get("class")[0] == "floorArea":
                    floorArea = h.text.strip()
                elif h.get("class")[0] == "ensuites":
                    ensuites = h.text.strip()

    ##property_description
    property_description = ''
    property_description = bsObj_listing.find("div",{"class":"description detailsPage"}).text

    ##snapshot_datetime
    snapshot_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    listing["snapshot_datetime"] = snapshot_datetime
    listing["bedrooms"] = bedrooms
    listing["bathrooms"] = bathrooms
    listing["landArea"] = landArea
    listing["carParks"] = carParks
    listing["floorArea"] = floorArea
    listing["street"] = street
    listing["suburb"] = suburb
    listing["title"] = title
    listing["price"] = price
    listing["listed_datetime"] = listed_datetime
    listing["url"] = url_listing
    listing["seller"] = seller
    listing["ensuites"] = ensuites
    listing["property_type"] = property_type
    listing["property_description"] = property_description

    listings.append(listing)
    print(count)
    print(url_listing)
    count = count + 1
    # if count >= 3:
    #     break

pprint(listings)
pprint(len(listings))

# print(bedrooms)
# print(bathrooms)
# print(landArea)
# print(carParks)
# print(floorArea)
# print(street)
# print(suburb)
# print(title)
# print(price)
# print(listed_datetime)



filename = 'RealEstate_listing_' +  datetime.now().strftime("%Y_%m_%d") + '.txt'

with codecs.open(filename, 'w') as f:
    for i in listings:
        f.write(json.dumps(i) + "\n")

# pprint("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# pprint("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# pprint("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# pprint("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# pprint("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# pprint("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# pprint("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

#pprint(listings)