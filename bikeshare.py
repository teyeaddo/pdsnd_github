import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    valid_cities = ['chicago', 'new york city', 'washington']
    city = input('Would you like to see data for Chicago, New York City, or Washington? ').lower()
    
    while city not in valid_cities:
        print('Invalid input. You must choose Chicago, New York City, or Washington.')
        city = input('Would you like to see data for Chicago, New York City, or Washington? ').lower()

    month = input('Which month? January, February, March, April, May, or June? ').lower()
    while month not in ['january', 'february', 'march', 'april', 'may', 'june']:
        print('Invalid input. You must choose a month from January to June.')
        month = input('Which month? January, February, March, April, May, or June? ').lower()
        
    day = input('Which day of the week? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? ').lower()

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Loads data file into a DataFrame
    df = pd.read_csv(CITY_DATA[city])
    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # Filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        # Filter by day of week to create the new DataFrame
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    common_month = df['month'].mode()[0]
    print('The most common month:', common_month)

    # Display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most common day of the week:', common_day)

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('The most common start hour:', common_hour)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display the most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station:', common_start_station)

    # Display the most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station:', common_end_station)

    # Display the most common trip
    trip_counts = df.groupby(['Start Station', 'End Station']).size()
    if not trip_counts.empty:
        common_trip = trip_counts.idxmax()
        print('The most common trip:', common_trip[0], 'to', common_trip[1])
    else:
        print('No trip data available for this selection.')


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time:', total_travel_time)

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of User Types:')
    print(user_types)

    try:
        # Display counts of gender
        gender_counts = df['Gender'].value_counts()
        print('Counts of Gender:\n', gender_counts)
    except KeyError:
        print('Error: Gender data not available for this city.')

    try:
        # Display earliest, most recent, and most common year of birth
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print('The earliest year of birth:', earliest_year)
        print('The most recent year of birth:', most_recent_year)
        print('The most common year of birth:', common_year)
    except KeyError:
        print('Error: Birth year data not available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """Asks user if they prefer to see raw data."""
    i = 0
    raw = input("Do you wish to see the raw data?").lower()

    while True:            
        if raw == 'no':
            break
        elif raw == 'yes':
            print(df[i:i+5])
            raw = input("Do you wish to see the next 5 rows of raw data?").lower()
            i += 5
        else:
            raw = input("\nInvalid input. Please enter only 'yes' or 'no'\n").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
