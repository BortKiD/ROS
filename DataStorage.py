from collections import deque

class DataStorage:
    def __init__(self, max_data_points=10000):
        self.max_data_points = max_data_points
        self.data = deque(maxlen=max_data_points)

    def save_data(self, data):
        self.data.append(data)

    def save_to_file(self, filename):
        with open(filename, "wt") as file:
            json.dump(list(self.data), file)