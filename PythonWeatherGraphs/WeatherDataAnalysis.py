import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt


def data_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Password1',
        database='vacation_weather',
        port='3307'
    )
    return connection

def daily_average_temp():
    connection = data_connection()
    query = """with daily_average AS (
             SELECT day, date, avg(temperature) AS avg_daily_temp
             from vacation_weather_data
             GROUP BY day, date)
             Select day, count(*) as num_days,
             round(AVG(avg_daily_temp),2) AS avg_temp
             from daily_average
             group by day
             order by field(day, 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')"""

    cursor = connection.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()

    columns = [i[0] for i in cursor.description]

    df = pd.DataFrame(rows, columns=columns)

    # Checked to see how many rows
    #total_rows = df.index.size

    #print(total_rows)
    #print(df)

    temp_data = df['avg_temp']
    day = df['day']

    plt.figure(figsize=(15, 5))
    plt.plot(day, temp_data, linestyle='-', marker='o', color='blue')
    plt.title('Temperature During Vacation')
    plt.xlabel('Day Of Week')
    plt.ylabel('Temperature')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    cursor.close()
    connection.close()

def avg_daily_humidity():
    connection = data_connection()
    query = """with humidity_avg as(
select day, date, avg(humidity) as avg_daily_humidity
from vacation_weather_data
group by day, date)

-- Average by the day
select day, round(AVG(avg_daily_humidity),2) as avg_daily_humidity
from humidity_avg
group by day
order by field(day, 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')"""
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [i[0]for i in cursor.description]

    df = pd.DataFrame(rows, columns=columns)
    humidity_avg = df['avg_daily_humidity']
    day = df['day']
    plt.figure(figsize=(10, 5))
    plt.plot(day, humidity_avg, linestyle='-', marker='o', color='red')
    plt.title('AVG Daily Humidity')
    plt.xlabel('Day Of The Week')
    plt.ylabel('Humidity Percentage')
    plt.grid(True)
    plt.show()


    #print(df)

    cursor.close()
    connection.close()

def daily_conditions():
    connection = data_connection()
    cursor = connection.cursor()

    query = ("""
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
    """)

    cursor.execute(query)

    rows = cursor.fetchall()
    columns = [i[0] for i in cursor.description]

    df = pd.DataFrame(rows, columns=columns)
    conditions_avg = df['conditions'].value_counts()

    plt.figure(figsize=(10, 5))
    plt.pie(conditions_avg, labels=conditions_avg.index,
    autopct='%1.1f%%',
    startangle=90,
    colors=['lightblue', 'brown', 'grey'])
    plt.title('Weather Condition Distribution')
    plt.show()


def temp_humidity_combined():
    connection = data_connection()
    cursor = connection.cursor()

    query = """
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
ORDER BY FIELD(day, 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')
    """
    cursor.execute(query)

    rows = cursor.fetchall()
    columns = [i[0] for i in cursor.description]
    df = pd.DataFrame(rows, columns=columns)
    #print(df)

    days = df['day']
    temp = df['avg_daily_temp']
    humidity = df['avg_daily_humidity']
    plt.figure(figsize=(10, 5))
    plt.plot(days, humidity, linestyle='-', marker='o', color='red', label='humidity')
    plt.plot(days, temp, linestyle='-', marker='o', color='blue', label='temperature')

    plt.title('Temperature And Humidity')
    plt.legend()
    plt.show()

# Remove '#' to show graph
#daily_average_temp()
#avg_daily_humidity()
#daily_conditions()
temp_humidity_combined()