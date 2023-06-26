from fpdf import FPDF
from datetime import datetime, timedelta
import random
import string
import randomtimestamp

pdf_w = 210
pdf_h = 297

main_info_settings = ('Arial', 'B', 14)


class PDF(FPDF):
    # def lines(self):
    #     self.set_line_width(0.0)
    #     self.line(5.0, 5.0, 205.0, 5.0)  # top one
    #     self.line(5.0, 292.0, 205.0, 292.0)  # bottom one
    #     self.line(5.0, 5.0, 5.0, 292.0)  # left one
    #     self.line(205.0, 5.0, 205.0, 292.0)  # right one

    def titles(self, order_number):
        self.set_xy(0.0, 0.0)
        self.set_font('Arial', 'B', 10)
        self.set_text_color(0, 0, 0)
        self.set_xy(45.0, 15.0)
        self.text(
            45, 28,
            # align='C',
            f"Order {order_number} is confirmed.",
        )
        self.set_top_margin(10)

    def common_info(self):
        txt = 'LTD "White Trevel", Mob: +7 (495) 646-83-62'
        txt_2 = 'Agency: OneTwoTrip LLP, IATA'
        self.set_xy(50.0, 0.0)
        self.set_text_color(0, 0, 0)
        self.set_font('Arial', '', 8)
        self.text(45, 15, txt)
        self.text(45, 19, txt_2)
        self.set_margins(0, 0)
        # self.multi_cell(0, 22, txt_2)
        self.text(150, 15, 'E-TICKET')
        self.text(45, 37, "PASSENGER'S NAME AND SURNAME / ID")
        self.text(150, 37, 'DATE / ORDER NUMBER')
        self.text(110, 82, 'Economy (A)')
        self.text(110, 86, 'Baggage: C1 pc 20kg per passenger.')
        self.text(110, 90, 'Hand baggage: 1 pc 7kg per passenger.')
        self.text(110, 94, 'Status: HK')
        # main info
        self.set_font('Arial', style='', size=10)
        self.text(15, 65, 'DEPARTURE:')
        self.text(15, 80, 'FLIGHT#')
        self.text(15, 86, 'e-Ticket')
        self.text(15, 92, 'Airline')
        self.text(15, 98, 'Duration:')
        self.text(15, 113, 'ARRIVAL:')
        # price info
        self.text(10, 150, 'FARE')
        self.text(10, 155, 'TAXES AND CARRIER-IMPOSED FEES')
        self.text(10, 160, 'SERVICE FEE')
        self.text(10, 200, 'ENDORSEMENTS')
        self.text(10, 205, 'FARE CALCULATION')
        self.text(10, 210, 'FORM OF PAYMENT CASH')
        self.set_font('Arial', style='B', size=12)
        self.text(10, 165, 'TOTAL')
        self.text(10, 185, 'TOTAL PER PASSENGER')

    def price_info(self, price):
        tax = round(13 * price / 100, 1)
        self.set_font('Arial', style='', size=12)
        self.text(110, 150, str(price - tax))
        self.text(128, 150, 'RUB')
        self.text(110, 155, '0.00')
        self.text(128, 155, 'RUB')
        self.text(110, 160, str(tax))
        self.text(128, 160, 'RUB')
        self.set_font('Arial', style='B', size=12)
        self.text(110, 165, str(price))
        self.text(128, 165, 'RUB')
        self.text(110, 185, str(price))
        self.text(128, 185, 'RUB')

    def logo(self):
        self.set_xy(8.0, 6.0)
        self.image('logo.png', type='', w=1700 / 80, h=1920 / 80)

    def take_off_pic(self):
        self.set_xy(45.0, 59.0)
        self.image('take_off.png', type='', w=600 / 80, h=820 / 80)

    def landing_pic(self):
        self.set_xy(45.0, 107.0)
        self.image('landing.png', type='', w=600 / 80, h=820 / 80)

    def rectangles(self):
        self.set_xy(166.0, 57.0)
        self.image('rectang.png', type='', w=1500 / 80, h=1120 / 80)
        self.set_xy(166.0, 105.0)
        self.image('rectang.png', type='', w=1500 / 80, h=1120 / 80)

    def add_line(self):
        self.dashed_line(10, 55, 190, 55)
        self.line(10, 175, 138, 175)

    def add_name_surname(self, name, surname):
        self.set_font('Arial', 'B', 14)
        self.text(45, 43, name.upper() + ' ' + surname.upper() + ' /')

    def add_date(self, date=datetime.today() - timedelta(days=4)):
        self.set_font('Arial', 'B', 14)
        self.text(150, 43, str(date.strftime('%Y-%m-%d')) + ' /')

    def add_passport(self, id_num):
        self.set_font('Arial', 'B', 14)
        self.text(45, 48, id_num)

    def add_order_number(self, order_number):
        self.set_font('Arial', 'B', 14)
        self.text(150, 48, order_number)

    def add_e_ticket(self, e_ticket):
        self.set_font('Arial', 'B', 14)
        self.text(150, 20, e_ticket)

    def user_info(
            self, dep_date, dep_time,
            flight_num, airline, duration,
            arr_date, arr_time,
            origin, destination,
            origin_full, destination_full,
            origin_airport, destination_airport
    ):
        self.set_font('Arial', style='B', size=14)
        # print('etic ', e_ticket)
        self.text(57, 65, dep_date)
        self.text(57, 71, dep_time)
        self.text(57, 113, arr_date)
        self.text(57, 119, arr_time)
        self.set_font('Arial', style='', size=10)
        self.text(57, 80, flight_num)
        # self.text(57, 86, e_ticket.upper())
        self.text(57, 92, airline)
        self.text(57, 98, duration)
        self.text(110, 65, origin)
        self.text(110, 113, destination)
        self.set_font('Arial', style='', size=12)
        self.text(110, 71, origin_full)
        self.text(110, 119, destination_full)
        self.set_font('Arial', style='B', size=18)
        self.text(169, 68, origin_airport)
        self.text(169, 116, destination_airport)


