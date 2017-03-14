 TRUNCATE TABLE dbo.load_listings

 
-- update listed date for trademe listings
UPDATE load_listings
SET listed_datetime = DATEADD(YEAR,-1,listed_datetime)
WHERE source = 'TRADEME'
AND DATEDIFF(DAY,snapshot_datetime,listed_datetime) > 1

SELECT * 
FROM  load_listings
WHERE source = 'TRADEME'
AND DATEDIFF(DAY,snapshot_datetime,listed_datetime) > 1

--------
 SELECT * FROM dbo.load_listings
 WHERE seller like '%edinB%'
 AND	CONVERT(CHAR(8),snapshot_datetime,112) ='20161015'  

 

 SELECT SELLER, COUNT(*)
 FROM	load_listings 
 WHERE source = 'realestate'
 AND   CONVERT(CHAR(8),snapshot_datetime,112) ='20161016' 
 AND	suburb <> 'mosgiel'
 GROUP BY seller
 ORDER BY COUNT(*) DESC

  --private
  SELECT CASE WHEN listed_datetime >= '2017-02-19' 
   THEN DATEADD(YEAR,-1,listed_datetime) 
   ELSE listed_datetime
   END listed_datetime, * FROM load_listings
  WHERE 
   CONVERT(CHAR(8),snapshot_datetime,112) ='20170219' 
   AND seller = 'private'
   ORDER BY CASE WHEN listed_datetime >= '2017-02-19' 
   THEN DATEADD(YEAR,-1,listed_datetime) 
   ELSE listed_datetime
   END DESC

 -- SELECT b.payers,b.property_address ,a.*--SELLER, COUNT(*)
 --FROM	load_listings a
 --LEFT JOIN [dbo].[load_rates_remove_duplicates] b
 --ON a.street = rtrim(ltrim(replace(b.property_address,'dunedin','')))
 --WHERE source = 'trademe'
 --AND   CONVERT(CHAR(8),snapshot_datetime,112) ='20170125' 
 --AND	seller = 'private'
 --AND	listed_datetime <= snapshot_datetime
 --order by listed_datetime desc


 SELECT a.* FROM load_listings a
	LEFT JOIN	load_listings b
	ON		a.street = b.street
	--AND		a.suburb = b.suburb
	AND		b.source = 'realestate'
	AND		CONVERT(CHAR(8),b.snapshot_datetime,112) = '20161016' 
	WHERE	CONVERT(CHAR(8),a.snapshot_datetime,112) = '20161016' 
	AND		a.street IS NOT NULL
	AND		a.source = 'trademe'
	AND		b.source IS NULL
