import os
from dotenv import load_dotenv
import requests

load_dotenv()

SHEETY_PRICES_ENDPOINT = os.getenv("SHEETY_PRICES_ENDPOINT")
SHEETY_USERS_ENDPOINT = os.getenv("SHEETY_USERS_ENDPOINT")
TOKEN = os.getenv("SHEETY_API_TOKEN")

HEADERS = {"Authorization": f"Bearer {TOKEN}"}

class DataManager:

    def __init__(self):
        self.prices_endpoint = SHEETY_PRICES_ENDPOINT
        self.users_endpoint = SHEETY_USERS_ENDPOINT
        self.destination_data = {}
        self.customer_data = {}

    def get_destination_data(self):
        response = requests.get(url=self.prices_endpoint, headers=HEADERS)
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
                url=f"{self.prices_endpoint}/{city['id']}",
                json=new_data,
                headers=HEADERS
            )
            print(response.text)

    def get_customer_emails(self):
        response = requests.get(url=self.users_endpoint, headers=HEADERS)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data