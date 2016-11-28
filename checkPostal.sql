SELECT SUBSTRING(property_address,1,CHARINDEX(' ',property_address)) street_no
,SUBSTRING(property_address,CHARINDEX(' ',property_address)+ 1,LEN(property_address))  street_name,* 
FROM [housing].[dbo].[load_rates_remove_duplicates] a
INNER JOIN #postal p
ON		CHARINDEX(p.stree_name,a.property_address) >0
ORDER BY street_name,street_no

SELECT  
distinct SUBSTRING(property_address,CHARINDEX(' ',property_address)+ 1,LEN(property_address))  street_name 
FROM [housing].[dbo].[load_rates_remove_duplicates] a
INNER JOIN #postal p
ON		CHARINDEX(p.stree_name,a.property_address) >0
ORDER BY street_name,street_no




SELECT * FROM [housing].[dbo].[load_rates]
WHERE PROPERTY_ADDRESS LIKE '%LYNN%STREET%'


SELECT 'lynn street' stree_name INTO #postal
UNION
SELECT 'greenhill avenue'
UNION
SELECT 'prospect bank'
UNION
SELECT 'holyrood avenue'
UNION
SELECT 'shetland street'
UNION
SELECT 'mayfield avenue'
UNION
SELECT 'stratheam avenue'
UNION
SELECT 'forresbank avenue'
UNION
SELECT 'ethel street'


--check postal address is not property address and chinese 
SELECT	DISTINCT postal_address
		,property_address
		,PAYERS
		,URL
		
FROM	[housing].[dbo].[load_rates_remove_duplicates]  a
  inner join  
			(SELECT pinyin FROM [housing].[dbo].[ChineseSurname] 
			 union
			 SELECT hongkongsurname FROM  [dbo].[HongKongSurname]
			)
			b
  ON charindex(b.pinyin,a.payers)>0
WHERE	CHARINDEX(REPLACE(property_address,' - ','/'),postal_address)=0
order by postal_address 
 


select  *  FROM	[housing].[dbo].[load_rates_remove_duplicates]
WHERE POSTAL_ADDRESS = '35 Grove Street Dunedin  9012'
