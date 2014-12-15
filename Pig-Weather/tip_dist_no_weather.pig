f = load '$INPUT' using PigStorage(',') as (medallion:chararray, hack_license:chararray, vendor_id:chararray, pickup_datetime:chararray, dropoff_datetime:chararray, passenger_count:int, trip_time_in_secs:int, trip_distance:float, pickup_longitude:float, pickup_latitude:float, dropoff_longitude:float, dropoff_latitude:float, fare_amount:float, tip_amount:float, total_amount:float, precipt:float);
f1 = filter f by (trip_distance>0 and trip_distance/trip_time_in_secs<100 and trip_distance<100);
ff = foreach f1 generate (int)trip_distance/5, tip_amount;
g = group ff by $0;
t = foreach g generate flatten(group), AVG(ff.tip_amount);
store t into '$OUTPUT' using PigStorage(',');