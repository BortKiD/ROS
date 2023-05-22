from collections import deque
import csv

class DataStorage:
    """Класс хранилища данных.

    Поля:
        max_data_point (int): максимальное число сохраняемых строк.
        data (deque): кольцевой буфер для хранения данных.
    
    Методы:
        save_data(data): Сохраняет данные в кольцевой буфер.
        save_to_file(filename): Записывает сохраненные данные в файл.
    """
    def __init__(self, max_data_points:int=10000):
        self.max_data_points = max_data_points
        self.data = deque(maxlen=max_data_points)

    def save_data(self, data):
        """Сохраняет данные в кольцевой буфер
        
        Аргументы:
            data: строка, добавляемая в буфер
        """
        self.data.append(data)

    def save_to_file(self, filename):
        """Записывает сохраненные данные в файл
        
        Аргументы:
            filename: название файла
        """
        with open(filename, "wt") as file:
            writer = csv.writer(file, lineterminator='\n')
            writer.writerows(list(self.data))