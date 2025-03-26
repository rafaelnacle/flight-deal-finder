import time
from datetime import datetime, timedelta

from pyexpat.errors import messages

from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

# Set airport origin:
ORIGIN_CITY_IATA = "LON"

# Update the airport codes in Google Sheet
for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_destination_code(row["city"])
        # Slow down request to avoid rate limit
        time.sleep(2)
print(f"Sheet Data:\n {sheet_data}")

data_manager.destination_data = sheet_data
data_manager.update_destination_codes()

# Retrieve customer emails
customer_data = data_manager.get_customer_emails()
customer_email_list = [row["whatIsYourEmail?"] for row in customer_data]

# Search for flights
tomorrow = datetime.now() + timedelta(days=1)
six_months_from_today = datetime.now() + timedelta(days=(6*30))

for destination in sheet_data:
    print(f"Getting flight for {destination['city']}...")
    flights = flight_search.check_flight(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_months_from_today
    )
    cheapest_flight = find_cheapest_flight(flights)
    print(f"{destination['city']}: £{cheapest_flight.price}")
    # Slow down request to avoid rate limit
    time.sleep(2)

    if cheapest_flight.price != "N/A":
        print(f"No direct flight to {destination['city']}. Looking for indirect flights...")

        stopover_flights = flight_search.check_flight(
            ORIGIN_CITY_IATA,
            destination["iataCode"],
            from_time=tomorrow,
            to_time=six_months_from_today,
            is_direct=False
        )

        cheapest_flight = find_cheapest_flight(stopover_flights)
        print(f"Cheapest indirect flight price is: £{cheapest_flight.price}")


    # notification_manager.send_sms(
    #     message_body=f"Low price alert! Only £{cheapest_flight.price} to fly "
    #                  f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
    #                  f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
    # )
