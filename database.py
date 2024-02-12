

import sqlite3
from collections import defaultdict
import csv


csv_file_path = "output_stats.csv"

# Create an SQLite database
connection = sqlite3.connect("locust_data.db")
cursor = connection.cursor()

# Create the response_time table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS response_times (
        Name TEXT,
        Request_Count INTEGER,
        Median_Response_Time REAL,
        Average_Response_Time REAL,
        Min_Response_Time REAL,
        Max_Response_Time REAL
    )
''')

# Read data from the CSV file and insert it into the response_time table
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        cursor.execute('''
            INSERT OR IGNORE INTO response_times VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            row['Name'], int(row['Request Count']),
            float(row['Median Response Time']), float(row['Average Response Time']),
            float(row['Min Response Time']), float(row['Max Response Time'])
        ))

# Commit the changes and close the connection
connection.commit()
connection.close()

print("Database and table created successfully.")



def fetch_cpu_data():
    connection = sqlite3.connect("locust_data.db")
    cursor = connection.cursor()

    # Fetch CPU utilization data
    cursor.execute("SELECT request_name, AVG(avg_cpu_percent) FROM cpu_utilization GROUP BY request_name")
    cpu_data = cursor.fetchall()

    connection.close()

    return cpu_data

# Example usage
cpu_data = fetch_cpu_data()

# Print or process the aggregated CPU utilization data as needed
print("Aggregated CPU Utilization Data:")
for row in cpu_data:
    request_name, avg_cpu_percent = row
    print(f"Request: {request_name}, Average CPU Utilization: {avg_cpu_percent}%")

def fetch_response_time():
    connection = sqlite3.connect("locust_data.db")
    cursor = connection.cursor()

    # Fetch CPU utilization data
    cursor.execute("SELECT DISTINCT Name, Average_Response_Time from response_times")
    cpu_data = cursor.fetchall()

    connection.close()

    return cpu_data

response_time=fetch_response_time()
# for row in response_time:
#     name, time=row
#     print(f"Request: {name}, Average response time: {response_time}")

print(response_time)
# Example usage

