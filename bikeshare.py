# Date: Created on April 22nd 2021
# Project Title: Udacity Bikeshare project
# Description: Python program to return user data and statistics from bikerental data

import time
import pandas as pd
import numpy as np
import sys

# Show version numbers for clarity in output
print("Python Version: ", sys.version)
print("Pandas Version: ", pd.__version__)
print("Numpy Version:  ", np.__version__)
print()

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
              

# Define global lists to be used for valid entries to check user inputs.
cities = ['chicago', 'new york', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (int) data_count - number of lines of raw data that the script will output for each set of stats
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print()
    print('Enter the city you want data for: Chicago, New York or Washington?')
    city = input('Enter your selection: ').lower()
    while city not in cities:    
        city = input('{} invlaid, Please try again. Chicago, New York or Washington: '.format(city)).lower()

    # get user input for month (all, january, february, ... , june)
    print()
    print('Enter the month you want data for: January, February, March, April, May, June or all?')
    month = input('Enter your selection: ').lower()
    while month not in months:    
        month = input('{} invlaid, Please try again. January, February, March, April, May, June or all?: '.format(month)).lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print()
    print('Enter the day you want data for: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all?')
    day = input('Enter your selection: ').lower()
    while day not in days:    
        day = input('{} invlaid, Please try again. Monday, Tuesday, Wednesday, Thursday, Friday, Daturday, Sunday or all?: '.format(day)).lower()
        
    # prompt user if they wish to have raw data displayed.
    data_count = 0
    print()
    print('Do you want raw data output along with stats?')
    data_required = input('Enter y for 5 lines, or any key to continue: ').lower()
    while data_required == 'y':
        data_count += 5
        data_required = input('{} lines of raw data will be printed. Enter y for 5 more lines or anykey to continue: '.format(data_count).lower())        
       
    print('-'*40)
    return city, month, day, data_count

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
    print("Getting data for {}".format(city).title())
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from raw datafram Start Time column to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int (all index 0, Jan index 1, Feb index 2 etc)
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df, city):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel for {}...\n'.format(city).title())
    start_time = time.time()

    # display the most common month
    # 'month' is already extracted to its own column in the dataframe by the load_data function - no need to extract
    # find the most popular month
    popular_month = df['month'].mode()[0]
    # Use popular_month integer to index the 'months' global list to return a valid month name
    print('Most Popular Month:', months[popular_month - 1].title())  

    # display the most common day of week
    # 'day_of_week' is already extracted to its own column in the dataframe by the load_data function  - no need to extract
    # find the most popular month
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular Day:', popular_day)

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df, city):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip for {}...\n'.format(city).title())
    start_time = time.time()

    # display most commonly used start station - Already provided in df from load_data
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station:', popular_start_station)

    # display most commonly used end station - Already provided in df from load_data
    popular_end_station = df['End Station'].mode()[0]
    print('Most Common End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    # Creating a concatination of all start and end stations in the dataframe to a new single string 'combination'
    df['combination'] = df['Start Station'] + ' to ' + df['End Station']
    # Using Mode()[0] to find the most common occurences of the concatinated string
    print('The most frequent combination of start station and end station per trip is:\n{}'.format((df['combination'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df, city):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration Stats for {}...\n'.format(city).title())
    start_time = time.time()

    # display total travel time. 'Trip Duration' is provided in the dataframe. Use sum() for the total - convert seconds to hrs & mins
    total_triptime = df['Trip Duration'].sum()
    triptime_days = total_triptime / 86400 # Seconds per day (60 * 60 * 24)
    print('Total Travel time: {} secs or {} days'.format(total_triptime, triptime_days))

    # display mean travel time. 'Trip Duration' is provided in the dataframe. Use sum() for the total - convert seconds to hrs & mins
    mean_triptime = df['Trip Duration'].mean()
    mean_triptime_days = mean_triptime / 60 # Seconds per min
    print('Mean Travel time: {} secs or {} mins'.format(mean_triptime, mean_triptime_days))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats for {}...\n'.format(city).title())
    start_time = time.time()

    # Display counts of user types but first replace NaN with 'None'
    replace_nan_user = df['User Type'].fillna('None')
    user_types = replace_nan_user.value_counts()
    print(user_types)
        
    # if-else to check the city. If its washington display message no gender or birth data.
    if city != 'washington':
        # Display counts of gender but first replace NaN with 'None'
        replace_nan_gender = df['Gender'].fillna('None')
        gender_count = replace_nan_gender.value_counts()
        print()
        print(gender_count)
        # Display earliest, most recent, and most common year of birth
        print('\nEarliest birth year: ', df['Birth Year'].min())
        print('Latest birth year: ', df['Birth Year'].max())
        print('Most Common birth year: ', df['Birth Year'].mode()[0])
    else:
        print('\nNo Gender or Birth date data available for Washington')

        print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40) 

def print_data(df, data_count, city, stats):
    # Prints the current dataframe in use for stats calcs based on the 'data_count' from the user.
    if data_count == 0:
        print('\nNo raw Data requested by user for {}'.format(city.title()))
    else:
        print('\n{} data for {}'.format(city.title(), stats))
        print(df.iloc[0:data_count])
 
def main():
    while True:
        # Get user inputs
        city, month, day, data_count  = get_filters()
        # Create the filtered or unflitered dataframe based on the user inputs 
        df = load_data(city, month, day)
        
        # Calculate and print the required statistics. Adding print_data function to print raw data if required by user
        stats = 'Trip Time Stats'
        print_data(df, data_count, city, stats)
        time_stats(df, city)
 
        stats = 'Station Stats'
        print_data(df, data_count, city, stats)
        station_stats(df, city)
 
        stats = 'Trip Duration Stats'
        print_data(df, data_count, city, stats)
        trip_duration_stats(df, city)
        
        stats = 'User Stats'
        print_data(df, data_count, city, stats)
        user_stats(df, city)
        
        # Check if user wants more stats or any key to exit.
        restart = input('\nWould you like to restart? Enter yes or any key to quit.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()