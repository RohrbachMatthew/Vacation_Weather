import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt


def data_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Gigity102',
        database='vacation_weather',
        port='3307'
    )

    query = 'SELECT * FROM vacation_weather_data'
    cursor = connection.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()

    columns = [i[0] for i in cursor.description]
    return rows, columns

rows, columns = data_connection()
df = pd.DataFrame(rows, columns=columns)

total_rows = df.index.size

#print(total_rows)
#print(df)

temp_data = df['temperature']
day = df['day']

plt.figure(figsize=(15, 5))
plt.plot(temp_data, linestyle='-', marker='o', color='blue')
plt.title('Temperature During Vacation')
plt.xlabel('Day Number')
plt.ylabel('Temperature')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()