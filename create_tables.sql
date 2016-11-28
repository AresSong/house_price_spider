
 use housing
 go

 drop table dbo.load_listings
  CREATE TABLE dbo.load_listings
                    (
					[index] NVARCHAR(50),
                    bathroom NVARCHAR(50),
                    bedroom NVARCHAR(50),
                    ensuite NVARCHAR(50),
                    carpark NVARCHAR(50),
                    city    NVARCHAR(50),
                    floor_area NVARCHAR(50),
                    land_area NVARCHAR(50),
                    incorrect_address NVARCHAR(500),
                    listed_datetime DATETIME,
                    price   NVARCHAR(50),
                    property_description nvarchar(max),
                    property_type NVARCHAR(100),
                    region  NVARCHAR(50),
                    sell_type NVARCHAR(50),
                    seller  NVARCHAR(200),
                    snapshot_datetime DATETIME,
                    source  NVARCHAR(50),
                    street  NVARCHAR(100),
                    suburb  NVARCHAR(200),
                    title   NVARCHAR(200),
                    [url]     NVARCHAR(500)
					)