"""
Файл с функциями.
В файле предоставлена реализация фильтров для поиска вакансий.
Базовая сортировка, которая применяется ко всем вакансиям – по времени добавления вакансии на сайт (сначала выводятся самые свежие вакансии)
"""
import classes
from classes import Connector
import time, json, datetime
from operator import attrgetter
def create_database(keyword: str):
    # функция формирования базы данных
    print("...Формируем базу данных...")
    time.sleep(1)
    # создаем объекты для каждого сайта поиска работы
    hh = classes.HH(keyword)
    sj = classes.SJ(keyword)
    # обнуляем базу данных (если она была создана до этого)
    hh.connect.clear()
    sj.connect.clear()
    classes.Vacancy.clear_vacancy_list()
    # подгоняем результат под шаблон и сохраняем в формате JSON
    hh.get_request()
    hh.to_json()
    sj.get_request()
    sj.to_json()
    # проверяем сформированную базу данных и выводим ее статус:
    with open(hh.connect_address, "r", encoding="utf-8") as file:
        data = json.load(file)
    if len(data) < 1:
        print("База данных не была сформирована! Проверьте поисковой запрос!")
        return False
    else:
        print("База данных успешно сформирована!")
        for i in data:
            if i["platform"] == "HeadHunter":
                item = classes.HHVacancy(i)
            elif i["platform"] == "SuperJob":
                item = classes.SJVacancy(i)
        return True

def params():
    """Функция для формирования параметров фильтрации вакансий"""
    try:
        param = set(map(int, input(
            "Введите через пробел номера параметров для фильтрации вакансий:\n1 - Высокая зарплата\n2 - Наличие тестового задания\n3 - Временная\частичная занятость\n4 - Дата добавления вакансии\n").split()))
    except ValueError:
        print("Пожалуйста, проверьте ввод! должны быть числа через пробел!")
        time.sleep(1)
        params()
    return param

def save_info(search_name, data):
    """Функция для сохранения данных в указанный файл"""
    file = Connector(f"JSON_database/database_{search_name}_{datetime.date.today()}.json")
    file.insert(data)
    print("Данные сохранены!")

if __name__ == '__main__':
    create_database("python")
