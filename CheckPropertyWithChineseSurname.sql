 --remove duplicates
USE housing
GO
SELECT COUNT(*) FROM load_rates

SELECT DISTINCT   [capital_value]
      ,[date_of_agreement]
      ,[gross_sale_price]
      ,[land_value]
      ,[payers]
      ,[postal_address]
      ,[property_address]
      ,[settlement_date]
      ,[url]
      ,[value_of_improvements]
      ,[future_land_value]
      ,[future_value_of_improvements]
      ,[future_capital_value]
 FROM load_rates
 WHERE property_address = '1 Highcliff Road Dunedin'
SELECT property_address
FROM load_rates
GROUP BY property_address
HAVING COUNT(*)>1
--49984
--361
SELECT 49984 - 361
--49623

 -- get all chinese owned property
  SELECT DISTINCT SUBSTRING(property_address,1,CHARINDEX(' ',property_address)) street_no
,SUBSTRING(property_address,CHARINDEX(' ',property_address)+ 1,LEN(property_address))  street_name
,[property_address], postal_address,payers,url
INTO #TEMP
  FROM [housing].[dbo].load_rates a
  inner join  
			(SELECT pinyin FROM [housing].[dbo].[ChineseSurname] 
			 union
			 SELECT hongkongsurname FROM  [dbo].[HongKongSurname]
			)
			b
  ON charindex(b.pinyin,a.payers)>0
  ORDER BY postal_address

  CREATE TABLE load_chinese_owned_property_20170208
  (
   property_key INT IDENTITY(1,1),
   property_address VARCHAR(500),
   postal_address VARCHAR(500),
   payers VARCHAR(500),
   url VARCHAR(500)  
  )

  
INSERT INTO [dbo].[load_chinese_owned_property_20170208]
           ([property_address]
           ,[postal_address]
           ,[payers]
           ,[url])
SELECT [property_address],[postal_address],[payers],[url] FROM #TEMP


SELECT [property_address]
           ,SUBSTRING([postal_address],1,LEN([postal_address])-5) [postal_address]
           ,[payers]
           ,[url] 
		   FROM [load_chinese_owned_property_20170208]
		   WHERE postal_address LIKE '%Hospital%'
SELECT [property_address]
           ,[postal_address]
           ,[payers]
           ,[url] 
		   FROM [load_chinese_owned_property_20170208]

SELECT * FROM [load_chinese_owned_property_20170208]

SELECT  a.postal_address FROM [load_chinese_owned_property_20170208] a
LEFT JOIN google_formatted_DCC_rates_postal_address b
ON	a.url = b.url
WHERE b.url IS NULL
GROUP BY a.postal_address


SELECT postal_address FROM [load_chinese_owned_property_20170208] a
GROUP BY a.postal_address


SELECT * FROM google_formatted_DCC_rates_postal_address
 


--in new zealand
SELECT * FROM
(
SELECT iRank = row_number() over(partition by postal_address order BY len(payerS) DESC),postal_address,google_formatted_postal_address,payers
FROM google_formatted_DCC_rates_postal_address
WHERE google_formatted_postal_address LIKE '%new%zealand'
--ORDER BY postal_address
) T
WHERE irank = 1
UNION
----not in new zealand
--po box
SELECT * FROM
(
SELECT iRank = row_number() over(partition by postal_address order BY len(payerS) DESC),postal_address,google_formatted_postal_address,payers
FROM google_formatted_DCC_rates_postal_address
WHERE google_formatted_postal_address NOT LIKE '%new%zealand'
AND postal_address LIKE '%PO%BOX%'
--ORDER BY postal_address
) T
WHERE irank = 1
UNION
-- actual address
SELECT * FROM
(
SELECT iRank = row_number() over(partition by postal_address order BY len(payerS) DESC),postal_address,google_formatted_postal_address,payers
FROM google_formatted_DCC_rates_postal_address
WHERE google_formatted_postal_address NOT LIKE '%new%zealand'
AND postal_address NOT LIKE '%PO%BOX%'
--ORDER BY postal_address
) T
WHERE irank = 1

--------------------------------------------------------------------------------------------------------------------------------------------
WITH t
AS 
(
SELECT * FROM
(
SELECT iRank = row_number() over(partition by postal_address order BY len(payerS) DESC),postal_address,google_formatted_postal_address,payers
FROM google_formatted_DCC_rates_postal_address
WHERE google_formatted_postal_address LIKE '%new%zealand'
AND postal_address NOT LIKE '%PO%BOX%'
--ORDER BY postal_address
) T
WHERE irank = 1
)
, 
tt
AS
(
SELECT postal_address,google_formatted_postal_address, REPLACE(SUBSTRING(payers,1,LEN(payers)-1),';',' & ') payers
		,SUBSTRING(google_formatted_postal_address,LEN(google_formatted_postal_address)-16,4) post_code
		,SUBSTRING(google_formatted_postal_address,1,CHARINDEX(',',google_formatted_postal_address)-1)  street
		,SUBSTRING(  
					SUBSTRING(google_formatted_postal_address, CHARINDEX(',',google_formatted_postal_address)+1, LEN(google_formatted_postal_address)) 
				   ,1
				   ,CHARINDEX(',',SUBSTRING(google_formatted_postal_address, CHARINDEX(',',google_formatted_postal_address)+1, LEN(google_formatted_postal_address)) )-1
				   ) suburb
	    ,
		    SUBSTRING( 	      
				  SUBSTRING(  
					SUBSTRING(google_formatted_postal_address, CHARINDEX(',',google_formatted_postal_address)+1, LEN(google_formatted_postal_address)) 
				   ,CHARINDEX(',',SUBSTRING(google_formatted_postal_address, CHARINDEX(',',google_formatted_postal_address)+1, LEN(google_formatted_postal_address)) )+1
				   ,LEN(google_formatted_postal_address)
				   ) 
				  ,1
				  ,LEN(google_formatted_postal_address)
				  ) city
			
FROM t  
)
SELECT	postal_address
		,google_formatted_postal_address
		,payers
		,post_code
		,street
		,REPLACE(suburb,' '+ post_code,'') suburb
		,CASE WHEN CHARINDEX(post_code, city) <=2
		 THEN REPLACE(suburb,' '+ post_code,'')
		 ELSE SUBSTRING(city,1, CHARINDEX(post_code, city)-2) END city
