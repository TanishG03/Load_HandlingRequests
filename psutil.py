from locust import HttpUser, task, between
import sqlite3
import time

class MyUser(HttpUser):
    wait_time = between(1, 3)

    host = "http://127.0.0.1:3000/"
    host_secondary = "http://127.0.0.1:3001/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_request_names = []

    def fetch_response_time(self):
        connection = sqlite3.connect("locust_data.db")
        cursor = connection.cursor()

        cursor.execute("SELECT DISTINCT Name, Average_Response_Time FROM response_times ORDER BY Average_Response_Time DESC LIMIT 2")
        top_response_time = cursor.fetchall()
        # print(top_response_time)

        connection.close()

        return top_response_time

    def on_start(self):
        response_time_data = self.fetch_response_time()

        self.max_request_names = [name.lstrip('/') for name, _ in response_time_data]
        


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
        if endpoint in self.max_request_names:

            self.client.base_url = self.host_secondary
            print(f"Redirecting request {endpoint} to the secondary server")

            with self.client.get(endpoint, catch_response=True) as response:
                self.handle_response(response, name)

        else:
            self.client.base_url = self.host
            print(f"Redirecting request {endpoint} to the primary server")

            with self.client.get(endpoint, catch_response=True) as response:
                self.handle_response(response, name)
  

    def handle_response(self, response, name):
        response_time = response.elapsed.total_seconds()
        print(name, response_time)
