import telebot
from dotenv import load_dotenv
import os
from config import Req
from config import Hotels

load_dotenv()
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

req = Req()


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def what_city(message):
    """Функция принимает команду пользователя и спрашивает город для поиска"""
    Req.cmd = message.text
    bot.send_message(message.from_user.id, "В каком городе ищем?")
    if req.cmd == '/bestdeal':
        bot.register_next_step_handler(message, range_price)
    else:
        bot.register_next_step_handler(message, how_many_hotels)


def range_price(message):
    """Принимает название города от пользователя и спрашивает диапазон цен для поиска"""
    Req.citi_name = message.text
    bot.send_message(message.from_user.id, "Введите диапазон цен")
    bot.register_next_step_handler(message, range_dis)


def range_dis(message):
    """Принимает диапазон цен от пользователя и спрашивает диапазон расстояний"""
    Req.range_price = message.text
    bot.send_message(message.from_user.id, "Введите диапазон расстояний от центра")
    bot.register_next_step_handler(message, how_many_hotels)


def how_many_hotels(message):
    """Если команда была bestdeal, то принимает диапазон расстояний.
    В противном случает принимает название города для поиска.
    В любом случае спрашивает слолько отелей вывести в результат."""
    if req.cmd == '/bestdeal':
        Req.range_dis = message.text
    else:
        Req.citi_name = message.text
    bot.send_message(message.from_user.id, "Сколько отелей вывести в результат?")
    bot.register_next_step_handler(message, answer)


def answer(message):
    """Принимает информацию о количестве отелей,
    которое необходимо вывести в результат. Выясняет id города,
    делает API-запрос по этому id. Формирует и отправляет читабельный ответ"""
    Req.hmh = message.text
    try:
        Req.citi_id, Req.citi_res = req.get_citi_ID()

        if req.cmd == '/lowprice':
            req.top_hotels_LP()
        elif req.cmd == '/highprice':
            req.top_hotels_HP()
        elif req.cmd == '/bestdeal':
            req.top_hotels_BD()

        my_list = list()
        if req.cmd == '/bestdeal':
            for i in req.result[:int(message.text)]:
                hotel = Hotels(i['name'], i['address']['streetAddress'], i['landmarks'][0]['distance'],
                               i['ratePlan']['price']['current'])
                if Req.range_dis.split('-')[0] <= hotel.dist <= Req.range_dis.split('-')[1]:
                    my_list.append(hotel)
        else:
            for i in req.result[:int(message.text)]:
                try:
                    hotel = Hotels(i['name'], i['address']['streetAddress'], i['landmarks'][0]['distance'],
                                   i['ratePlan']['price']['current'])
                except KeyError:
                    hotel = Hotels(i['name'], i['address']['streetAddress'], i['landmarks'][0]['distance'],
                                   None)
                my_list.append(hotel)

        data = ''
        for i_hotel in my_list:
            data += f'Name: {i_hotel.name}\nAddress: \t{i_hotel.address}\nDistance: ' \
                    f'{i_hotel.dist}\nPrice: {i_hotel.price}\n\n'
        if len(Req.citi_res) == 2:
            bot.send_message(message.from_user.id, f'{Req.citi_res[0][26:-7]}, {Req.citi_res[1]}')
        else:
            bot.send_message(message.from_user.id, f'{Req.citi_res[0][26:-7]}, {Req.citi_res[1]},{Req.citi_res[2]}')
        bot.send_message(message.from_user.id, data)
    except Exception:
        bot.send_message(message.from_user.id, 'Error')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    """Основной обработчик сообщений"""
    if message.text == "Привет" or message.text == "привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "/lowprice — вывод самых дешёвых отелей в городе\n"
                                               "/highprice — вывод самых дорогих отелей в городе\n"
                                               "/bestdeal — вывод отелей, наиболее подходящих по цене "
                                               "и расположению от центра")

    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


bot.polling(none_stop=True, interval=0)
