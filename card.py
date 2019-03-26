class Card:
    def __init__(self, value):
        self.value = value

    def __gt__(self, other):
        return self.value > other.value

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return str(self.value)
