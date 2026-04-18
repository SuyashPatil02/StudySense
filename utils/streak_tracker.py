import pandas as pd
from datetime import timedelta, datetime

def calculate_streak(df):
    if df.empty:
        return 0

    # Convert to datetime (important)
    df["date"] = pd.to_datetime(df["date"])

    # Get unique sorted dates
    unique_dates = sorted(df["date"].dt.date.unique())

    if not unique_dates:
        return 0

    today = datetime.now().date()
    last_date = unique_dates[-1]

    # If last study is too old → reset streak
    if (today - last_date).days > 1:
        return 0

    streak = 1

    for i in range(len(unique_dates) - 1, 0, -1):
        if unique_dates[i] - unique_dates[i - 1] == timedelta(days=1):
            streak += 1
        else:
            break

    return streak