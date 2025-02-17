from locust import HttpUser, between, task
import random


class ApiUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def get_movies(self):
        self.client.get('/movies')

    @task
    def get_movie(self):
        movies = ['Avatar', 'Braveheart', 'Caroline', 'X']
        idx = random.randrange(len(movies)-1)
        self.client.get(f'/movie/{movies[idx]}')
  
