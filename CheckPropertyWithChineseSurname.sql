 

  SELECT DISTINCT SUBSTRING(property_address,1,CHARINDEX(' ',property_address)) street_no
,SUBSTRING(property_address,CHARINDEX(' ',property_address)+ 1,LEN(property_address))  street_name
,[property_address], postal_address,payers,url
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
   

