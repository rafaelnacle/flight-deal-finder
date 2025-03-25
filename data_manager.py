import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth

load_dotenv()

SHEETY_PRICES_ENDPOINT = "https://api.sheety.co/0280f87b4f179fca1b41989e9ec5c2da/flightDeals/prices"
TOKEN = os.getenv("SHEETY_API_TOKEN")

HEADERS = {"Authorization": f"Bearer {TOKEN}"}

class DataManager:

    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHEETY_PRICES_ENDPOINT, headers=HEADERS)
        data = response.json()
        self.destination_data = data["prices"]

        return self.destination_data
