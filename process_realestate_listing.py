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
import os
from sqlalchemy import create_engine
import pyodbc


load_folder = r"C:\Users\hosxh\PycharmProjects\house_price_spider\files\load_files"
processed_folder =  r"C:\Users\hosxh\PycharmProjects\house_price_spider\files\processed_files"
load_file_matching = r"RealEstate_listing*.txt"

engine = create_engine(r"mssql+pyodbc://sa:123@localhost")
os.chdir(load_folder)
listing_files = glob.glob(load_file_matching)


def remove_letters(x):
    if re.search('[0-9]+', x) is not None:
        return re.search('[0-9]+', x).group()
    else:
        None


def clear_floor_area(x):
    if len(x.strip()) == 0:
        return None
    elif x.find("m2"):
        return re.search('[0-9]+', x).group()
    else:
        return "error"


def clear_land_area(x):
    if len(x.strip()) == 0:
        return None
    elif x.find("m2") != -1:
        return re.search('[0-9]+', x.replace(",", "")).group()
    elif x.find("ha") != -1:
        return int(re.search('[0-9]+', x.replace(",", "")).group()) * 10000
    else:
        return "error"


for file in listing_files:
    listings = []
    #file = "realestate_listing_2016_10_14.txt"
    os.chdir(load_folder)
    with open(file, 'r') as f:
        for line in f:
            listings.append(json.loads(line))

    # pprint(listings)
    # pprint(len(listings))

    #
    # #inspect attribute type
    # key_inspection = set()
    # for listing in listings:
    #     listing = dict(listing)
    #     for key, value in listing.items():
    #         key_inspection.add(key)
    # print(key_inspection)
    # # {'landArea', 'carParks', 'seller', 'ensuites', 'suburb', 'street'
    # #     , 'floorArea', 'snapshot_datetime', 'listed_datetime', 'bathrooms'
    # #     , 'price', 'bedrooms', 'url', 'property_type', 'property_description', 'title'}
    #
    # ##inspect price type
    # price_inspection = set()
    # for listing in listings:
    #     listing = dict(listing)
    #     for key, value in listing.items():
    #         if key == "price":
    #             if value.find("Negotiable from $") and value.find("Enquiries over $") and\
    #                     value.find("Offers over $") and value.find("Asking price $") and\
    #                     value.find("POA") and value.find("Auction") and value.find("$") != 0:
    #                 price_inspection.add(value)
    #
    # print(price_inspection)
    # ##Negotiable from $, Enquiries over $,Offers over $,Asking price $,POA,Auction,Tender,Deadline Treaty,Offers,Negotiation
    #

    listings_formatted = list()
    #test
    #listing = {"price": "Auction", "property_description": r"\nAuction Location: LJ Hooker Office, 63 Musselburgh Rise, Dunedin.\nFor 10 happy years the current owner has enjoyed life at No 43 Dunrobin Street. Hidden from the street, with plenty of sun and natural light, this one level 120m2 gem on 476m2 section is sure to delight. It's the perfect fit for couples of all ages and small families. Minutes walk to Grants Braes Primary School, this property is located in the heart of the Waverley community. 3 good size bedrooms, open plan living room, dining and kitchen all heated by a heatpump. Recently re-carpeted and refreshed exterior, this is what we class as - just good real estate!! Decisions have been made - to be sold prior to or at Auction.\n", "ensuites": "", "carParks": "1            Car Space", "property_type": "Residential House", "bathrooms": "1            Bathroom", "listed_datetime": "Listed 6 Oct 2016", "bedrooms": "3            Bedrooms", "seller": "Wayne Graham Realty Ltd LJ Hooker, Dunedin", "title": "Outstanding Value in Waverley", "floorArea": "", "url": "http://www.realestate.co.nz/2918084", "snapshot_datetime": "2016-10-08 20:55:03", "street": "43 Dunrobin Street", "suburb": "Waverley", "landArea": "476 m2 Land"}

    for listing in listings:
        listing_formatted = dict()
        for key,value in listing.items():
            if key == "bedrooms":
                listing_formatted["bedroom"] = value
            elif key == "bathrooms":
                listing_formatted["bathroom"] = value
            elif key == "landArea":
                listing_formatted["land_area"] = value
            elif key == 'carParks':
                listing_formatted["carpark"] = value
            elif key == 'ensuites':
                listing_formatted["ensuite"] = value
            elif key == 'floorArea':
                listing_formatted["floor_area"] = value
            elif key == 'title':
                listing_formatted["title"] = value
            elif key == 'property_type':
                listing_formatted["property_type"] = value
            elif key == 'property_description':
                listing_formatted["property_description"] = value.strip('\n')
            elif key == 'seller':
                listing_formatted["seller"] = value
            elif key == 'suburb':
                listing_formatted["suburb"] = value
            elif key == 'street':
                listing_formatted["street"] = value
            elif key == 'url':
                listing_formatted["url"] = value
            elif key == 'listed_datetime':
                listing_formatted["listed_datetime"] = datetime.strptime(value.replace("Listed ",""),"%d %b %Y").strftime("%Y-%m-%d %H:%M:%S")
            elif key == "snapshot_datetime":
                listing_formatted["snapshot_datetime"] = value
            elif key == "price":
                #print(value)
                if value.find("Negotiable from $") != -1:
                    listing_formatted["sell_type"] = "negotiable_from"
                    listing_formatted["price"] = value.replace("Negotiable from $","").replace(",","")
                elif value.find("Enquiries over $") != -1:
                    listing_formatted["sell_type"] = "enquiries_over"
                    listing_formatted["price"] = value.replace("Enquiries over $","").replace(",","")
                elif value.find("Asking price $")  != -1:
                    listing_formatted["sell_type"] = "asking_price"
                    listing_formatted["price"] = value.replace("Asking price $", "").replace(",", "")
                elif value.find("Offers over $") != -1:
                    listing_formatted["sell_type"] = "offers_over"
                    listing_formatted["price"] = value.replace("Offers over $", "").replace(",", "")
                elif value.find("POA")  != -1:
                    listing_formatted["sell_type"] = "POA"
                    listing_formatted["price"] = value.replace("POA", "").replace(",", "")
                elif value.find("Auction")  != -1:
                    listing_formatted["sell_type"] = "auction"
                    listing_formatted["price"] = value.replace("Auction", "").replace(",", "")
                elif value.find("Tender")  != -1:
                    listing_formatted["sell_type"] = "tendar"
                    listing_formatted["price"] = value.replace("Tender", "").replace(",", "")
                elif value.find("Deadline Treaty")  != -1:
                    #print("~~~~~~~~~~~~~~~")
                    listing_formatted["sell_type"] = "deadline_treaty"
                    listing_formatted["price"] = value.replace("Deadline Treaty", "").replace(",", "")
                    # print(value.replace("Deadline Treaty", "").replace(",", ""))
                elif value.find("Offers")  != -1:
                    listing_formatted["sell_type"] = "offers"
                    listing_formatted["price"] = value.replace("Offers", "").replace(",", "")
                elif value.find("Negotiation") != -1:
                    listing_formatted["sell_type"] = "negotiation"
                    listing_formatted["price"] = value.replace("Negotiation", "").replace(",", "")
            listing_formatted["city"] = "Dunedin"
            listing_formatted["region"] = "Otago"
            listing_formatted["source"] = "RealEstate"
        listings_formatted.append(listing_formatted)

    # print(listings_formatted)

    listings_formatted = pd.DataFrame(listings_formatted)
    #print(listings_formatted.head(10))
    # print(listings_formatted.columns)


    # print(listings_formatted["bathroom"].map(remove_letters))
    # print(listings_formatted["bedroom"].map(remove_letters))
    # print(listings_formatted["carpark"].map(remove_letters))
    # print(listings_formatted["ensuite"].map(remove_letters))

    listings_formatted["bathroom"] = listings_formatted["bathroom"].map(remove_letters)
    listings_formatted["bedroom"] = listings_formatted["bedroom"].map(remove_letters)
    listings_formatted["carpark"] = listings_formatted["carpark"].map(remove_letters)
    listings_formatted["ensuite"] = listings_formatted["ensuite"].map(remove_letters)

    # print(listings_formatted.head(100))
    # print(listings_formatted["floor_area"].map(clear_floor_area))
    # print(listings_formatted["land_area"].map(clear_land_area))
    listings_formatted["floor_area"] = listings_formatted["floor_area"].map(clear_floor_area)
    listings_formatted["land_area"] = listings_formatted["land_area"].map(clear_land_area)

    #print(listings_formatted.head())
    # print(listings_formatted.columns)
    # print(listings_formatted)

    ## check number of listings for each agent company
    # print(type(listings_formatted[["url","seller"]].groupby(["seller"]).agg(["count"])))
    # print(len(listings_formatted))
    # listings_formatted[["url","seller"]].groupby(["seller"]).agg(["count"]).to_csv("testing.csv")

    #print(listings_formatted.loc[listings_formatted["seller"] == "Proven Realty Ltd Ray White, Dunedin"])
    ## check deadline sales
    # print(listings_formatted.loc[(listings_formatted["seller"] == "Edinburgh Realty Ltd Dunedin") &
    #                             ( listings_formatted["property_description"].map(lambda x: re.search("dead",x,re.IGNORECASE) is not None) )])

    # os.chdir(processed_folder)
    # filename = "formatted_" + file
    # with codecs.open(processed_folder + filename, 'w') as f:
    #     for i in listings:
    #         f.write(json.dumps(i) + "\n")
    listings_formatted.to_sql(name = "load_listings", con = engine, if_exists = "append")




