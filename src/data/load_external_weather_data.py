import pycristoforo as pyc
import numpy as np
import json
import urllib
import pandas as pd
import folium
from IPython.display import display
np.random.seed(42)

# API Key = UCRVR9PAQESM7V7FZBZKP558F


def generate_coordinates(country="Spain", num_points=5):
    country_shape = pyc.get_shape(country)
    points = pyc.geoloc_generation(country_shape, num_points, country)
    # Code produces coordinates the wrong way round which must be rectified
    coordinates_wrong = [point['geometry']['coordinates'] for point in points]
    for c in coordinates_wrong:
        c[0], c[1] = c[1], c[0]
    return coordinates_wrong


def get_historical_conditions(latitude,
                              longitude,
                              date_begin, date_end,
                              api_key,
                              hourly_data,
                              interval):
    api_conditions_url = "https://api.weatherstack.com/historical" +\
                         '?access_key=' + api_key +\
                         '&query=' +\
                         str(latitude) + ',' + str(longitude) +\
                         '&historical_date_start=' + date_begin +\
                         '&historical_date_end=' + date_end +\
                         '&units=m' +\
                         '&interval=' + str(interval)
    if hourly_data:  # If we only want to see daily data and not hourly data
        api_conditions_url = api_conditions_url + '&hourly=1'
    try:  # get conditions from visualcrossing API
        f = urllib.request.urlopen(api_conditions_url)
    except:
        return 'url request did not work'
    print(api_conditions_url)

    json_currently = f.read()
    f.close()
    return json.loads(json_currently)


def plot_points(coordinates):
    """
    Plot all the coordinates of the randomized points on a map
    """
    map = folium.Map(location=coordinates[0], zoom_start=12)
    for coordinate in coordinates:
        folium.Marker(coordinate).add_to(map)
    display(map)


def pad_time(x):
    """
    Format the time properly to parse as a datetime object
    """
    if len(x) < 2:
        return '000' + x
    elif len(x) < 4:
        return '0' + x
    else:
        return x


def clean_conditions(results, hourly_data=True):
    """
    Pass in JSON results from visualcrossing API and
    return cleaned DataFrame ready for analysis
    """
    df = pd.DataFrame.from_dict(results['historical'],
                                orient='index')
    df = pd.concat([df.drop(['astro'], axis=1),
                    df['astro'].apply(pd.Series)], axis=1)
    if hourly_data:
        df = df.explode('hourly')
        # Expand dictionary containing hourly details
        df = pd.concat([df.drop(['hourly'], axis=1),
                        df['hourly'].apply(pd.Series)], axis=1)

    df['date'] = df['date'] + '-' + df['time'] \
                .apply(lambda x: str(x)) \
                .apply(lambda x: pad_time(x))
    df['datetime'] = pd.to_datetime(df['date'],
                                    format='%Y-%m-%d-%H%M')
    # df.drop(['time', 'date'], axis=1, inplace=True)
    df = df.set_index('datetime')
    df = df.iloc[:, 1:]
    print(df.head())
    return df


def main(country='Spain',
         randomized=True,
         num_points=2,
         date_begin='2018-01-01', date_end='2018-01-02',
         hourly_data=True,
         api_key='953235aa4e74fcb593bd59c2b548d03a',
         specific_coordinates=[],
         interval=6):
    """
    Generates hourly or daily weather data for a given country over
    specific time period. Data sourced from visualcrossing

    Function will generate either random weather data over country or will
    generate weather data at a given point set of points chosen by the user.

    Parameters:
    country (str): country of interest
    randomized (bool): specify whether user desires randomly placed points
    within country or specific location
    num_points (int): number of points over country which are desired
    date_begin (str): beginning date YYYY-MM-DD
    date_end (str): end date YYYY-MM-DD
    daily_data (bool): daily (True) or hourly (False) data
    specific_coordinates (list):
    list of lists of floats [[lat1, long1], [lat2, long2], ....]
    at which you would like to extract the weather
    Returns:
    saves weather data

    """

    # Generate 'num_points' randomly sampled coordinates in country
    if randomized:
        coordinates = generate_coordinates(country=country,
                                           num_points=num_points)
    else:  # use specified coordinates
        coordinates = specific_coordinates
    plot_points(coordinates)  # Plot points on map for reference
    for coordinate in coordinates:
        latitude, longitude = coordinate
        json_conditions = get_historical_conditions(
                        latitude=latitude,
                        longitude=longitude,
                        date_begin=date_begin,
                        date_end=date_end,
                        api_key=api_key,
                        hourly_data=hourly_data,
                        interval=interval)

        clean_conditions(json_conditions,
                         hourly_data=hourly_data
                         ).to_csv(
                            '{}_{}_weather_data_@_{:.2f}_{:.2f}.csv'.format(
                                country,
                                'hourly' if hourly_data else 'daily',
                                latitude,
                                longitude))

        # location_data_list.append(clean_conditions(json_conditions))


if __name__ == '__main__':
    main(country='Spain',
         randomized=True,
         num_points=1,
         date_begin='2021-06-01',
         date_end='2021-06-01',
         hourly_data=True,
         interval=1)
