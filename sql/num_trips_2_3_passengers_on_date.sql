SELECT
	count(case when passenger_count = 2 then 1 else null end) as TwoCount,
	count(case when passenger_count = 3 then 1 else null end) as ThreeCount
FROM green_taxi_data
WHERE lpep_pickup_datetime >= '2019-01-01 00:00:00'
	AND lpep_pickup_datetime < '2019-01-02 00:00:00';