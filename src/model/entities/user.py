class User:
    def __init__(self, name, record_date):
        self.name = name
        self.record_date = record_date
        self.babys = []

    def add_baby(self, baby):
        self.babys.append(baby)