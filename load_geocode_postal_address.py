import googlemaps
from pprint import pprint
import pandas as pd
from sqlalchemy import create_engine

gmaps = googlemaps.Client(key='AIzaSyDeoUwZdZdc6wyVhYFl9zv09oCH4DguwB4')
engine = create_engine(r"mssql+pyodbc://sa:123@localhost")
DCC_rates = pd.read_sql(r"""SELECT [property_address]
           ,[postal_address]
           ,[payers]
           ,[url]
		   FROM [load_chinese_owned_property_20170208]""",engine)
DCC_rates["postal_address"] = DCC_rates["postal_address"].map(lambda x: " ".join(x.split("\n")))

google_formatted_DCC_rates = list()
column_name = list()
for index, row in DCC_rates.iterrows():
    # print((row))
    # print(row["property_address"])
    geocode_result = gmaps.geocode(str(row["postal_address"]))
    if len(geocode_result) != 0:
        row["google_formatted_postal_address"] = geocode_result[0]["formatted_address"]
        row["google_lat"] = geocode_result[0]["geometry"]["location"]["lat"]
        row["google_lng"] = geocode_result[0]["geometry"]["location"]["lng"]
        # print(list(row))
        google_formatted_DCC_rates.append(list(row))
        column_name = row.index



google_formatted_DCC_rates = pd.DataFrame(google_formatted_DCC_rates)
google_formatted_DCC_rates.columns = column_name

pprint(google_formatted_DCC_rates)

google_formatted_DCC_rates.to_sql("google_formatted_DCC_rates_postal_address",engine,if_exists = "append")

# # Geocoding an address
# geocode_result = gmaps.geocode('114 Tyne Street Mosgiel')
# # geocode_result = gmaps.geocode('251 Signal Hill Road Dunedin')
#
# pprint((geocode_result[0]))
#
# pprint((geocode_result[0]["formatted_address"]))
# pprint((geocode_result[0]["geometry"]["location"]["lat"]))
# pprint((geocode_result[0]["geometry"]["location"]["lng"]))
#
# # for i in geocode_result.item:
# #     i.key