def get_ticket_pdf(data, user_name, user_surname, passport_id, destinat, orig):
    pdf_name = user_name + '_' + user_surname + destinat + "_ticket.pdf"
    print(data, user_name, user_surname, passport_id, destinat, orig)
    # print(data[0]['departure_at'])
    dep = data[0]['departure_at'][:-6].replace('T', ' ')
    dep_date = str(dep).split(' ')[0]
    dep_time = str(dep).split(' ')[1].split(':00')[0]
    duration = data[0]['duration']
    duration_hour = duration // 60
    duration_min = duration % 60
    duration_str = str(duration_hour) + ' h ' + str(duration_min) + ' min'
    arr = str(datetime.strptime(dep, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=duration))
    arr_date = arr.split()[0]
    arr_time = arr.split()[1].split(':00')[0]
    if len(str(arr_time)) == 2:
        arr_time += ':00'
    order_number = f'{random.randrange(1, 10 ** 6):06}'
    e_ticket = str(random.randint(10, 99)) + ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    airline = data[0]['airline']
    flight_num = airline + '-' + str(data[0]['flight_number'])
    origin_city = data[0]['origin']
    destination_city = data[0]['destination']
    origin_airport = data[0]['origin_airport']
    destination_airport = data[0]['destination_airport']
    price = data[0]['price']
    pdf = PDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    # print('заказ ', order_number)
    pdf.titles(order_number=order_number)
    pdf.logo()
    pdf.rect(166, 60, w=1500 / 80, h=950 / 80, style='S')
    pdf.rect(166, 108, w=1500 / 80, h=950 / 80, style='S')
    pdf.add_name_surname(user_name, user_surname)
    pdf.add_passport(passport_id)
    pdf.add_date()
    pdf.add_order_number(order_number)
    pdf.add_e_ticket(e_ticket)
    pdf.add_line()
    pdf.common_info()
    pdf.user_info(
        dep_date=dep_date,
        dep_time=dep_time,
        arr_date=arr_date,
        arr_time=arr_time,
        flight_num=flight_num,
        airline=airline,
        duration=duration_str,
        origin=origin_city,
        destination=destination_city,
        origin_full=orig,
        destination_full=destinat,
        origin_airport=origin_airport,
        destination_airport=destination_airport,
    )
    pdf.take_off_pic()
    pdf.landing_pic()
    pdf.price_info(price)
    pdf.output('tickets/' + pdf_name, 'F')