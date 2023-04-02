import json, os, pprint
import time
from abc import ABC, abstractmethod
from classes import Connector
import requests

__all__ = ["Engine", "HH", "SJ"]


class Engine(ABC):
    """Абстрактный класс для формирования классов работы с поисковиками вакансий"""

    @abstractmethod
    def get_request(self):
        """Возвращает результаты запроса на сайт"""
        pass

    @abstractmethod
    def to_json(self):
        """Записывает файлы в БД в формате JSON в нужном для обработке формате (см. файл jobs_classes.py)"""
        pass

    @staticmethod
    def get_connector(file_name: str = "JSON_database/database.json"):
        """ Возвращает экземпляр класса Connector с БД по-умолчанию"""
        return Connector(file_name)


class HH(Engine):
    """Класс для осуществления взаимодействия с API HeadHunter"""

    def __init__(self, search_word: str, connect_address: str = "JSON_database/database.json"):
        # фраза для поиска вакансии
        self.search_word = search_word
        # ссылка на API для поиска
        self.__URL = "https://api.hh.ru/vacancies/"
        # список из найденных вакансий
        self._vacancies_list = list()
        # адрес БД
        self.connect_address = connect_address
        # объект-коннектор для работы с БД
        self.connect = self.get_connector(self.connect_address)

    def params_per_page(self, page=0):
        """Метод, формирующий условия запросов к API конкретной страницы"""
        # формируем параметры для поиска вакансий
        self.params = {
            "text": self.search_word,
            'area': 113,
            "page": page,
            "per_page": 100
        }
        return self.params
    def get_request(self):
        """Метод запроса вакансий к API (список из вакансий на конкретной странице)"""
        # список-множество id подходящих вакансий
        self._items_list = list()
        for page in range(0, 20):
            if len(self._items_list) <= 1000:
                # получаем ответ от API
                response = requests.get(self.__URL, params=self.params_per_page(page))
                # переводим формат JSON в словарь DICT сохраняем список из id вакансий (чтобы не перегружать базу данных, а также потому, что вытягиваются не все данные конкретной вакансии)
                response_dict = response.json()
                for i in response_dict["items"]:
                    self._items_list.append(i)
                # делаем задержку между запросами на страницы, чтобы HeadHunter не подумал, что мы их пытаемся нагрузить
                time.sleep(0.25)
            else:
                break
        print("...Вакансии с HH получены...")
        return self._items_list

    def get_info(self, vacancy: dict):
        """Метод, достающий нужую информацию из словаря"""
        info = {
            "platform": "HeadHunter",
            "id": vacancy.get("id"),
            "name": vacancy.get("name"),
            "url": vacancy.get("alternate_url"),
            "has_test": vacancy.get("has_test"),
            "salary": vacancy.get("salary"),
            "date_published": vacancy.get("published_at"),
            "accept_temporary": vacancy.get("accept_temporary")
        }
        return info

    def to_json(self):
        """Метод сохранения данных о вакансиях в отдельный файл (отдельная БД)"""
        # обнуляем список с вакансиями, если ранее уже был выполнен поиск
        self._vacancies_list = list()

        for item in self._items_list:
            if len(self._vacancies_list) <= 1000:
                vacancy_info = self.get_info(item)
                if vacancy_info.get("salary") is None or vacancy_info.get("salary").get("currency") == "RUR":
                    self._vacancies_list.append(self.get_info(item))
                time.sleep(0.005)
        self.connect.insert(self._vacancies_list)


class SJ(Engine):
    """Класс для осуществления взаимодействия с API SuperJob"""

    # ссылка на страницу поиска вакансий
    def __init__(self, search_word: str, connect_address: str = "JSON_database/database.json"):
        self.search_word = search_word
        self.URL = 'https://api.superjob.ru/2.0/vacancies/'
        self._vacancies_list = list()
        self.connect_address = connect_address
        self.connect = self.get_connector(self.connect_address)

    def params_per_page(self, page=0):
        """Метод, формирующий условия запросов к API конкретной страницы"""
        # формируем параметры для поиска вакансий
        self.params = {
            'keyword': self.search_word,
            'count': 200,
            'page': page
        }
        return self.params

    def get_request(self, page=0):
        # формируем заголовок запроса
        self.headers = {
            'Host': 'api.superjob.ru',
            'X-Api-App-Id': os.getenv('SJ_Key'),
            'Authorization': 'Bearer r.000000010000001.example.access_token',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # обнуляем список с вакансиями, если ранее уже был выполнен поиск
        self._items_list = list()
        for page in range(0, 5):
            current_objects = requests.get(self.URL, headers=self.headers, params=self.params_per_page(page)).json()
            for i in current_objects["objects"]:
                if i.get("currency") == "rub":
                    self._items_list.append(i)
                    time.sleep(0.005)
        print("...Вакансии с SJ получены...")
        return self._items_list

    def get_info(self, vacancy):
        vacancy_info = {
            "platform": "SuperJob",
            "name": vacancy.get("profession"),
            "url": vacancy.get("link"),
            "has_test": None,
            "accept_temporary": vacancy.get("type_of_work"),
            "salary": max(vacancy.get("payment_from"), vacancy.get("payment_to")),
            "experience": vacancy.get("experience"),
            "date_published": vacancy.get("date_published")
        }
        return vacancy_info

    def to_json(self):
        """Метод сохранения данных о вакансиях в отдельный файл (отдельная БД)"""
        # обнуляем список с вакансиями, если ранее уже был выполнен поиск
        self._vacancies_list = list()
        for item in self._items_list:
            if len(self._vacancies_list) <= 1000:
                vacancy_info = self.get_info(item)
                self._vacancies_list.append(vacancy_info)
                time.sleep(0.005)
        self.connect.insert(self._vacancies_list)