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
