class User:
    def __init__(self, name: str, age: int, city: str, state: str, week_gestation: int = None):
        """
        Initializes a User instance with a name and age.
        :param name: The name of the user.
        :param age: The age of the user.
        :param city: The city where the user resides.
        :param state: The state where the user resides.
        :param week_gestation: The week of gestation (if applicable).
        """
        self.name = name
        self.age = age
        self.city = city
        self.state = state
        self.week_gestation = week_gestation
        