import json, os, pprint
from abc import ABC, abstractmethod
from connector import Connector
import requests


class Engine(ABC):
    @abstractmethod
    def get_request(self):
        """Возвращает результаты запроса на сайт"""
        pass

    @abstractmethod
    def to_json(self):
        """Записывает файлы в БД в формате JSON"""
        pass

    @staticmethod
    def get_connector(file_name: str = "../JSON_database/database.json"):
        """ Возвращает экземпляр класса Connector """
        return Connector(file_name)


class HH(Engine):
    """Класс для осуществления взаимодействия с API HeadHunter"""

    def __init__(self, search_word: str):
        self.search_word = search_word
        self.__URL = "https://api.hh.ru/vacancies/"
        self.vacancies_list = list()
        self.connect = self.get_connector("../JSON_database/database_HH.json")

    def get_request(self, page=0):
        """Метод запроса вакансий к API (список из вакансий на конкретной странице)"""

        # формируем параметры для поиска вакансий
        self.params = {
            "text": self.search_word,
            "page": page,
            "per_page": 100,
        }

        # получаем ответ от API
        response = requests.get(self.__URL, params=self.params)
        # переводим формат JSON в строку STR
        response_str = response.content.decode()
        # возвращаем ответ
        return response_str

    def to_json(self):
        """Метод сохранения данных о вакансиях в отдельный файл (отдельная БД)"""
        # обнуляем список с вакансиями, если ранее уже был выполнен поиск
        self.vacancies_list = list()
        for page in range(0, 20):
            current_objects = json.loads(self.get_request(page))
            self.vacancies_list.extend(current_objects["items"])
        self.connect.insert(self.vacancies_list)


class SuperJob(Engine):
    """Класс для осуществления взаимодействия с API SuperJob"""

    # ссылка на страницу поиска вакансий
    def __init__(self, search_word: str):
        self.search_word = search_word
        self.URL = 'https://api.superjob.ru/2.0/vacancies/'
        self.vacancies_list = list()
        self.connect = self.get_connector("../JSON_database/database_SJ.json")

    def get_request(self, page=0):
        # формируем заголовок запроса
        self.headers = {
            'Host': 'api.superjob.ru',
            'X-Api-App-Id': os.getenv('SJ_Key'),
            'Authorization': 'Bearer r.000000010000001.example.access_token',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # формируем параметры запроса
        self.params = {
            'keyword': self.search_word,
            'count': 100,
            'page': page
        }

        # получаем ответ от API
        response = requests.get(self.URL, headers=self.headers, params=self.params)
        # переводим в формат JSON
        response_json = response.json()
        # возвращаем ответ
        return response_json
    def to_json(self):
        """Метод сохранения данных о вакансиях в отдельный файл (отдельная БД)"""
        # обнуляем список с вакансиями, если ранее уже был выполнен поиск
        self.vacancies_list = list()
        for page in range(0, 20):
            current_objects = self.get_request(page)
            self.vacancies_list.extend(current_objects["objects"])
        self.connect.insert(self.vacancies_list)