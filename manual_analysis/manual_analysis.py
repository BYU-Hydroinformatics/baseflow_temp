import pandas as pd
import matplotlib.pyplot as plt


def average_yearly_duration (data):

    # Load the data from the CSV file
    data = pd.read_csv(data)

    # Convert date columns to datetime objects
    data['start_date'] = pd.to_datetime(data['start_date'])
    data['end_date'] = pd.to_datetime(data['end_date'])

    # Calculate the time duration for each period (in days, you can change it to weeks, months, etc.)
    data['duration_days'] = (data['end_date'] - data['start_date']).dt.days

    # Group the data by different time periods (e.g., annually)
    annual_groups = data.groupby(data['start_date'].dt.year)

    # Calculate statistics for each group (e.g., mean duration)
    annual_stats = annual_groups['duration_days'].mean()

    # Visualize the annual pattern (you can change it to other periods)
    plt.figure(figsize=(10, 6))
    annual_stats.plot(kind='bar', title='Average Duration of Periods Annually')
    plt.xlabel('Year')
    plt.ylabel('Average Duration (days)')
    plt.show()


def total_monthly_duration (data):

    # Load the data from the CSV file
    data = pd.read_csv(data)

    # Convert date columns to datetime objects
    data['start_date'] = pd.to_datetime(data['start_date'])
    data['end_date'] = pd.to_datetime(data['end_date'])

    # Calculate the time duration for each period (in days)
    data['duration_days'] = (data['end_date'] - data['start_date']).dt.days

    # Group the data by month
    data['month'] = data['start_date'].dt.month
    monthly_groups = data.groupby('month')

    # Calculate the total duration for each month
    monthly_totals = monthly_groups['duration_days'].sum()

    # Visualize the monthly pattern
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    plt.figure(figsize=(10, 6))
    monthly_totals.index = [months[i - 1] for i in monthly_totals.index]  # Assign month names to the index
    monthly_totals.plot(kind='bar', title='Total Duration of Periods by Month')
    plt.xlabel('Month')
    plt.ylabel('Total Duration (days)')
    plt.show()


def total_yearly_duration(data):

    # Load the data from the CSV file
    data = pd.read_csv('manually.csv')

    # Convert date columns to datetime objects
    data['start_date'] = pd.to_datetime(data['start_date'])
    data['end_date'] = pd.to_datetime(data['end_date'])

    # Calculate the time duration for each period (in days)
    data['duration_days'] = (data['end_date'] - data['start_date']).dt.days

    # Group the data by year
    data['year'] = data['start_date'].dt.year
    yearly_groups = data.groupby('year')

    # Calculate the total duration for each year
    yearly_totals = yearly_groups['duration_days'].sum()

    # Visualize the yearly totals
    plt.figure(figsize=(10, 6))
    yearly_totals.plot(kind='bar', title='Total Duration of Periods by Year')
    plt.xlabel('Year')
    plt.ylabel('Total Duration (days)')
    plt.show()


def total_seasonal_duration(data):

    # Load the data from the CSV file
    data = pd.read_csv('manually.csv')

    # Convert date columns to datetime objects
    data['start_date'] = pd.to_datetime(data['start_date'])
    data['end_date'] = pd.to_datetime(data['end_date'])

    # Calculate the time duration for each period (in days)
    data['duration_days'] = (data['end_date'] - data['start_date']).dt.days

    # Define the mapping of months to seasons
    season_mapping = {
        1: 'Winter',
        2: 'Winter',
        3: 'Spring',
        4: 'Spring',
        5: 'Spring',
        6: 'Summer',
        7: 'Summer',
        8: 'Summer',
        9: 'Autumn',
        10: 'Autumn',
        11: 'Autumn',
        12: 'Winter',
    }

    # Assign the season to each row based on the start date
    data['season'] = data['start_date'].dt.month.map(season_mapping)

    # Group the data by season
    season_groups = data.groupby('season')

    # Calculate the total duration for each season
    season_totals = season_groups['duration_days'].sum()

    # Visualize the season totals
    plt.figure(figsize=(10, 6))
    season_totals.plot(kind='bar', title='Total Duration of Periods by Season')
    plt.xlabel('Season')
    plt.ylabel('Total Duration (days)')
    plt.show()
