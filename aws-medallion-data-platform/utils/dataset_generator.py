import os
import random
from datetime import datetime, timedelta

import pandas as pd


random.seed(42)


class DatasetGenerator:

    def __init__(self):

        self.cities = [
            "Mumbai","Delhi","Bangalore","Chennai","Hyderabad",
            "Kolkata","Pune","Ahmedabad","Jaipur","Goa"
        ]

        self.countries = [
            "India","USA","UK","Germany","France",
            "Canada","Australia","Singapore","Japan","UAE"
        ]

        self.flight_classes = [
            "Economy",
            "Premium Economy",
            "Business",
            "First"
        ]

    def generate_airports(self, rows=500):

        data = []

        for airport_id in range(1, rows + 1):

            city = random.choice(self.cities)
            country = random.choice(self.countries)

            data.append([
                airport_id,
                f"{city} International Airport",
                city,
                country,
                f"AP{airport_id:03}"
            ])

        return pd.DataFrame(
            data,
            columns=[
                "airport_id",
                "airport_name",
                "city",
                "country",
                "iata_code"
            ]
        )

    def generate_passengers(self, rows=10000):

        data = []

        for passenger_id in range(1, rows + 1):

            data.append([
                passenger_id,
                f"First{passenger_id}",
                f"Last{passenger_id}",
                random.choice(["Male", "Female"]),
                random.choice(self.countries),
                random.randint(18, 75)
            ])

        return pd.DataFrame(
            data,
            columns=[
                "passenger_id",
                "first_name",
                "last_name",
                "gender",
                "nationality",
                "age"
            ]
        )

    def generate_bookings(self, rows=100000):

        data = []

        start_date = datetime(2025, 1, 1)

        for booking_id in range(1, rows + 1):

            booking_date = start_date + timedelta(
                days=random.randint(0, 365)
            )

            data.append([
                booking_id,
                random.randint(1, 10000),
                random.randint(1, 500),
                booking_date.strftime("%Y-%m-%d"),
                round(random.uniform(100, 2000), 2),
                random.choice(self.flight_classes)
            ])

        return pd.DataFrame(
            data,
            columns=[
                "booking_id",
                "passenger_id",
                "airport_id",
                "booking_date",
                "ticket_price",
                "flight_class"
            ]
        )


if __name__ == "__main__":

    os.makedirs("datasets", exist_ok=True)

    generator = DatasetGenerator()

    generator.generate_airports().to_csv(
        "datasets/airports.csv",
        index=False
    )

    generator.generate_passengers().to_csv(
        "datasets/passengers.csv",
        index=False
    )

    generator.generate_bookings().to_csv(
        "datasets/bookings.csv",
        index=False
    )

    print("Datasets generated successfully")