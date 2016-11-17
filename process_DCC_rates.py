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



load_folder = r"C:\Users\ares\PycharmProjects\house_price_spider\files\DCC\working"
#processed_folder =  r"C:\Users\ares\PycharmProjects\house_price_spider\files\processed_files"
load_file_matching = r"DCC_Rates*.txt"

engine = create_engine(r"mssql+pyodbc://sa:123@localhost")
os.chdir(load_folder)
rate_files = glob.glob(load_file_matching)

count = 1

for  file in rate_files:
    rates = []
    rates_formatted = list()
    # file = "DCC_Rates_324133.txt"
    os.chdir(load_folder)
    with open(file, 'r') as f:
        for line in f:
            rates.append(json.loads(line))

    for rate in rates:
        rate_formatted = dict()
        if rate["capital_value"] == "":
            continue
        for key,value in rate.items():
            if key == "capital_value":
                rate_formatted["capital_value"] = str(value).replace(",","")
            elif key == "date_of_agreement":
                rate_formatted["date_of_agreement"] = datetime.strptime(str(value),"%d %b %Y").strftime("%Y-%m-%d %H:%M:%S")
            elif key == "postal_address":
                rate_formatted["postal_address"] = " ".join(str(value).strip().split("\n"))
            elif key == "url":
                rate_formatted["url"] = str(value)
            elif key == "gross_sale_price":
                rate_formatted["gross_sale_price"] = str(value).replace(",","")
            elif key == "land_value":
                rate_formatted["land_value"] = str(value).replace(",", "")
            elif key == "property_address":
                rate_formatted["property_address"] = str(value)
            elif key == "settlement_date":
                rate_formatted["settlement_date"] = datetime.strptime(str(value),"%d %b %Y").strftime("%Y-%m-%d %H:%M:%S")
            elif key == "value_of_improvements":
                rate_formatted["value_of_improvements"] = str(value).replace(",", "")
            elif key == "payers":
                payers = ""
                for payer in value:
                    if payer.strip() != "":
                        payers = payers + payer + ";"
                rate_formatted["payers"] = payers.strip()
        rates_formatted.append(rate_formatted)
    pprint(rates_formatted)
    rates_formatted = pd.DataFrame(rates_formatted)
    rates_formatted.to_sql(name="load_rates", con=engine, if_exists="append")
    print(count)
    count = count +1

    # if count > 1:
    #     break

