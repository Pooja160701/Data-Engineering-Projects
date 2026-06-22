import pandas as pd

def test_booking_dataset():

    df = pd.read_csv("datasets/bookings.csv")

    assert len(df) > 0

    assert df["booking_id"].isnull().sum() == 0

    assert df["ticket_price"].min() > 0