import os
import requests
import telebot

from create_rdf import get_ticket_pdf
from main import get_flight_info, get_info_by_user

token = os.getenv("TOKEN")
bot = telebot.TeleBot(token)
cities = {}
flight_date = {}
name = {}
surname = {}
passport = {}
origin_city = {}
destination_city = {}
flight_info = {}


@bot.message_handler(content_types=['text'])
def get_cities(message):
    if message.text.lower() == 'привет' or message.text.lower() == '/help' or message.text.lower() == '/start':
        bot.send_message(message.chat.id, 'Откуда и куда вы хотите? Пример ответа: "Из Дели в Москву"')
        bot.register_next_step_handler(message, get_date)
    else:
        bot.send_message(message.from_user.id, 'Напиши /start')


def get_date(message):
    cities[message.from_user.id] = message.text
    cities_list = message.text.split()
    c = "%20".join(cities_list)
    r = requests.get(f'https://www.travelpayouts.com/widgets_suggest_params?q={c}')
    flight_info[message.from_user.id] = r.json()
    if not r.json():
        bot.send_message(message.chat.id, 'Скорее всего ошибка в написании города. Попробуйте снова.')
    else:
        bot.send_message(message.chat.id, 'Когда хотите полететь? Пример ответа: 2022-11 или 2022-11-01')
        bot.register_next_step_handler(message, get_name)


def get_name(message):
    flight_date[message.from_user.id] = message.text
    available_flights = flight_info[message.from_user.id]
    if not (
        get_flight_info(
            origin=available_flights['origin']['iata'],
            destination=available_flights['destination']['iata'],
            departure_date=message.text
        )
    ):
        bot.send_message(message.chat.id, 'На эти даты нет билетов.')
        # bot.register_next_step_handler(message, get_cities)
    else:
        bot.send_message(message.chat.id, 'Ваше имя латиницей (как в паспорте)')
        bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    name[message.from_user.id] = message.text
    bot.send_message(message.chat.id, 'Ваша фамилия латиницей (как в пасспорте)')
    bot.register_next_step_handler(message, get_passport_id)


def get_passport_id(message):
    surname[message.from_user.id] = message.text
    bot.send_message(message.chat.id, 'Номер вашего паспорта')
    bot.register_next_step_handler(message, save_surname)


def save_surname(message):
    passport[message.from_user.id] = message.text
    city = cities[message.from_user.id]
    bot.send_message(message.chat.id, 'Сохранил.')
    bot.send_message(
        message.chat.id,
        f'Вы летите {city}. '
        f'А напишите, пожалуйста, город, из которого вы летите на английском, чтобы он красиво смотрелся в билете.'
    )
    bot.register_next_step_handler(message, save_origin)


def save_origin(message):
    origin_city[message.from_user.id] = message.text
    bot.send_message(message.chat.id, 'Сохранил.')
    bot.send_message(message.chat.id, 'А теперь город прибытия на английском.')
    bot.register_next_step_handler(message, save_destination)


def save_destination(message):
    destination_city[message.from_user.id] = message.text
    passport_id = passport[message.from_user.id]
    city = cities[message.from_user.id]
    dep_date = flight_date[message.from_user.id]
    user_name = name[message.from_user.id]
    user_surname = surname[message.from_user.id]
    destinat = destination_city[message.from_user.id]
    orig = origin_city[message.from_user.id]

    origin, destination, date = get_info_by_user(city, dep_date)

    data = get_flight_info(origin=origin, destination=destination, departure_date=date)
    # print(data)

    try:
        get_ticket_pdf(data, user_name, user_surname, passport_id, destinat, orig)
        bot.send_message(message.chat.id, 'Ваш билет:')
        send_document(message, destinat)
    except Exception as exc:
        bot.send_message(message.chat.id, 'Кажется, на эти даты билетов нет.')
        print(exc)


def send_document(message, destinat):
    doc_name = name[message.from_user.id] + '_' + surname[message.from_user.id] + destinat + "_ticket.pdf"
    document = open('tickets/' + doc_name, 'rb')
    bot.send_document(message.from_user.id, document)


bot.polling(none_stop=True, interval=0)
