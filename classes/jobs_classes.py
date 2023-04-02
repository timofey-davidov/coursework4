import json, datetime

__all__ = ["Vacancy", "HHVacancy", "SJVacancy"]


class Vacancy:
    """
    Класс, принимающий данные из парсера и создающий ЭКЗЕМПЛЯР ВАКАНСИИ с нужными данными
    Используется для хранения данных как во время их получения и записи, так и во время поиска
    """

    __slots__ = ("name", "url", "description", "salary", "counter", "experience", "date_published")
    # список вакансий
    _vacancy_list = list()

    def __gt__(self, other):
        """Сравнение объетов класса на >"""
        if isinstance(other, (int, float)):
            return self._salary_to_filter > other
        if isinstance(other, Vacancy):
            return self._salary_to_filter > other._salary_to_filter
    def __lt__(self, other):
        """Сравнение объектов класса на <"""
        if isinstance(other, (int, float)):
            return self._salary_to_filter < other
        if isinstance(other, Vacancy):
            return self._salary_to_filter < other._salary_to_filter

    def __iter__(self):
        """Получение итератора для перебора"""
        # оздаем счетчик для подсчета списка объектов
        self.counter = 1
        return iter(self._vacancy_list)

    def __next__(self):
        """Переход к слежующему значнеию итератора"""
        if self.counter < len(self._vacancy_list):
            vacancy = self._vacancy_list[self.counter]
            self.counter += 1
            return vacancy
        else:
            raise StopIteration

    def add_to_vacancy_list(self, item):
        """Метод, добавляющий вакансию в список вакансий"""
        self._vacancy_list.append(item)
    @classmethod
    def clear_vacancy_list(cls):
        """Метод, очищающий список вакансий"""
        cls._vacancy_list = list()

    def to_json(self):
        return {
            "platform": self.platform,
            "name": self.name,
            "url": self.url,
            "salary": self.salary,
            "_salary_to_filter": self._salary_to_filter,
            "experience": self.experience,
            "date_published": str(self.date_published),
            "has_test": self.has_test,
            "accept_temporary": self.accept_temporary
        }

class HHVacancy(Vacancy):  # add counter mixin
    """ HeadHunter Vacancy """

    def __init__(self, data: dict):
        self.platform = "HeadHunter"
        self.name = data.get("name")
        self.url = data.get("url")
        self.salary = self.get_salary(data)
        self._salary_to_filter = self.get_salary_to_filter(data)
        self.experience = self.get_experience_to_filter(data)
        self.date_published = datetime.datetime.strptime(data.get("date_published"), "%Y-%m-%dT%H:%M:%S%z").date()
        self.has_test = data.get("has_test")
        self.accept_temporary = data.get("accept_temporary")
        super()._vacancy_list.append(self)

    def __str__(self):
        return f'HH: {self.name}, зарплата: {self.salary} руб/мес, подробнее смотри {self.url}'

    def get_salary(self, current_salary: dict):
        """Метод для получения зарплаты для вывода пользователю"""
        if current_salary.get("salary") is not None:
            _from = current_salary["salary"]["from"]
            _to = current_salary["salary"]["to"]

            if _from and _to:
                return f"от {_from} до {_to}"
            elif not _from and _to:
                return _to
            elif _from and not _to:
                return _from
        return "не указана"

    def get_salary_to_filter(self, current_salary):
        if current_salary["salary"] is None:
            return 0
        elif isinstance(current_salary["salary"], (int, float)):
            return current_salary["salary"]
        elif isinstance(current_salary["salary"]["to"], (int, float)):
            return current_salary["salary"]["to"]
        elif isinstance(current_salary["salary"]["from"], (int, float)):
            return current_salary["salary"]["from"]
        return 0

    def get_experience_to_filter(self, data: dict):
        _experience = 0
        if data.get("experience") is not None:
            match data.get("experience").get("id"):
                case "noExperience":
                    _experience = 0
                case "between1And3":
                    _experience = 1
                case "between3And6":
                    _experience = 3
                case "moreThan6":
                    _experience = 6
        return _experience


class SJVacancy(Vacancy):  # add counter mixin
    """ SuperJob Vacancy """

    def __init__(self, data: dict):

        self.platform = "SuperJob"
        self.name = data.get("name")
        self.url = data.get("url")
        self.salary = self.get_salary(data)
        self._salary_to_filter = 0 if (self.salary is None or isinstance(self.salary, str)) else self.salary
        self.experience = self.get_experience_to_filter(data)
        self.date_published = datetime.datetime.fromtimestamp(data.get("date_published")).date()
        self.has_test = True if data.get("has_test") else False
        self.accept_temporary = self.get_accept_temporary(data.get("accept_temporary"))
        super()._vacancy_list.append(self)

    def get_salary(self, current_data: dict):
        """Определяем зарплату для текстового вывода"""
        if current_data.get("salary") is None or current_data.get("salary") == 0:
            return "не указана"
        else:
            return current_data.get("salary")

    def get_experience_to_filter(self, data):
        """Определяем опыт"""
        _experience = 0
        match data["experience"]["id"]:
            case 1:
                _experience = 0
            case 2:
                _experience = 1
            case 3:
                _experience = 3
            case 4:
                _experience = 6
        return _experience

    def get_accept_temporary(self, data: dict):
        """Функция, проверяющая, является ли данная работа ВРЕМЕННОЙ (НЕПОЛНОЙ)"""
        if data.get("") in (0, 6, 9):
            return False
        return True

    def __str__(self):
        return f'SJ: {self.name}, зарплата: {self.salary} руб/мес, подробнее смотри {self.url}'
