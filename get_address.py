from urllib.request import urlopen
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from pprint import pprint
import re
from urllib.error import HTTPError
#Retrieve HTML string from the URL
#html = urlopen("http://www.pythonscraping.com/exercises/exercise1.html")

#addresses = pd.DataFrame(columns = ['street_no','street','city','suburb','postcode'])
addresses = list()

street = 'PINE HILL ROAD'
city = 'DUNEDIN'
i = 1

number = re.compile(r"[0-9]+")


while i <= 1000:
    address = list()

    suburb = ''
    postcode = ''
    street_no = str(i)#'1'
    full_street =  street_no + ' ' + street

    #address = r'https://www.nzpost.co.nz/tools/address-postcode-finder/suggest/112%20Pine%20Hill%20Road%20Dunedin'
    search_prefix = r'https://www.nzpost.co.nz/tools/address-postcode-finder/suggest/'
    search_space = r'%20'
    search_address = street_no + search_space + street + search_space + city
    search_string = search_prefix + search_address
    search_string = search_string.replace(' ',search_space)


    print(search_string)

    try:
        html = urlopen(search_string)
    except HTTPError as e:
        continue

    bsObj = BeautifulSoup(html.read(), "html.parser")

    #print(html.read())
    #print(bsObj.html)

    ## address not exists
    ### sample for address exists
    '''
    <!--<div id="no-exact-match" class="messages warning">-->
    <p>'<strong>13 Pine Hill Road Dunedin</strong>' is not a complete address.</p>
    '''

    if (bsObj.find("div", { "class" : "suggestion" }) is not None and bsObj.find("div", { "class" : "suggestion" }).text.find('is not a complete address') > 0 )  :
        i = i + 1
        continue
    else:

        ## address exists
        ### sample for address exists
        '''
        < p


        class ="address-label-postal" itemscope="" itemtype="http://schema.org/PostalAddress" >

        < span
        itemprop = "streetAddress" >

        112
        Pine
        Hill
        Road < br >

        < / span >

        < span
        itemprop = "addressLocality" > Dalmore < / span > < br >

        < span
        itemprop = "addressRegion" > Dunedin < / span >

        < span
        itemprop = "postalCode" > 9010 < / span >

        < / p >
        '''
        ### Decompose the address
        start_char = r'>'
        print(bsObj.find("p", {"class": "address-label-postal"}).text.strip() )
        print(bsObj.find("p", { "class" : "address-label-postal" }).text.strip().upper().replace(full_street,'').replace(city,'').split(' '))
        #print(type(bsObj.find("p", { "class" : "address-label-postal" }).text))
        if bsObj.find("p", { "class" : "address-label-postal" }).text.strip().upper().replace(full_street,'').find(city) == -1 :
            i = i + 1
            continue

        address = bsObj.find("p", { "class" : "address-label-postal" }).text.strip().upper().replace(full_street,'').replace(city,'').split(' ')

        #print((address))
        if len(address) > 2:
            for a in address:
                if number.match(a) is None:
                    suburb = suburb + ' ' + a
                    suburb = suburb.strip()
                else:
                    postcode = a
        else:
            suburb = address[0]
            postcode = address[1]

        address = [street_no, street, city,suburb,postcode]
        addresses.append(address)
    i = i +1


addresses_pd = pd.DataFrame(addresses,columns = ['street_no','street','city','suburb','postcode'] )

pprint(addresses_pd)
addresses_pd.to_csv('C:\\Users\\ares\\PycharmProjects\\house_price_spider\\tst.csv')