f = load '$INPUT' using PigStorage(',') as (Date:chararray, Hour:chararray, P:float);
ff = foreach f generate Hour, ($2>0?1:0), Date;
g = group ff by ($0, $1);
t = foreach g generate group, COUNT(ff.Date);
store t into '$OUTPUT' using PigStorage(',');