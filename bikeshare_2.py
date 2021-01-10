import calendar
import pandas as pd
import time

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_NAMES = list(calendar.month_name)[1:]
DAY_NAMES = list(calendar.day_name)

def is_y_or_n(answer): 
    lowered_answer = answer.lower()
    return lowered_answer == 'y' or lowered_answer == 'n'

def prompt_user_confirmation(question):
    while True:
        answer = input(question)
        if is_y_or_n(answer):
            break
    return answer

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    city = None
    month = None
    day = None
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Enter enter one of the city name (chicago, new york city, washington): ').lower()
        if city in CITY_DATA:
            break

    # get user input for month (all, january, february, ... , june)
    should_filter_by_month = prompt_user_confirmation('Would you like to filter by "month"? (y/n) ')
    if should_filter_by_month == 'y':
        while True:
            filter_by_month = input('Please enter month: (all, january, february, ... , june): ')
            valid_month_input_filters = ['All', *MONTH_NAMES]
            if filter_by_month.title() in valid_month_input_filters:
                month = filter_by_month
                break
            else:
                print('[Invalid Input] please try again.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    should_filter_by_day = prompt_user_confirmation('Would you like to filter by "day"? (y/n) ')
    if should_filter_by_day == 'y':
        while True:
            filter_by_day = input('Please enter day of week (all, monday, tuesday, ... sunday): ')
            valid_day_input_filters = ['All', *DAY_NAMES]
            if filter_by_day.title() in valid_day_input_filters:
                day = filter_by_day
                break
            else:
                print('[Invalid Input] please try again.')

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
    df = pd.read_csv("{}.csv".format(city.replace(" ", "_")))
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Start Month'] = df['Start Time'].dt.month_name()
    df['Start Day'] = df['Start Time'].dt.day_name()
    df['Start Hour'] = df['Start Time'].dt.hour

    if month and month.lower() != 'all':
        df = df[df['Start Month'] == month.title()]

    if day and day.lower() != 'all':
        df = df[df['Start Day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('\nMost common month: {}'.format(df['Start Month'].mode()[0]))

    # display the most common day of week
    print('\nMost common day of week: {}'.format(df['Start Day'].mode()[0]))

    # display the most common start hour
    print('\nMost common start hour: {}'.format(df['Start Hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_commonly_used_start_station = df['Start Station'].mode()[0]
    print('\nThe most commonly used start station: {}\n'.format(most_commonly_used_start_station))

    # display most commonly used end station
    most_commonly_used_end_station = df['End Station'].mode()[0]
    print('\nThe most commonly used end station: {}\n'.format(most_commonly_used_end_station))

    # display most frequent combination of start station and end station trip
    most_frequent_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    most_frequent_combination_msg_tpl = '\nThe most frequent combination of start station is "{}" and end station is "{}" trip: \n'

    print(most_frequent_combination_msg_tpl.format(most_frequent_combination[0], most_frequent_combination[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('\nTotal travel time: {}\n'.format(df['Trip Duration'].sum()))

    # display mean travel time
    print('\nMean travel time: {}\n'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """
    Displays statistics on bikeshare users.

    Args:
        (pandas.core.frame.DataFrame) - filtered dataframe
        (str) city - name of the city to analyze
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nCount by user types:\n')
    print(df['User Type'].value_counts())

    if city.lower() in ['chicago', 'new york city']: 
        # display counts of each gender (only available for NYC and Chicago)
        print('\nCount by gender:\n')
        print(df['Gender'].value_counts())

        # Display earliest, most recent, and most common year of birth (only available for NYC and Chicago)
        earliest_yob = int(df['Birth Year'].min(skipna=True))
        most_recent_yob = int(df['Birth Year'].max(skipna=True))
        most_commont_yob = int(df['Birth Year'].mode()[0])
        print('\n Earliest year of birth: {}\n'.format(earliest_yob))
        print('\n Most recent year of birth: {}\n'.format(most_recent_yob))
        print('\n Most common year of birth: {}\n'.format(most_commont_yob))
    else:
        print('Count by gender and year of birth details only available for NYC and Chicago')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    should_filter_by_month = prompt_user_confirmation('Would you like see 5 lines of raw data? (y/n) ')
    if should_filter_by_month == 'y':
        print(df.head())

        rows_per_page = 5
        total_rows = df.shape[0]
        next_start_index = 6

        if total_rows - rows_per_page > 0:
            while len(df.iloc[next_start_index:]) > 0:
                remaining_rows = len(df.iloc[next_start_index:])
                show_more_msg = 'There are {} / {} rows of data left. Would like to see another {} more lines of raw data? (y/n) '.format(remaining_rows, total_rows, rows_per_page)
                show_more_ans = prompt_user_confirmation(show_more_msg)
                if show_more_ans == 'y':
                    checkpoint = next_start_index + rows_per_page
                    rows_to_print = df.iloc[next_start_index:checkpoint + 1]
                    print(rows_to_print)
                    next_start_index = checkpoint + rows_per_page
                else:
                    break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        """ display stats only when there is results to prevent gettin error """
        if len(df.index) > 0:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df, city)
            display_raw_data(df)
        else:
            print('- No results found -')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
