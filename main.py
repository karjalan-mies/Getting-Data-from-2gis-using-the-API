import csv
import logging
import os


import requests
from pprint import pprint
API_TOKEN = os.environ.get('API_TOKEN')


def get_data_from_csv(file_name: str)-> list:
    vv_stores = []
    with open(file_name, 'r', encoding='utf-8') as f:
        fields = ['id_tt_cl', 'Quantity_febr', 'Summa_febr', 'Quantity_march',
                  'Summa_march', 'Quantity_april', 'Summa_april',
                  'Quantity_may', 'Summa_may', 'march/febr', 'april/march',
                  'may/april', 'sr_febr', 'sr_march', 'sr_april', 'sr_may',
                  'sr_march/febr', 'sr_april/march', 'sr_may/april', 'adress',
                  'Hours', 'lat', 'lon', 'ploshad', 'city_tt', 'Район',
                  'shtat', 'qty_kassa', 'qty_kassa_so', 'format',
                  'project_name']
        reader = csv.DictReader(f, fields, delimiter=';')
        count = 0
        for row in reader:
            if count > 0:
                vv_stores.append(
                    {'id_tt_cl': row['id_tt_cl'],
                     'lon': row['lon'],
                     'lat': row['lat']})
            count += 1
    return vv_stores


def get_data_from_2gis(shop, q, radius=200):
    URL = 'https://catalog.api.2gis.com/3.0/items'
    params = {
        'q': q,
        'key': API_TOKEN,
        'type': 'branch',
        'lon': shop['lon'],
        'lat': shop['lat'],
        'radius': radius,
    }
    response = requests.get(URL, params=params).json()
    return response


def get_data_from_json(shop, json_data) -> dict:
    current_shop_data = []
    for row in json_data:
        try:
            current_shop_data.append(row['name'].split(', ')[0])
        except KeyError:
            logging.error('Ключ "address_name" не найден')
    if current_shop_data[0] == 'ВкусВилл':
        current_shop_data.remove('ВкусВилл')
    return {'id_tt_cl': shop['id_tt_cl'],
            'count_shops': len(current_shop_data),
            'shop_list': ','.join(current_shop_data)}


def get_nearest_shops(shops: list) -> list:
    nearest_shops = []
    for shop in shops:
        json_data = get_data_from_2gis(shop, 'Продукты')
        if json_data:
            json_data = json_data['result']['items']
            result = get_data_from_json(shop, json_data)
            nearest_shops.append(result)
    return nearest_shops


def write_to_file(nearest_shops):
    with open('result_vv.csv', 'w') as f:
        names = ['id_tt_cl', 'count_shops', 'shop_list']
        file_writer = csv.DictWriter(f, delimiter=';', fieldnames=names)
        file_writer.writeheader()
        for shop in nearest_shops:
            file_writer.writerow(shop)


if __name__ == '__main__':
    vv_shops = get_data_from_csv('docs//ВкусВил.csv')
    nearest_shops = get_nearest_shops(vv_shops)
    pprint(nearest_shops)
    write_to_file(nearest_shops)
