# Instructions

```
$ docker-compose up -d
$ python ingest_data.py --user="root" --password="root" --host="localhost" --port=5432 --dbname="ny_taxi" --tablename="green_taxi_data" --url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz"
```