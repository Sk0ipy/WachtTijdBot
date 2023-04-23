# this will get the response from the API and return it

import requests


class GetAPI:
    base_url = "https://queue-times.com/nl/parks.json"

    def __init__(self):
        self.response = requests.get(self.base_url)
        self.data = self.response.json()

    def get_data(self):
        return self.data





