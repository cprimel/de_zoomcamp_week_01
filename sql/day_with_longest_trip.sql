SELECT date_trunc('day', lpep_pickup_datetime) as day,
		sum(trip_distance)
FROM green_taxi_data
GROUP BY date_trunc('day', lpep_pickup_datetime)
ORDER BY MAX(trip_distance) desc
LIMIT 10;