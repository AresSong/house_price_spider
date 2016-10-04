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
#
url = r"http://www.trademe.co.nz/browse/categoryattributesearchresults.aspx?134=10&135=71&136=&153=&132=PROPERTY&49=0&49=0&122=0&122=0&29=&123=0&123=0&search=1&sidebar=1&cid=5748&rptpath=350-5748-"
url_prefix = r'http://www.trademe.co.nz'

count = 0

url_listings = list()

while(1 == 1):
    try:
        # html = urlopen(r"")
        html = urlopen(url)
    except HTTPError as e:
        pass

    bsObj = BeautifulSoup(html.read(), "html.parser")

    for title in bsObj.find_all("div",{"class":"property-card-title"}):
        #print(title.a.get('href'))
        url_listings.append(url_prefix + title.a.get('href'))
        #count = count + 1

    #print(count)

    if bsObj.find('a',{"rel":"next"}, href=True) is None:
        #print('No next page')
        break
    else:
        url = url_prefix + bsObj.find('a', {"rel": "next"}, href=True).get('href')

pprint(url_listings)

count = 1 # only use for testing

for url_listing in url_listings:
    listing = dict()
    #url_listing = r'http://www.trademe.co.nz/property/residential-property-for-sale/auction-1172952708.htm'
    #url_listing = r'http://www.trademe.co.nz/property/residential-property-for-sale/auction-1174147461.htm'
    #url_listing = r'http://www.trademe.co.nz/property/residential/sections-for-sale/auction-1122492054.htm'
    try:
        # html = urlopen(r"")
        html_listing = urlopen(url_listing)
    except HTTPError as e:
        pass

    bsObj_listing = BeautifulSoup(html_listing.read(), "html.parser")

    #pprint(str(bsObj_listing.find("li",{"id":"ListingTitle_titleTime"}).string).replace("Listed: ",""))

    attribute_key = None
    attribute_value = list()

    for listing_attribute in bsObj_listing.find("table",{"id":"ListingAttributes"}).children:
        if str(type(listing_attribute))  == "<class 'bs4.element.NavigableString'>":
            continue
        #print(type(listing_attribute))
        for i in listing_attribute.contents:
            if str(type(i)) != "<class 'bs4.element.NavigableString'>":
                for i_sub in i.contents: ###geting attributes of address
                    if i_sub.find("/>") == -1:
                        #print(i_sub.strip())
                        if attribute_key is None:
                            attribute_key = i_sub.strip()
                        else:
                            attribute_value.append(i_sub.strip())
        listing[attribute_key] = attribute_value
        attribute_key = None
        attribute_value = list()
        #print("------------------")

    listed_datetime_str =  str(bsObj_listing.find("li", {"id": "ListingTitle_titleTime"}).string).replace("Listed: ","")
    current_year = str(datetime.now().year)
    listed_datetime_datetime = datetime.strptime(listed_datetime_str + " " + current_year, "%a %d %b, %I:%M %p %Y")

    listing["listed_datetime"] =  listed_datetime_datetime.strftime("%Y-%m-%d %H:%M:%S")
    listing["url"] = url_listing

    if bsObj_listing.find("div",{"class":"Padding"}).h2.text.find("Advertiser") != -1:
        if  bsObj_listing.find("a",{"id":"ClassifiedActions_AgentsListingsLink"}) is not None and \
                        bsObj_listing.find("a",{"id":"ClassifiedActions_AgentsListingsLink"}).get('href').find("4332677") != -1 :
            listing["seller"] = "Colliers International"
        else:
            listing["seller"] = "private"
    elif bsObj_listing.find("div",{"class":"Padding"}).h2.text.find("Vendor") != -1:
        listing["seller"] = bsObj_listing.find("div", {"id": "ClassifiedActions_FirstAgentName"}).text
    else:
        listing["seller"] = bsObj_listing.find("div",{"id":"ClassifiedActions_AgencyName"}).text

    listing["snapshot_datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pprint(listing)
    listings.append(listing)
    # count = count + 1
    # if count>10:
    #     break

filename = 'trademe_listing_' +  datetime.now().strftime("%Y_%m_%d") + '.txt'

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