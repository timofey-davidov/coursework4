"""
Файл с основным телом программы
"""
from classes import Connector
from operator import attrgetter
import time, datetime
import utils, classes


def main():
    # вакансия для поиска
    job_search = input(f"{username}, введите вакансию для поиска:\t\t").lower().strip()
    # создание БД
    database_flag = utils.create_database(job_search)
    if database_flag:
        param_list = utils.params()
        print("Анализируем вакансии...")
        time.sleep(1)
        print("Вот несколько наиболее подходящих вакансий под Ваш запрос:")
        # словарь со значениями для сортировки
        sort_dict = {1: "_salary_to_filter", 2: "has_test", 3: "accept_temporary", 4: "date_published"}
        # формирование значений для сортировки
        attr = list(sort_dict.get(i) for i in param_list)
        if None in attr:
            attr = [i for i in attr if i is not None]
        if len(attr) != 0:
            working_list = sorted(classes.Vacancy._vacancy_list, key=attrgetter(*attr), reverse=True)
        else:
            working_list = sorted(classes.Vacancy._vacancy_list, key=attrgetter("_salary_to_filter"), reverse=True)
        working_list_enumerated = list(enumerate(working_list, 1))
        count = int(input("Введите количество вакансий для вывода в топ: "))
        for i in range(0, count):
            print(f"{working_list_enumerated[i][0]}. {working_list_enumerated[i][1]}", sep="\n")
        save_flag = int(input(f"Сохранить данные?\n(1 - Да, 2 - Нет)\n"))
        if save_flag == 1:
            data = [i.to_json() for i in working_list]
            utils.save_info(job_search, data)

if __name__ == '__main__':
    username = input("Добрый день! Представьтесь, пожалуйста:\t\t").lower().capitalize()
    while True:
        # ОСНОВНАЯ функция для работы с пользователем
        main()
        # ЗАВЕРШАЮЩАЯ функция для работы с пользователем
        exit_status = int(input("Подобрать для Вас других вакансий?\n(1 - Да, 2 - Нет)\n"))
        if exit_status == 2:
            break
    print("Спасибо за обращение! Хорошего дня!")
