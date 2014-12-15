/*medallion, hack_license, vendor_id, pickup_datetime, dropoff_datetime, passenger_count, trip_time_in_secs, trip_distance, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, fare_amount, tip_amount, total_amount, precipt*/



t = LOAD 'tripData2013/trip_data_12.csv' USING PigStorage(',') As (medallion:chararray, hack_license:chararray, vendor_id:chararray, rate_code:int, store_and_fwd_flag:chararray, pickup_datetime:chararray, dropoff_datetime:chararray, passenger_count:int, trip_time_in_secs:int, trip_distance:int, pickup_longitude:float, pickup_latitude:float, dropoff_longitude:float, dropoff_latitude:float);
f = LOAD 'faredata2013/trip_fare_12.csv' USING PigStorage(',') As (medallion:chararray, hack_license:chararray, vendor_id:chararray, pickup_datetime:chararray, payment_type:chararray, fareamount:float, surcharge:float, mta_tax:float, tip_amount:float, tolls_amount:float, total_amount:float);
we = load 'processed/p12.csv' using PigStorage(',') as (Date:chararray, Hour:Chararray, P:float);
w = foreach we generate $0, ($1=='24'?'00':$1), ($2>0?1:0);
ft = join f by (medallion, hack_license, vendor_id, pickup_datetime), t by (medallion, hack_license, vendor_id, pickup_datetime);
fullfare = foreach ft generate $0, $1, $2, $3, $17, $18, $19, $20, $21, $22, $23, $24, $5, $8, $10;
temp = foreach w generate SUBSTRING(CONCAT($0, $1), 6, 10), $2;
ffp = foreach fullfare generate $0, $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, CONCAT(SUBSTRING($3, 8, 10), SUBSTRING($3, 11, 13));
res = foreach (join ffp by $15, temp by $0) generate $0, $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $17;
store res into 'res12' using PigStorage(',');
