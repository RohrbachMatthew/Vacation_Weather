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
order by field(day, 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')