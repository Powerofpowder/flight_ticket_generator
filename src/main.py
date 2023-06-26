# from collections import OrderedDict
# from copy import deepcopy
#
# import requests
# import requests
# import json
# import hashlib
#
# from collections.abc import MutableMapping
#
#
# def flatten_dict(d: MutableMapping, parent_key: str = '', sep: str ='.') -> MutableMapping:
#     items = []
#     for k, v in d.items():
#         new_key = parent_key + sep + k if parent_key else k
#         if isinstance(v, MutableMapping):
#             items.extend(flatten_dict(v, new_key, sep=sep).items())
#         else:
#             items.append((new_key, v))
#     return dict(items)
#
# token = 'b57898fb118834aae6aacb1a65aa22e8'
# marker = '382549'
#
#
#
# original_data = {
#     "marker": marker,
#     "host": "datascience_project",
#     "user_ip": "103.108.5.67",
#     "locale": "ru",
#     "trip_class": "Y",
#     "passengers": {
#         "children": 0,
#         "infants": 0,
#         "adults": 2,
#     },
#     "segments": [
#         {
#             "origin": "DEL",
#             "destination": "MOV",
#             "date": "2022-10-25"
#         },
#     ]
# }
#
# data = deepcopy(original_data)
# data['segments'] = data['segments'][0]
# data = flatten_dict(data)
# data = OrderedDict(list(sorted(data.items())))
# result = ":".join(list(map(str, data.values())))
# result = f'{token}:{result}'
#
#
# original_data['signature'] = hashlib.md5(result.encode()).hexdigest()
#
# response = requests.post(
#     "http://api.travelpayouts.com/v1/flight_search",
#     json=original_data
# )
# print(response)
# # r = requests.get('http://api.travelpayouts.com/v1/flight_search_results?uuid=%ebe4fa71-bc07-40df-ae4e-4b72116583da%')
import string
import random
import requests
from datetime import datetime

from create_rdf import get_ticket_pdf

url = 'https://api.travelpayouts.com/aviasales/v3/prices_for_dates'


def get_flight_info(origin, destination, departure_date):
    r = requests.get(
        url,
        params={
            'origin': origin,
            'destination': destination,
            'unique': 'false',
            'sorting': 'price',
            'departure_at': departure_date,
            'direct': 'true',
            'currency': 'rub',
            'limit': 5,
            'page': 1,
            'one_way': 'true',
            'token': 'b57898fb118834aae6aacb1a65aa22e8',
        }
    )
    print(r.json())
    return r.json()['data']


def get_info_by_user(cities, date_str):
    # date_obj = datetime.strptime(date_str, '%d/%m/%y')
    cities_list = cities.split()
    cities = "%20".join(cities_list)
    r = requests.get(f'https://www.travelpayouts.com/widgets_suggest_params?q={cities}')
    available_flights = r.json()
    origin_code = available_flights['origin']['iata']
    destination_code = available_flights['destination']['iata']
    return origin_code, destination_code, date_str


# data = get_flight_info(origin='IST', destination="UFA", departure_date='2023-07-10')
# print(data)
# get_ticket_pdf(data, 'Alimova', 'Anastasia', '6337388', 'Moscow', 'Kazan')
