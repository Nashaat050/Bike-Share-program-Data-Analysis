import time
import pandas as pd

CITY_DATA = {"chicago": "chicago.csv",
             "new york city": "new_york_city.csv",
             "washington": "washington.csv"}


def get_filters():
    cities = ["chicago", "new york city", "washington"]
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]

    while True:
        city = str(input("choose a city to explore (chicago, new york city, washington)\n")).lower()
        if city.lower() in cities:
            break
        else:
            print("wrong choice . Please try again")

    while True:
        month = str(input(
            "choose a month or all to apply no month filter! (january,february, march,april,may,june)\n")).lower()
        if month.lower() in months:
            break
        else:
            print('wrong choice. Please try again')

    while True:
        day = str(input(
            "Insert day of the week or all to no filter\n"
            "(monday,tuesday,wednesday,thursday,friday,saturday,sunday)\n")).lower()
        if day.lower() in days:
            break
        else:
            print("wrong choice. Please try again")

    print("_" * 40)
    return city, month, day


def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.day_name()
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df["month"] == month]
    if day != 'all':
        df = df[df["day_of_week"] == day.title()]
    return df


def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df["hour"] = df["Start Time"].dt.hour

    print("the most common month is {} \nthe most common day is {} \nthe most common start hour is {}"
          .format(df["month"].mode()[0], df["day_of_week"].mode()[0], df["hour"].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    trip = df["Start Station"] + df["End Station"]

    print("the most commonly used start station is {}\nthe most common end station is {}\nthe most frequent trip is {}"
          .format(df["Start Station"].mode()[0], df["End Station"].mode()[0], trip.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print("Total travel time is {}\nthe mean travel time is {}"
          .format(df["Trip Duration"].sum(), df["Trip Duration"].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    if "Gender" and "Birth Year" in df:
        print("counts of users types is {}\ncounts of gender is {}"
              .format(df["User Type"].value_counts(), df["Gender"].value_counts()))
        print("the earliest year of birth is {}\nthe recent year is {}\n& the most common year is {}"
              .format(int(df["Birth Year"].min()),
                      int(df["Birth Year"].max()),
                      int(df["Birth Year"].mode()[0])))
    else:
        print('Gender stats cannot be calculated because Gender and Birth Year does not appear in the dataframe')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_data(df):
    view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?").lower()
    start_loc = 0
    while view_data == "yes":
        start_loc += 5
        print(df.iloc[0:start_loc])
        view_display = input("Do you wish to continue?: ").lower()
        if view_display == "yes":
            continue
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
