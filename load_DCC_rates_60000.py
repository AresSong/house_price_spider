from urllib.request import urlopen
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from pprint import pprint
import re
from urllib.error import HTTPError
from urllib.error import URLError
import time
from datetime import datetime
import json
import codecs

#300000
#400000
#324133
start = 350000
end = 360000
file_folder = r'C:\Users\hosxh\Dropbox\housing_files\\DCC\\working\\'

##add postal address from 339160


# url = r"http://www.dunedin.govt.nz/services/rates-information/rates?ratingID=326001"
# url = r"http://www.dunedin.govt.nz/services/rates-information/rates?ratingID=321972"
# url = r"http://www.dunedin.govt.nz/services/rates-information/rates?ratingID=300000"

current = start
rates = list()
dump_count = 1

while(current <= end):
    rate_info = dict()
    url = r"http://www.dunedin.govt.nz/services/rates-information/rates?ratingID=" + str(current)
    # url = r"http://www.dunedin.govt.nz/services/rates-information/rates?ratingID=321973" + str(current)
    try:
        html = urlopen(url,timeout = 30)
    except (URLError , HTTPError) as e:
        continue

    # print(url)

    bsObj = BeautifulSoup(html.read(), "html.parser")

    table_property_detail = bsObj.find("table",{"summary":re.compile("^The basic property information of")})

    if table_property_detail is None:
        continue

    for i in table_property_detail.contents:
        if str(type(i)) != "<class 'bs4.element.NavigableString'>" and i.th is not None:
            if i.th.text == "Property address":
                #print(i.td.text)
                rate_info["property_address"] = i.td.text
            elif i.th.text == "Postal address for this assessment":
                rate_info["postal_address"] = i.td.text
            elif i.th.text == "Ratepayer name(s)":
                #print(i.td.contents)
                payers = list()
                for payer in i.td.contents:
                    if str(type(payer)) == "<class 'bs4.element.NavigableString'>":
                        payers.append(payer)
                rate_info["payers"] = payers
        #print("~~~~~~~~~~~~~~~~~")

    table_current_Rates = bsObj.find("table",{"summary":"Current Rating Information"})
    for i in table_current_Rates.contents:
        if str(type(i)) != "<class 'bs4.element.NavigableString'>" and i.th is not None:
            #print(len(i.contents))
            if len(i.contents) == 5: #need to change, using 5 is not properly
                if i.th.text == "Rating period":
                    rate_info["rating_period"] = i.td.text
            else:
                for sub_i in i.contents:
                    if str(type(sub_i)) != "<class 'bs4.element.NavigableString'>" and sub_i.th is not None:
                        if sub_i.th.text.find("Value of improvements") != -1:
                            rate_info["value_of_improvements"] = sub_i.td.text
                        elif sub_i.th.text.find("Land value") != -1:
                            rate_info["land_value"] = sub_i.td.text
                        elif sub_i.th.text.find("Capital value") != -1 :
                            rate_info["capital_value"] = sub_i.td.text
                        elif sub_i.th.text.find("Rating differential") != -1:
                            rate_info["rating_differential"] = sub_i.td.text
                        elif sub_i.th.text.find("Land use") != -1:
                            rate_info["land use"] = sub_i.td.text
                        elif sub_i.th.text.find("Area in hectares") != -1:
                            rate_info["area_in_hectares"] = sub_i.td.text

    table_sale_details = bsObj.find("table",{"summary":"Most recent Property Sales Data"})
    if table_sale_details is not None:
        table_sale_details = table_sale_details.find("div", {"id": "ctl00_CODContent_rptRatesDetails_ctl00_rptSales_ctl00_pnlRow"})
        for i in table_sale_details.contents:
            if str(type(i)) != "<class 'bs4.element.NavigableString'>" and i.th is not None:
                if i.th.text == "Gross Sale Price":
                    rate_info["gross_sale_price"] = i.td.text
                elif i.th.text == "Date of Agreement":
                    rate_info["date_of_agreement"] = i.td.text
                elif i.th.text == "Settlement Date":
                    rate_info["settlement_date"] = i.td.text

    table_future_Rates = bsObj.find("table", {"summary": "Future rating details"})
    if table_future_Rates is not None:
        for i in table_future_Rates.contents:
            if str(type(i)) != "<class 'bs4.element.NavigableString'>" and i.th is not None:
                #print(len(i.contents))
                if len(i.contents) == 5: #need to change, using 5 is not properly
                    # print(i.contents)
                    if i.th.text == "Future rating period":
                        rate_info["future_rating_period"] = i.td.text
                    elif i.th.text.find("Value of improvements") != -1:
                        rate_info["future_value_of_improvements"] = i.td.text
                    elif i.th.text.find("Land value") != -1:
                        rate_info["future_land_value"] = i.td.text
                    elif i.th.text.find("Capital value") != -1:
                        rate_info["future_capital_value"] = i.td.text
                    elif i.th.text.find("Rating differential") != -1:
                        rate_info["future_rating_differential"] = i.td.text
                    elif i.th.text.find("Land use") != -1:
                        rate_info["future_land use"] = i.td.text
                    elif i.th.text.find("Area in hectares") != -1:
                        rate_info["future_area_in_hectares"] = i.td.text

    rate_info["url"] = url
    # print(current)
    # pprint(rate_info)
    rates.append(rate_info)

    dump_count = dump_count + 1
    if dump_count == 100:
        filename = 'DCC_Rates_' + str(current) + '.txt'
        with codecs.open(file_folder + filename, 'w') as f:
            for i in rates:
                f.write(json.dumps(i) + "\n")
        rates = list()
        dump_count = 1
    current = current + 1
    # if current >= 1:
    #     break