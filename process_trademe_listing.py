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
import glob
import glob
import os
from sqlalchemy import create_engine

load_folder = r"C:\Users\ares\PycharmProjects\house_price_spider\files\load_files"
load_file_matching = r"trademe_listing*.txt"
engine = create_engine(r"mssql+pyodbc://sa:123@localhost")
os.chdir(load_folder)

listing_files = glob.glob("trademe_listing*.txt")

def remove_letters(x):
    x = str(x)
    if re.search('[0-9]+', x) is not None:
        return re.search('[0-9]+', x).group()
    else:
        None

for file in listing_files:
    # print(file)
    listings = []
    with open(file, 'r') as f:
        for line in f:
            listings.append(json.loads(line))

    # pprint(listings)
    # pprint(len(listings))

    #test
    #listing = {"snapshot_datetime": "2016-10-03 22:30:24", "seller": "Ray White Dunedin (Proven Realty Ltd)", "Property type:": ["House"], "Rooms:": ["6 or more bedrooms, 6 or more bathrooms"], "listed_datetime": "2016-10-03 16:31:00", "Location:": ["360 High Street", "City Centre", "Dunedin", "Otago"], "url": "http://www.trademe.co.nz/property/residential-property-for-sale/auction-1174158920.htm", "Price:": ["Asking price $925,000"], "Rateable value (RV):": ["$735,000"]}

    ##inspect attribute type
    # key_inspection = set()
    # for listing in listings:
    #     listing = dict(listing)
    #     for key, value in listing.items():
    #         key_inspection.add(key)
    # print(key_inspection)
    #{'url', 'Property type:', 'Land area:', 'Price:', 'seller', 'Floor area:', 'In the area:'
    # , 'Smoke alarm:', 'Open home times:', 'Viewing instructions:', 'Parking:', 'listed_datetime'
    # , 'Rateable value (RV):', 'snapshot_datetime', 'Location:', 'Property ID#:', 'Rooms:'}

    ##inspect price type
    # price_inspection = set()
    # for listing in listings:
    #     listing = dict(listing)
    #     for key, value in listing.items():
    #         if key == "Price:":
    #             if value[0].find("Asking price") != -1 and value[0].find("Enquiries over") != -1  and \
    #                 value[0].find("Price by negotiatio") != -1  and value[0].find("To be sold by deadline") != -1 :
    #                 price_inspection.add(value)
    #
    # print(price_inspection)
    ## Asking price $, Enquiries over $, Price by negotiatio, To be sold by deadline

    # selected_features = set(['','',''])
    #

    listings_formatted = list()

    for listing in listings:
        listing_formatted = dict()
        for key, value in listing.items():
            if key == "Location:":
                if len(value) == 4:
                    listing_formatted["street"] = value[0]
                    listing_formatted["suburb"] = value[1]
                    listing_formatted["city"] = value[2]
                    listing_formatted["region"] = value[3]
                else:
                    listing_formatted["incorrect_address"] = ",".join(value)
            elif key == "Rooms:":
                rooms = str(value)
                rooms = rooms.split(",")
                for room in rooms:
                    if  room.find("bedroom") != -1:
                        listing_formatted["bedroom"] = room
                    else:
                        listing_formatted["bathroom"] = room
            elif key == "Floor area:":
                listing_formatted["floor_area"] = value[0]
            elif key == "Location:":
                listing_formatted["land_area"] = value[0]
            elif key == "Price:":
                if value[0].find("Asking price") != -1:
                    listing_formatted["sell_type"] = "asking_price"
                    listing_formatted["price"] = str(value[0]).replace("Asking price $","").replace(",","").strip()
                elif value[0].find("Enquiries over") != -1:
                    listing_formatted["sell_type"] = "enquiries_over"
                    listing_formatted["price"] = str(value[0]).replace("Enquiries over $","").replace(",","").strip()
                elif value[0].find("Price by negotiatio") != -1 :
                    listing_formatted["sell_type"] = "negotiation"
                    listing_formatted["price"] = None
                elif value[0].find("To be sold by deadline") != -1 :
                    listing_formatted["sell_type"] = "sold_by_deadline"
                    listing_formatted["price"] = None
                elif value[0].find("auction") != -1:
                    listing_formatted["sell_type"] = "auction"
                    listing_formatted["price"] = None
            elif key == "Property type:":
                listing_formatted["property_type"] = str(value[0])
            elif key == "url":
                listing_formatted["url"] = value
            elif key == "seller":
                listing_formatted["seller"] = value
            elif key == "listed_datetime":
                listing_formatted["listed_datetime"] = value
            elif key == "snapshot_datetime":
                listing_formatted["snapshot_datetime"] = value
        listing_formatted["source"] = "TradeMe"
        listings_formatted.append(listing_formatted)



    listings_formatted = pd.DataFrame(listings_formatted)
    # print(listings_formatted)
    listings_formatted["bathroom"] = listings_formatted["bathroom"].map(remove_letters)
    listings_formatted["bedroom"] = listings_formatted["bedroom"].map(remove_letters)
    listings_formatted = listings_formatted.where((pd.notnull(listings_formatted)), '')
    # pprint(listings_formatted)
    # pprint(len(listings_formatted))
    # print(listings_formatted.head())
    # print(listings_formatted.columns)

    # filename = "formatted_" + file
    # with codecs.open(filename, 'w') as f:
    #     for i in listings:
    #         f.write(json.dumps(i) + "\n")
    # print(listings_formatted.dtypes)
    # print((listings_formatted.loc[264]))

    listings_formatted.to_sql(name="load_listings", con=engine, if_exists="append")
