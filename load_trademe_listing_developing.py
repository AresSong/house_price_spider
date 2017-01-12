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
from selenium import webdriver
import multiprocessing

PhantomJS_path = r"C:\Users\hosxh\Documents\phantomjs-2.1.1-windows\bin\phantomjs.exe"

url = r"http://www.trademe.co.nz/browse/categoryattributesearchresults.aspx?134=10&135=71&136=&153=&132=PROPERTY&49=0&49=0&122=0&122=0&29=&123=0&123=0&search=1&sidebar=1&cid=5748&rptpath=350-5748-"
url_prefix = r'http://www.trademe.co.nz'
file_folder = r'C:\Users\hosxh\Dropbox\housing_files\load_files\\'
driver = webdriver.PhantomJS(executable_path=PhantomJS_path)

listings = list()
count = 0

url_listings = list()

# pprint(url_listings)

def get_listing(url):
    global listings
    global count
    driver = webdriver.PhantomJS(executable_path=PhantomJS_path)
    listing = dict()
    driver.get(url)
    time.sleep(5)
    pageSource = driver.page_source
    bsObj_listing = BeautifulSoup(pageSource, "html.parser")

    table = bsObj_listing.find("table", {"id": "ListingAttributes"})

    table = str(table).replace("<br>", ";").replace("</br>", "")
    df = pd.read_html(table, flavor='bs4')[0]

    i_attrs = 0
    while i_attrs <= len(df) - 1:
        # print(df.loc[0,i_attrs])
        listing[df.loc[i_attrs, 0]] = df.loc[i_attrs, 1]
        i_attrs = i_attrs + 1

    listed_datetime_str = str(bsObj_listing.find("li", {"id": "ListingTitle_titleTime"}).string).replace("Listed: ", "")
    current_year = str(datetime.now().year)
    listed_datetime_datetime = datetime.strptime(listed_datetime_str + " " + current_year, "%a %d %b, %I:%M %p %Y")

    listing["listed_datetime"] = listed_datetime_datetime.strftime("%Y-%m-%d %H:%M:%S")
    listing["url"] = url

    if bsObj_listing.find("div", {"class": "Padding"}).h2.text.find("Advertiser") != -1:
        if bsObj_listing.find("a", {"id": "ClassifiedActions_AgentsListingsLink"}) is not None and \
                        bsObj_listing.find("a", {"id": "ClassifiedActions_AgentsListingsLink"}).get('href').find(
                            "4332677") != -1:
            listing["seller"] = "Colliers International"
        elif bsObj_listing.find("div", {"id": "ClassifiedActions_AgencyName"}) is not None:
            listing["seller"] = bsObj_listing.find("div", {"id": "ClassifiedActions_AgencyName"}).text.strip()
        else:
            listing["seller"] = "private"
    elif bsObj_listing.find("div", {"class": "Padding"}).h2.text.find("Vendor") != -1:
        listing["seller"] = bsObj_listing.find("div", {"id": "ClassifiedActions_FirstAgentName"}).text
    else:
        listing["seller"] = bsObj_listing.find("div", {"id": "ClassifiedActions_AgencyName"}).text

    listing["snapshot_datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    listing["Location:"] = str(listing["Location:"]).split(";")
    listings.append(listing)
    print(count)
    count = count + 1
    driver.close()

count = 1 # only use for testing

while (1 == 1):
    driver.get(url)
    time.sleep(5)
    pageSource = driver.page_source
    bsObj = BeautifulSoup(pageSource, "html.parser")

    for title in bsObj.find_all("div", {"class": "property-card-title"}):
        url_listings.append(url_prefix + title.a.get('href'))

    if bsObj.find('a', {"rel": "next"}, href=True) is None:
        break
    else:
        url = url_prefix + bsObj.find('a', {"rel": "next"}, href=True).get('href')

driver.close()

if __name__ == "__main__":

            # print(url)
    pool = multiprocessing.Pool(2)
    pool.map(get_listing, url_listings)

filename = 'trademe_listing_' +  datetime.now().strftime("%Y_%m_%d") + '.txt'

with codecs.open(file_folder+filename, 'w',encoding="utf-8") as f:
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