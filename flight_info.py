# import requests
#
#
# url = 'https://api.travelpayouts.com/aviasales/v3/prices_for_dates'
#
#
# def get_flight_info(origin, destination, departure_date):
#     r = requests.get(
#         url,
#         params={
#             'origin': origin,
#             'destination': destination,
#             'unique': 'false',
#             'sorting': 'price',
#             'departure_at': departure_date,
#             'direct': 'true',
#             'currency': 'rub',
#             'limit': 5,
#             'page': 1,
#             'one_way': 'true',
#             'token': 'b57898fb118834aae6aacb1a65aa22e8',
#         }
#     )
#     return r.json()['data']
from datetime import datetime

from datetime import datetime
date_time_str = '18/09/19'

print(datetime.strptime(date_time_str, '%d/%m/%y'))

