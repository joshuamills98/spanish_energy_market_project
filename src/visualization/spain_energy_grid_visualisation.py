import pandas as pd
import folium
from IPython.display import display
import requests
from bs4 import BeautifulSoup


# def get_ccaa_geojson():
#     """
#     Run API call to get geojson file for autonomous communities within Spain
#     """
#     path = os.path.join(os.getcwd(), 'Comunidades_Autonomas_ETRS89_30N.shp')
#     print(path)
#     reader = shapefile.Reader(path)
#     fields = reader.fields[1:]
#     field_names = [field[0] for field in fields]
#     buffer = []
#     for sr in reader.shapeRecords():
#         atr = dict(zip(field_names, sr.record))
#         geom = sr.shape.__geo_interface__
#         buffer.append(dict(type="Feature", \
#         geometry=geom, properties=atr))

#     # write the GeoJSON file
#     geojson = open("pyshp-demo.json", "w")
#     geojson.write(dumps({"type": "FeatureCollection",\
#     "features": buffer}, indent=2) + "\n")
#     geojson.close()


def get_ccaa_solar_data():
    """
    Get solar production data (by autonomous communuity) from wikipedia
    """
    url = 'https://en.wikipedia.org/wiki/Solar_power_in_Spain'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    data = []
    table = soup.find('table', attrs={'class': 'wikitable sortable'})
    table_body = table.find('tbody')
    # print(table_body)

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        # print(cols)
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])  # Get rid of empty values
    data = data[1:-1]  # Remove header and tail
    df = pd.DataFrame(data,
                      columns=['Region',
                               '2010',
                               '2011'])

    df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric)

    mapping = {'Andalusia': 'Andalucia',
               'Balearic Islands': 'Baleares',
               'Basque Country': 'Pais Vasco',
               'Canary Islands': 'Canarias',
               'Castile and León': 'Castilla-Leon',
               'Castile-La Mancha': 'Castilla-La Mancha',
               'Catalonia': 'CataluÃ±a',
               'Navarre': 'Navarra',
               'Community of Madrid': 'Madrid',
               'Ceuta and Melilla': 'Ceuta',
               'Region of Murcia': 'Murcia',
               'Valencian Community': 'Valencia'}

    df['Region'] = df['Region'].replace(mapping)
    return df


def get_ccaa_wind_data():
    """
    Get onshore wind-production data (by autonomous communuity) from wikipedia
    """
    url = 'https://en.wikipedia.org/wiki/Wind_power_in_Spain'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    data = []
    table = soup.find('table', attrs={'class': 'wikitable sortable'})
    table_body = table.find('tbody')
    # print(table_body)

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        # print(cols)
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])  # Get rid of empty values
    data = data[2:-1]

    df = pd.DataFrame(data,
                      columns=['Rank',
                               'Region',
                               '2008',
                               '2009',
                               '2010',
                               '2015'])

    df.iloc[:, 2:] = df.iloc[:, 2:].applymap(lambda x: x.replace(',', '')) \
                                   .apply(pd.to_numeric)

    mapping = {'Andalusia': 'Andalucia',
               'Balearic Islands': 'Baleares',
               'Basque Country': 'Pais Vasco',
               'Canary Islands': 'Canarias',
               'Castile and León': 'Castilla-Leon',
               'Castile-La Mancha': 'Castilla-La Mancha',
               'Catalonia': 'CataluÃ±a',
               'Navarre': 'Navarra',
               'Valencian Community': 'Valencia'}

    df['Region'] = df['Region'].replace(mapping)
    return df


def map_regional_data(geojson_data_path,
                      wind_data,
                      year,
                      gen_type='wind',
                      ):
    communities_map = folium.Map(location=[40.416775, -3.703790],
                                 tiles='stamenterrain',
                                 zoom_start=4)
    chloro = folium.Choropleth(
        geo_data=geojson_data_path,
        name='choropleth',
        data=wind_data,
        fill_color='{}'.format('BuPu' if gen_type == 'wind' else 'YlGn'),
        fill_opacity=0.9,
        columns=['Region', year],
        key_on='feature.properties.name',
        highlight=True,
        legend_name='{} in {} (MW)'\
            .format(
            'Installed PV Capacity' if gen_type == 'solar' else 'Wind Generation',
            year)
    ).add_to(communities_map)
    style_function = "font-size: 15px; font-weight: bold"
    folium.features.GeoJsonTooltip(
            ['name'],
            style=style_function,
            labels=False).add_to(chloro.geojson)
    folium.LayerControl().add_to(communities_map)
    display(communities_map)


if __name__ == '__main__':
    # print(get_ccaa_solar_data())
    geo_json_path = r'.\data\external\spain-regions.geojson'
    map_regional_data(geo_json_path, 
                      get_ccaa_solar_data(), 
                      year='2011', 
                      gen_type='solar')
