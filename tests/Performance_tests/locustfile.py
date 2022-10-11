from locust import HttpUser, task


mess_toolong = "Request took too long..."


class PerfTest(HttpUser):
    @task
    def index_page(self):
        with self.client.get("/", catch_response=True) as response:
            if response.elapsed.total_seconds() > 5:
                response.failure(mess_toolong)

    @task
    def showSummary_page(self):
        form = {'email': "john@simplylift.co"}
        with self.client.post("/showSummary", data=form, catch_response=True) as response:
            if response.elapsed.total_seconds() > 5:
                response.failure(mess_toolong)

    @task
    def book_page(self):
        with self.client.get('/book/Spring%20Festival/Simply%20Lift',
                             catch_response=True) as response:
            if response.elapsed.total_seconds() > 5:
                response.failure(mess_toolong)

    @task
    def purchase_page(self):
        form = {'club': "Simply Lift",
                'competition': "Spring Festival",
                'places': 5}
        with self.client.post("/purchasePlaces", data=form,
                              catch_response=True) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure(mess_toolong)

    @task
    def board_page(self):
        with self.client.get("/pointsBoard",
                             catch_response=True) as response:
            if response.elapsed.total_seconds() > 5:
                response.failure(mess_toolong)

    @task
    def logout_page(self):
        with self.client.get("/logout",
                             catch_response=True) as response:
            if response.elapsed.total_seconds() > 5:
                response.failure(mess_toolong)
