#element class
import random

class Element_Handler():
    def __init__(self, num, min, max):
        self.num = num
        self.colors = []
        self.min = min
        self.max = max
        self.map = []

    def setup(self):
        for i in range(self.num):
            self.colors.append(self._generate_color())

        # row attracted to collumns. eg: row 1 col 2, is row 1 attraction to col 2
        attraction_map = [[0] * self.num for i in range(self.num)]

        for i in range(self.num):
            for j in range(self.num):
                attraction_map[i][j] = [[0, self.min, (self.min + self.max) / 2, self.max],
                                        [1, 0, random.randint(-100, 100) / 100, 0]]
        self.map = attraction_map

    def assign_element(self):
        return random.randint(1, self.num)

    def _generate_color(self):
        return random.randint(0, 150), random.randint(0, 150), random.randint(0, 150)
