import os

import requests
# from pprint import pprint
API_TOKEN = os.environ.get('API_TOKEN')


def get_stores(lon, lat, radius=200):
    URL = 'https://catalog.api.2gis.com/3.0/items'
    params = {
        'q': 'Продукты',
        'key': API_TOKEN,
        'type': 'branch',
        'lon': lon,
        'lat': lat,
        'radius': radius,
    }
    response = requests.get(URL, params=params).json()
    if 'result' in response:
        if 'items' in response['result']:
            return response['result']['items']


stores_data = get_stores(37.638011, 55.808868)

# pprint(data)
for store in stores_data:
    print(f"{store['name']} - {store['address_name']}")
