import json


class Vacancy:
    """
    Класс, принимающий данные из парсера и создающий ЭКЗЕМПЛЯР ВАКАНСИИ с нужными данными
    Используется для хранения данных как во время их получения и записи, так и во время поиска
    """

    __slots__ = ("name", "url", "description", "salary")

    def __str__(self):
        return f"Вакасия: {self.name}\nСсылка на вакансию: {self.url}\nОписание вакансии:{self.description}\nЗарплата: {self.salary}"

    def __repr__(self):
        return f"Vacancy, {self.name}, {self.url}, {self.description}, {self.salary}"

    def __gt__(self, other):
        """Сравнение объетов класса на >"""
        if isinstance(other, Vacancy):
            return self.salary > other.salary

    def __lt__(self, other):
        """Сравнение объектов класса на <"""
        if isinstance(other, Vacancy):
            return self.salary < other.salary

    def __iter__(self):
        """Получение итератора для перебора"""
        pass

    def __next__(self):
        """Переход к слежующему значнеию итератора"""
        pass



class CountMixin:

    @property
    def get_count_of_vacancy(self):
        """
        Вернуть количество вакансий от текущего сервиса.
        Получать количество необходимо динамически из файла.
        """
        pass



class HHVacancy(Vacancy):  # add counter mixin
    """ HeadHunter Vacancy """
    def __init__(self, data: dict):
        self.name = data["name"]
        self.url = data["url"]
        self.description = data["snippet"]["responsibility"]
    def __str__(self):
        return f'HH: {self.name}, зарплата: {self.salary} руб/мес'


    # def get_salary(self, current_salary: dict):
    #     if type(current_salary["salary"]) is None:
    #         return 0
    #     if type(current_salary["salary"]) in (int, float):
    #         return current_salary["salary"]
    #     if type(current_salary["salary"]) is dict:
    #         if current_salary["salary"]["to"] is None:
    #             if current_salary["salary"]["from"] is None:
    #                 return 0
    #             else:
    #                 return current_salary["salary"]["from"]
    #         else:
    #             return current_salary["salary"]["to"]


class SJVacancy(Vacancy):  # add counter mixin
    """ SuperJob Vacancy """
    def __init__(self, data: dict):
        self.name = data
        self.url = data
        self.description = data
    def __str__(self):
        return f'SJ: {self.name}, зарплата: {self.salary} руб/мес'


def sorting(vacancies: list):
    """ Должен сортировать любой список вакансий по ежемесячной оплате (gt, lt magic methods) """
    return sorted(vacancies, key = lambda item: item.salary)


def get_top(vacancies, top_count):
    """ Должен возвращать {top_count} записей из вакансий по зарплате (iter, next magic methods) """
    pass

if __name__ == '__main__':
    with open("../JSON_database/database_HH.json", "r", encoding="UTF-8") as file:
        data = json.loads(file.read())
    lst = [HHVacancy(i) for i in data]