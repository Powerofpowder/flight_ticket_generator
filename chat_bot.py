import telebot

from create_rdf import get_ticket_pdf
from main import get_info_by_user, get_flight_info

token = '1900724040:AAGedVyVclJKMqogC6ZrAyQ1TMCqxmJFU6M'
bot = telebot.TeleBot(token)
cities = {}
flight_date = {}
name = {}
surname = {}
passport = {}
origin_city = {}
destination_city = {}


@bot.message_handler(content_types=['text'])
def get_cities(message):
    if message.text.lower() == 'привет' or message.text.lower() == '/help' or message.text.lower() == '/start':
        bot.send_message(message.chat.id, 'Откуда и куда вы хотите? Пример ответа: "Из Дели в Москву"')
        bot.register_next_step_handler(message, get_date)
    else:
        bot.send_message(message.from_user.id, 'Напиши /start')


def get_date(message):
    cities[message.from_user.id] = message.text
    bot.send_message(message.chat.id, 'Когда хотите полететь? Пример ответа: 2022-11 или 2022-11-01')
    bot.register_next_step_handler(message, get_name)


def get_name(message):
    flight_date[message.from_user.id] = message.text
    bot.send_message(message.chat.id, 'Ваше имя латиницей (как в пасспорте)')
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
        send_document(message)
    except Exception as exc:
        bot.send_message(message.chat.id, 'Кажется, на эти даты билетов нет.')
        print(exc)


def send_document(message):
    doc_name = name[message.from_user.id] + '_' + surname[message.from_user.id] + "_ticket.pdf"
    document = open(doc_name, 'rb')
    bot.send_document(message.from_user.id, document)


bot.polling(none_stop=True, interval=0)


