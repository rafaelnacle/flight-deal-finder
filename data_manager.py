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

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                json=new_data,
                headers=HEADERS
            )
            print(response.text)
