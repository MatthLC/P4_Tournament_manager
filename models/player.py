class Players:
    def __init__(self, first_name, last_name, sex, birthday, ranking):
        self.first_name = first_name
        self.last_name = last_name
        self.sex = sex
        self.birthday = birthday
        self.ranking = ranking

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
