class Player(object):
    def __init__(self, name):
        self.points = 0
        self.name = name

    def get_name(self):
        return self.name

    def get_points(self):
        return self.points

    def set_points(self, points):
        self.points = points

class Piece(object):
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

class RedPiece(Piece):
    def __init__(self):
        super(RedPiece, self).__init__('red')

class BlackPiece(Piece):
    def __init__(self):
        super(RedPiece, self).__init__('black')
