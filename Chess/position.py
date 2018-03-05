"""
class: Position
"""


class Position:
    def __init__(self, position):
        if isinstance(position, str):
            if len(position) != 2:
                raise ValueError('{} is not a valid position'.format(position))
            self.coordinates = (ord(position[1]) - ord('1'), ord(position[0]) - ord('a'))
        else:
            self.coordinates = position
        position = self.coordinates
        if position[0] > 7 or position[0] < 0 or position[1] > 7 or position[1] < 0:
            raise ValueError('{} is not a valid position'.format(position))

    def getColumn(self):
        column = self.coordinates[1]
        return Position( (0, column))

    def getRow(self):
        row = self.coordinates[0]
        return Position((row, 0))

    def add(self, other_position):
        pos = (self.coordinates[0] + other_position.coordinates[0], self.coordinates[1] + other_position.coordinates[1])
        return Position( pos)

    def sub(self, other_position):
        pos = (self.coordinates[0] - other_position.coordinates[0], self.coordinates[1] - other_position.coordinates[1])
        return Position( pos)

    def multiply(self, n):
        return Position( (self.coordinates[0] * n, self.coordinates[1] * n))

    def __eq__(self, other):
        if self.coordinates == other.coordinates:
            return True
        else:
            return False

    def unitVector(self, other_position):
        pos = other_position.sub(self)
        if pos.coordinate[0] == 0:
            column = pos.coordinate[1] / abs(pos.coordinate[1])
            return Position((0, column))
        elif pos.coordinate[1] == 0:
            row = pos.coordinate[0] / abs(pos.coordinate[0])
            return Position((row, 0))
        else:
            denominator = pos.coordinate[0]
            row, column = pos.coordinate[0] / denominator, pos.coordinate[1] / denominator
            return Position( (row, column))


    def __str__(self):
        return chr(ord('a') + self.coordinates[1]) + chr(ord('1') + self.coordinates[0])
