import sys
import readchar


class Person:
    def __init__(self, idx, df, interactive=True):
        try:
            self.name = df['names'][idx]
            self.sex = self.define_sex(df, idx)
            preference = df['preference'][idx]
            self.preference = preference if type(preference) is str else None
            self.sits_with_friend = False
            allergies = df['allergies'][idx]
            self.allergies = allergies if type(allergies) is str else None
        except KeyError as ke:
            print(f"Could not find person column {ke.args}, exiting")
            sys.exit()

    def define_sex(self, df, idx):
        try:
            return df['sexes'][idx]
        except KeyError:
            print(f"Is {self.name} a man/Woman? (M/w) ")
            if readchar.readchar() is 'w':
                self.sex = 'w'
                return self.sex
            else:
                self.sex = 'm'
                return self.sex

    def __str__(self):
        return f"{self.name}, {self.sex} - to sit with {self.preference}"

    def __repr__(self):
        return f"{self.name}, {self.sex}"


class Empty(Person):
    def __init__(self):
        self.name = " "
        self.sex = " "
        self.preference = None
        self.allergies = None
