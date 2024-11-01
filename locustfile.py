from locust import HttpUser, TaskSet, task, between

class MyTask(TaskSet):
    @task(1)
    def get_items(self):
        self.client.get("/item")

    @task(2)
    def create_items(self):
        self.client.post("/items",json={"name":"test item","description": "A test item", "price": 9.99, "tax": 1.5})

class WebSiteUser(HttpUser):
    tasks = [MyTask]
    wait_time = between(1,5)
