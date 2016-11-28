 
 SELECT * FROM dbo.load_listings
 WHERE seller like '%edinB%'
 AND	CONVERT(CHAR(8),snapshot_datetime,112) ='20161015'  

 DECLARE @today CHAR(8) = CONVERT(CHAR(8),DATEADD(day,0,getdate()),112)

 SELECT @today

 SELECT b.property_address,b.payers,a.* FROM 
 (
	SELECT a.* FROM load_listings a
	LEFT JOIN	load_listings b
	ON		a.street = b.street
	--AND		a.suburb = b.suburb
	AND		b.source = 'Trademe'
	AND		CONVERT(CHAR(8),b.snapshot_datetime,112) = @today
	WHERE	CONVERT(CHAR(8),a.snapshot_datetime,112) = @today
	AND		a.street IS NOT NULL
	AND		a.source = 'realestate'
	AND		b.source IS NULL
	UNION
	SELECT a.* FROM load_listings a
	WHERE	a.source = 'trademe'
	AND		CONVERT(CHAR(8),a.snapshot_datetime,112) = @today 
 
 ) a
 LEFT JOIN [dbo].[load_rates_remove_duplicates] b
 ON a.street = rtrim(ltrim(replace(b.property_address,'dunedin','')))
 WHERE	DATEDIFF(day, listed_datetime,getdate())>=60
 AND	DATEDIFF(day, listed_datetime,getdate())<=100
 AND	CONVERT(CHAR(8),snapshot_datetime,112) =@today
 ORDER BY listed_datetime DESC


 SELECT SELLER, COUNT(*)
 FROM	load_listings 
 WHERE source = 'realestate'
 AND   CONVERT(CHAR(8),snapshot_datetime,112) ='20161016' 
 AND	suburb <> 'mosgiel'
 GROUP BY seller
 ORDER BY COUNT(*) DESC

  


  SELECT b.payers,b.property_address ,a.*--SELLER, COUNT(*)
 FROM	load_listings a
 LEFT JOIN [dbo].[load_rates_remove_duplicates] b
 ON a.street = rtrim(ltrim(replace(b.property_address,'dunedin','')))
 WHERE source = 'trademe'
 AND   CONVERT(CHAR(8),snapshot_datetime,112) ='20161108' 
 AND	seller = 'private'
 AND	listed_datetime <= snapshot_datetime
 order by listed_datetime desc


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