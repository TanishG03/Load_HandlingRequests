from locust import HttpUser, task, between, stats
import locust.stats
import time
import sqlite3
import psutil

locust.stats.CSV_STATS_INTERVAL_SEC = 5 # default is 1 second
locust.stats.CSV_STATS_FLUSH_INTERVAL_SEC = 60

class MyUser(HttpUser):
    wait_time = between(1, 3)
    # host = "https://jsonplaceholder.typicode.com"
    host="http://127.0.0.1:3000/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = None
        self.request_data = {}
        self.cpu_data = {}
        self.timer_start = time.time()

        # self.create_tables()

        # Confirm database formation
        # self.confirm_database()

    def create_tables(self):
        connection = sqlite3.connect("locust_data.db")
        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_name TEXT,
                request_count INTEGER,
                avg_response_time REAL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cpu_utilization (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_name TEXT,
                avg_cpu_percent REAL
            )
        ''')

        connection.commit()
        connection.close()

    def confirm_database(self):
        connection = sqlite3.connect("locust_data.db")
        cursor = connection.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        print("Tables in the database:")
        for table in tables:
            print(table[0])

        connection.close()

    def store_data(self, request_data, cpu_data):
        connection = sqlite3.connect("locust_data.db")
        cursor = connection.cursor()

        for name, data in request_data.items():
            avg_response_time = sum(data["response_times"]) / len(data["response_times"])
            cursor.execute(
                "INSERT INTO requests (request_name, request_count, avg_response_time) VALUES (?, ?, ?)",
                (name, data["count"], avg_response_time),
            )

        for name, data in cpu_data.items():
            avg_cpu_percent = sum(data["cpu_percent"]) / len(data["cpu_percent"])
            cursor.execute(
                "INSERT INTO cpu_utilization (request_name, avg_cpu_percent) VALUES (?, ?)",
                (name, avg_cpu_percent),
            )

        connection.commit()
        connection.close()

    def on_start(self):
        self.start_time = time.time()

    def on_stop(self):
            # print(self.request_data)
            # self.store_data(self.request_data, self.cpu_data)
            self.start_time = time.time()
    



    def on_request_success(self, request_type, name, response_time, response_length):
        if name not in self.request_data:
            self.request_data[name] = {"count": 0, "response_times": []}
        self.request_data[name]["count"] += 1
        self.request_data[name]["response_times"].append(response_time)

    @task
    def get_post_1(self):
        self.perform_request("get_post_1", "posts/1")

    @task
    def get_post_2(self):
        self.perform_request("get_post_2", "posts/2")

    @task
    def get_albums(self):
        self.perform_request("get_albums", "albums")

    @task
    def get_photos(self):
        self.perform_request("get_photos", "photos")

    @task
    def get_comments(self):
        self.perform_request("get_comments", "comments")
    
    @task
    def get_comments1(self):
        self.perform_request("get_comments1", "comments/1")
    @task
    def get_comments2(self):
        self.perform_request("get_comments2", "comments/2")

    

    def perform_request(self, name, endpoint):
        with self.client.get(endpoint, catch_response=True) as response:
            self.handle_response(response, name)

    def handle_response(self, response, name):
        response_time = response.elapsed.total_seconds()
        print(name,response_time)

        if name not in self.request_data:
            self.request_data[name] = {"count": 0, "response_times": []}

        self.request_data[name]["count"] += 1
        self.request_data[name]["response_times"].append(response_time)

        cpu_percent = psutil.cpu_percent(interval=0.1)  # Adjust the interval as needed

        if name not in self.cpu_data:
            self.cpu_data[name] = {"count": 0, "cpu_percent": []}

        self.cpu_data[name]["count"] += 1
        self.cpu_data[name]["cpu_percent"].append(cpu_percent)


