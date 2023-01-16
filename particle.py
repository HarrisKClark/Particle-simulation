#particle class

class Particle():
    def __init__(self, x, y, size, element):
        self.x = x
        self.y = y
        self.size = size
        self.element = element

        self.xforce = 0
        self.yforce = 0
        self.true_color = (0,0,0)
        self.interactions = 0

    def element_attributes(self, element_handler):
        self.true_color = element_handler.colors[self.element-1]

    def display_color(self):
        display_color = [self.true_color[0], self.true_color[1], self.true_color[2]]
        if self.interactions > 20:
            display_color[0] = 100 + self.true_color[0]
            display_color[1] = 100 + self.true_color[1]
            display_color[2] = 100 + self.true_color[2]

        else:
            display_color[0] = 5*self.interactions + self.true_color[0]
            display_color[1] = 5*self.interactions + self.true_color[1]
            display_color[2] = 5*self.interactions + self.true_color[2]

        return (display_color[0], display_color[1], display_color[2])
