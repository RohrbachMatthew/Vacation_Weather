/*
--This is for the AVG daily temperature 
-- Gets AVG temperature and makes a temp table
with daily_average AS (
SELECT day, date, avg(temperature) AS avg_daily_temp
from vacation_weather_data
GROUP BY day, date)

-- Average them by the day name
Select day, count(*) as num_days,
round(AVG(avg_daily_temp),2) AS avg_temp
from daily_average
group by day
order by field(day, 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')
*/


-- This is for the avg daily humidity
-- Get average humidity and make a temp table
/*
with humidity_avg as(
select day, date, avg(humidity) as avg_daily_humidity
from vacation_weather_data
group by day, date)

-- Average by the day
select day, count(*) as num_days,
round(AVG(avg_daily_humidity),2) as avg_daily_humidity
from humidity_avg
group by day
order by field(day, 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')
*/


/*
-- This is the average daily weather conditions (clear,cloudy,rain)

with ranked_conditions as (
SELECT day, conditions, 
count(*) as frequency,
rank() over (partition by day ORDER BY COUNT(*) DESC, conditions) as rn
from vacation_weather_data
group by day, conditions
)
select day, conditions
from ranked_conditions
where rn=1;
*/


-- Join table ot compare temps and humidity
with temp AS (
SELECT day, date, AVG(temperature) as avg_temp
FROM vacation_weather_data
GROUP BY day, date),
humidity AS (
SELECT day, date, AVG(humidity) as avg_humidity
FROM vacation_weather_data
GROUP BY day, date),
merged as (
SELECT t.day, t.date, t.avg_temp, h.avg_humidity
from temp t
JOIN humidity h ON t.day = h.day AND t.date = h.date
)
SELECT day,
round(avg(avg_temp), 2) as avg_daily_temp,
round(avg(avg_humidity), 2) as avg_daily_humidity
FROM merged
GROUP BY day
ORDER BY FIELD(day, 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday');