FROM TT


WITH t
AS 
(
SELECT * FROM
(
SELECT iRank = row_number() over(partition by postal_address order BY len(payerS) DESC),postal_address, REPLACE(SUBSTRING(payers,1,LEN(payers)-1),';',' & ') payers
FROM google_formatted_DCC_rates_postal_address
WHERE postal_address  LIKE '%PO%BOX%'
--ORDER BY postal_address
) T
WHERE irank = 1
)
SELECT * FROM T
 

SELECT * FROM
(
SELECT iRank = row_number() over(partition by a.postal_address order BY len(a.payerS) DESC),a.postal_address, REPLACE(SUBSTRING(a.payers,1,LEN(a.payers)-1),';',' & ') payers
FROM [load_chinese_owned_property_20170208] a
LEFT JOIN google_formatted_DCC_rates_postal_address b
ON	a.url = b.url
WHERE b.url IS NULL
--ORDER BY postal_address
) T
WHERE irank = 1

SELECT  a.postal_address,payers FROM [load_chinese_owned_property_20170208] a
LEFT JOIN google_formatted_DCC_rates_postal_address b
ON	a.url = b.url
WHERE b.url IS NULL
GROUP BY a.postal_address


---------------------------------------------------------------------


SELECT * FROM nz_postcode WHERE [place name] LIKE '%dunedin%'

SELECT *
FROM #TEMP
WHERE postal_address = '100 London Street Dunedin  9016'

SELECT * 
FROM #TEMP
WHERE postal_address LIKE '%AGEN%' OR postal_address LIKE '%REALTY%' OR postal_address LIKE '%PROPERTY%MANAGEMENT%'
OR  postal_address LIKE '%MANAGEMENT%' 



  SELECT * FROM #TEMP
  WHERE payers LIKE '%Te-Tsaw Chen%'
  Te-Tsaw Chen;Lai Hsiu-Chen Chen;

  -- count unique postal address
   -- get all chinese owned property
  SELECT  count(distinct postal_address)
  FROM [housing].[dbo].[load_rates_remove_duplicates] a
  inner join  
			(SELECT pinyin FROM [housing].[dbo].[ChineseSurname] 
			 union
			 SELECT hongkongsurname FROM  [dbo].[HongKongSurname]
			)
			b
  ON charindex(b.pinyin,a.payers)>0





  SELECT COUNT(*) FROM [housing].[dbo].[load_rates] WITH (NOLOCK)

  SELECT *
  INTO [housing].[dbo].[load_rates_remove_duplicates]
  FROM
		(
			SELECT irow = ROW_NUMBER() OVER(Partition BY property_address ORDER BY postal_address DESC)
				  , *
			FROM [housing].[dbo].[load_rates]  WITH (NOLOCK)
		) a
  WHERE irow = 1 

SELECT * INTO [housing].[dbo].[load_rates_remove_duplicates_20161107] FROM [housing].[dbo].[load_rates_remove_duplicates] 

--DROP TABLE [housing].[dbo].[load_rates_remove_duplicates] 

SELECT * FROM [housing].[dbo].[load_rates_remove_duplicates] 
WHERE postal_address IS NULL


 SELECT DISTINCT payers, [property_address], postal_address,url
 INTO #exclude_most_popular
  FROM [housing].[dbo].[load_rates_remove_duplicates] a
  inner join  
			(SELECT pinyin FROM [housing].[dbo].[ChineseSurname] 
			 union
			 SELECT hongkongsurname FROM  [dbo].[HongKongSurname]
			)
			b
  ON charindex(b.pinyin,a.payers)>0
  WHERE postal_address NOT IN (SELECT postal_address FROM #most_popular)
  
  
  select * from #most_popular


  --most popular
   SELECT DISTINCT SUBSTRING(property_address,1,CHARINDEX(' ',property_address)) street_no
,SUBSTRING(property_address,CHARINDEX(' ',property_address)+ 1,LEN(property_address))  street_name
,[property_address], postal_address,payers,url
INTO #most_popular
  FROM [housing].[dbo].[load_rates_remove_duplicates] a
  inner join  
			(SELECT pinyin FROM [housing].[dbo].[ChineseSurname] 
			 union
			 SELECT hongkongsurname FROM  [dbo].[HongKongSurname]
			)
			b
  ON charindex(b.pinyin,a.payers)>0
  INNER JOIN (
  SELECT  DISTINCT SUBSTRING(property_address,CHARINDEX(' ',property_address)+ 1,LEN(property_address))  street_name
  FROM [housing].[dbo].[load_rates_remove_duplicates] a
  inner join  
			(SELECT pinyin FROM [housing].[dbo].[ChineseSurname] 
			 union
			 SELECT hongkongsurname FROM  [dbo].[HongKongSurname]
			)
			b
  ON charindex(b.pinyin,a.payers)>0
  GROUP BY SUBSTRING(property_address,CHARINDEX(' ',property_address)+ 1,LEN(property_address))  
  HAVING COUNT(*)>=10
  ) c
  ON charindex(c.street_name,a.property_address)>0
  ORDER BY 2,1
   

