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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    city = input('For which city do you want to see the data: Chicago, New York City or Washington?').lower()
    cities = ['chicago', 'new york city', 'washington']
    while city.lower() not in cities:
        city = input('This city is not available for selection. Please select: Chicago, New York City or Washington.')

    # get user input for month (all, january, february, ... , june)
                 
    month = input('Please choose a month: January, February, March, April, May, June or all.').lower()
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while month.lower() not in months:
        month = input('Please select a month to choose from: January, February, March, April, May, June or all.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please choose a day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all.').lower()
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while day.lower() not in days:
        day = input('Please select a day of the week: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all.')
    
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
    df = pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()
    print ('The most common month is:{}'.format(common_month))

    # display the most common day of week
    common_day = df['day'].mode()
    print ('The most common day is:{}'.format(common_day))

    # display the most common start hour
    df['hour']= df['Start Time'].dt.hour
    common_hour = df['hour'].mode()
    print ('The most common day of hour is {}'.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start= df['Start Station'].mode()
    print ('The most commonly used start station is: {}.'.format(common_start))

    # display most commonly used end station
    common_end= df['End Station'].mode()
    print ('The most commonly used end station is: {}.'.format(common_end))

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + df['End Station']
    combination_trip = df['Trip'].mode()
    print ('The most frequent combination of start station and end station trip: {}.'.format(combination_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['trip duration'] = df['End Time'] - df['Start Time']
    total_time = df['trip duration'].sum()
    print('The total trip duration is {}.'.format(total_time))

    # display mean travel time
    average_time = df['trip duration'].mean()
    print('The average travel time is {}.'.format(average_time))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print('Count of user type:')
    print(user_type)

    # Display counts of gender
    if city != 'washington':
        print('Gender Stats:')
        print(df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    if city != 'washington':
        min_birth = df['Birth Year'].min()
        max_birth = df['Birth Year'].max()
        common_birth = df['Birth Year'].mode()
        print('The earliest year of birth is {}, the most recent year of birth is {}, the most common year of birth is    {}'.format(min_birth, max_birth, common_birth))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def raw_data(df):
    i=0
    user_question=input('Would you like to see 5 lines of raw data? Please type "y" or "n".').lower()
    while user_question in ['yes','y','yep','yea'] and i+5 < df.shape[0]:
        print(df.iloc[i:i+5])
        i += 5
        user_question = input('Would you like to see more data? Please enter "y" or "n":').lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
       
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
