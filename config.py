import os
import requests
import re


class Hotels:
    """Класс, описывающий структуру данных об отеле"""

    def __init__(self, name, address, dist, price):
        self.name = name
        self.address = address
        self.dist = dist
        self.price = price


class Req:
    """Класс, описывающий структуру API-запросов"""
    citi_id = None
    cmd = None
    citi_name = None
    hmh = None
    result = []
    range_price = None
    range_dis = None
    citi_res = None

    def get_citi_ID(self):
        """Метод выполняет запрос по переменной citi_nama. Возвращает id-города и геоданные."""
        url = "https://hotels4.p.rapidapi.com/locations/v2/search"
        querystring = {"query": self.citi_name, "locale": "ru_RU", "currency": "USD"}
        headers = {
            'x-rapidapi-key': os.getenv('x-rapidapi-key'),
            'x-rapidapi-host': os.getenv('x-rapidapi-host')
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        return response.json()['suggestions'][0]['entities'][0]['destinationId'], \
               (response.json()['suggestions'][0]['entities'][0]['caption']).split(',')

    def top_hotels_LP(self):
        """Метод выполные запраос с citi_id, возвращает json данные обо всех отелях города.
        Отсортировано по цене по возрастанию"""
        url = "https://hotels4.p.rapidapi.com/properties/list"
        querystring = {"destinationId": self.citi_id, "pageNumber": "1", "pageSize": "25", "checkIn": "2020-01-08",
                       "checkOut": "2020-01-15", "adults1": "1", "sortOrder": "PRICE", "locale": "ru_RU",
                       "currency": "RUB"}
        headers = {
            'x-rapidapi-key': os.getenv('x-rapidapi-key'),
            'x-rapidapi-host': os.getenv('x-rapidapi-host')
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        Req.result = response.json()['data']['body']['searchResults']['results']

    def top_hotels_HP(self):
        """Метод выполные запраос с citi_id, возвращает json данные обо всех отелях города.
        Отсортировано по цене по убыванию"""
        url = "https://hotels4.p.rapidapi.com/properties/list"
        querystring = {"destinationId": self.citi_id, "pageNumber": "1", "pageSize": "25", "checkIn": "2020-01-08",
                       "checkOut": "2020-01-15", "adults1": "1", "sortOrder": "PRICE_HIGHEST_FIRST", "locale": "ru_RU",
                       "currency": "RUB"}
        headers = {
            'x-rapidapi-key': os.getenv('x-rapidapi-key'),
            'x-rapidapi-host': os.getenv('x-rapidapi-host')
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        Req.result = response.json()['data']['body']['searchResults']['results']

    def top_hotels_BD(self):
        """Метод выполняет запрос с citi_id и диапазонами цен и расстояния,
        возвращает json данные обо всех отелях города. Отсортировано по цене по убыванию"""
        url = "https://hotels4.p.rapidapi.com/properties/list"
        querystring = {"destinationId": self.citi_id, "pageNumber": "1", "pageSize": "25", "checkIn": "2020-01-08",
                       "checkOut": "2020-01-15", "adults1": "1", "priceMin": Req.range_price.split('-')[0],
                       "priceMax": Req.range_price.split('-')[1],
                       "sortOrder": "PRICE", "locale": "ru_RU",
                       "currency": "RUB"}
        headers = {
            'x-rapidapi-key': os.getenv('x-rapidapi-key'),
            'x-rapidapi-host': os.getenv('x-rapidapi-host')
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        Req.result = response.json()['data']['body']['searchResults']['results']
