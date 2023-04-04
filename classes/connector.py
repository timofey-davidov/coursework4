import datetime
import os, json, time, datetime
__all__ = ["Connector"]


class Connector:
    """
    Класс коннектор к файлу, обязательно файл должен быть в json формате
    не забывать проверять целостность данных, что файл с данными не подвергся
    внешней деградации (если файл был создан более 24 часов назад – он считается
    неактуальным.
    ---
    Класс, описывающий подключение к файлам и работу с ними.
    """

    def __init__(self, path_to_file: str):
        """
        Метод, инициализации работы с файлом
        """
        # присваиваем приватному атрибуту путь до файла
        self.__data_file = path_to_file
        # осуществляем проверку файла через соответсвующий приватный метод
        self.__connect()

    @property
    def data_file(self):
        """
        Метод, возвращающий путь до файла
        """
        return self.__data_file

    @data_file.setter
    def data_file(self, value: str):
        """
        Метод, задающий новый путь до файла
        """
        # устанавливаем новое значение файла (путь до файла)
        self.__data_file = value
        # осуществляем проверку файла через соответсвующий приватный метод
        self.__connect()

    def __connect(self):
        """
        Метод, который осуществляет:
        1. Проверку на существование файла с данными и его создание при необходимости
        2. Проверку на деградацию: если файл потерял актуальность, возбуждается исключение
        """

        # проверка на существование файла
        if not os.path.exists(self.__data_file):
            file = open(self.__data_file, "w")
            file.close()

        # проверка на актуальность файла:
        current_time = time.time()  # текущее время
        file_creation_time = os.path.getmtime(self.__data_file)  # время создания файла
        if not current_time - file_creation_time < 84_400:  # проверяем разницу во времени (не более 24 часов)
            current_date = datetime.date.today()
            current_date = current_date.strftime("%d_%m_%Y")
            self.__data_file = f"{self.__data_file}_{current_date}"
            print(f"Файл слишком старый. Была создана новая база данных с именем {self.__data_file}_{self.__data_file}")

    def insert(self, data):
        """
        Метод записи данных в файл с сохранением структуры и исходных данных
        """
        with open(self.__data_file, "r", encoding="UTF-8") as file:
            f = file.read()
            if not f:
                base = []
            else:
                base = json.loads(f)
            base.extend(data)
            file.close()
        with open(self.__data_file, "w", encoding="UTF-8") as file:
            json.dump(base, file, ensure_ascii=False)
            file.close()

    def select(self, query: dict):
        """
        Метод выбора данных из файла с применением фильтрации
        query: содержит словарь, в котором ключ это поле для
        фильтрации, а значение это искомое значение, например:
        {'price': 1000}, должно отфильтровать данные по полю price
        и вернуть все строки, в которых цена 1000
        """
        with open(self.__data_file, "r") as file:
            json_list = json.load(file)
            return_list = list()
            if query:
                for i in json_list:
                    if i[list(query.keys())[0]] == list(query.values())[0]:
                        return_list.append(i)
            if len(return_list) == 0:
                print("Данные по текущему фильтру не найдены")
            file.close()
        return return_list

    def delete(self, query: dict):
        """
        Метод удаления записей из файла, которые соответствуют запрос,
        как в методе select. Если в query передан пустой словарь, то
        функция удаления не сработает
        """
        with open(self.__data_file, "r", encoding="UTF-8") as file:
            json_list = json.load(file)
            return_list = list()
            if query:
                for i in json_list:
                    if list(query.keys())[0] in i:
                        if i[list(query.keys())[0]] == list(query.values())[0]:
                            continue
                        else:
                            return_list.append(i)
            file.close()

        if query:
            with open(self.__data_file, "w", encoding="UTF-8") as file:
                json.dump(return_list, file)

    def clear(self):
        """
        Метод очистки файла с базой данных
        """
        with open(self.__data_file, "w", encoding="UTF-8") as file:
            file.close()

