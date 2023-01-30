SELECT z2."Zone", c.maxtip FROM
	(SELECT g."DOLocationID", MAX(g.tip_amount) as maxtip
	FROM green_taxi_data g
		LEFT JOIN zones z
		ON g."PULocationID" = z."LocationID"
	WHERE z."Zone" = 'Astoria'
	GROUP BY g."DOLocationID") as c
LEFT JOIN zones z2
	ON c."DOLocationID" = z2."LocationID"
ORDER BY maxtip desc;