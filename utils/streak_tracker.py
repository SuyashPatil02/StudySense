import pandas as pd
from datetime import timedelta


def calculate_streak(df):
    if df.empty:
        return 0

    unique_dates = sorted(df["date"].dt.date.unique())
    if not unique_dates:
        return 0

    streak = 1
    for i in range(len(unique_dates) - 1, 0, -1):
        if unique_dates[i] - unique_dates[i - 1] == timedelta(days=1):
            streak += 1
        else:
            break

    return streak