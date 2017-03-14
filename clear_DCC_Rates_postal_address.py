import pandas as pd
from sqlalchemy import create_engine
from pprint import pprint
from load_unity_address_func import unify_address_pandas
engine = create_engine(r"mssql+pyodbc://sa:123@localhost")
suburb_mapping = pd.read_sql(r"SELECT * FROM [dbo].[suburb_mapping]",engine)

DCC_rates = pd.read_sql(r"""SELECT [property_address]
           ,SUBSTRING([postal_address],1,LEN([postal_address])-5) [postal_address]
           ,[payers]
           ,[url]
		   FROM [load_chinese_owned_property_20170208]
"""
                        ,engine)

# pprint(suburb_mapping)
#
# print(DCC_rates)

# print(unify_address("45 Campbells Road Dunedin",suburb_mapping))


DCC_rates["postal_address"] = DCC_rates["postal_address"].map(lambda x: " ".join(x.split("\n")))

# pprint(DCC_rates)

unified_address = pd.DataFrame(DCC_rates["postal_address"].apply(unify_address_pandas, args = (suburb_mapping,) ))
unified_address = pd.DataFrame(list(unified_address["postal_address"]),
                               columns = ["postal_address","street_no_unified","street_name_unified",
                                          "suburb_unified","city_unified",
                                          "postcode_unified"])
# print(unified_address)
# print(type((unified_address)))

DCC_rates_unified_address = pd.merge(DCC_rates, unified_address, on='postal_address')

DCC_rates_unified_address.to_sql("DCC_rates_unified_postal_address",engine,if_exists = "append")