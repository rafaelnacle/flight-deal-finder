import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth

load_dotenv()

SHEETY_PRICES_ENDPOINT = "https://api.sheety.co/0280f87b4f179fca1b41989e9ec5c2da/flightDeals/prices"

class DataManager:

    def __init__(self):
        self._token = os.environ["SHEETY_TOKEN"]
        self._authorization = HTTPBasicAuth(self._token)
        self.destination_data = {}
