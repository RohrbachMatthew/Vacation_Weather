# Auto Data Collection Through Email

To use this project I would send an email to the email account associated with the python script.  
The python auto script would run at a scheduled time (11 PM), collect the data from the email and insert it into the mysql database.  
The data is from VA Beach.

## Files:
- [Click here for python email script](https://github.com/RohrbachMatthew/Vacation_Weather/blob/main/weather_email_auto_python/main.py) - This is the email script that would run once everyday.
- [Click here for the python script](https://github.com/RohrbachMatthew/Vacation_Weather/blob/main/weather_email_auto_python/main.py) - This is the Script for the graphs that were made.
- [Click here for table creation file](https://github.com/RohrbachMatthew/Vacation_Weather/blob/main/create_table_and_index.sql) - This is a .sql file to create the database table.
- [Click here for MySQL queries made](https://github.com/RohrbachMatthew/Vacation_Weather/blob/main/avg_day_temp.sql)- This file has queries that can be used.

---
## Graphs
**Below are graphs for the vacation weather analysis**  
**Click the graph to enlarge**
<table>
  <tr>
    <td align="center">
      <strong>Average Temperature For Each Day</strong><br>
      <img src="https://github.com/RohrbachMatthew/Vacation_Weather/blob/main/img/AvgTempGraph.png" width="200"/>
    </td>
    <td align="center">
      <strong>Average Humidity Percentage For Each Day</strong><br>
      <img src="https://github.com/RohrbachMatthew/Vacation_Weather/blob/main/img/AvgDailyHumidity.png" width="200"/>
    </td>
        <td align="center">
      <strong>Weather Condition Distribution During The Trip</strong><br>
      <img src="https://github.com/RohrbachMatthew/Vacation_Weather/blob/main/img/weather_conditions.png" width="150"/>
    </td>
  </tr>
  <tr>
    <td align="center">
      <strong>Comparison of Temperatures and Humidity</strong><br>
      <img src="https://github.com/RohrbachMatthew/Vacation_Weather/blob/main/img/humidity_temperature.png" width="200"/>
    </td>
  </tr>
</table>

