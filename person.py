import sys
import readchar


class Person:
    """Represents a person with attributes describing the person.

    Params:
    name -- Name of person
    sex -- Sex represented as 'm' or 'w'
    preference -- avec or seating preference, name of another person
    allergies -- string of all the allergies of this person
    """

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
        """Saves the sex of this person.

        Saves the sex of this person either by taking it from the the param df
        or by getting it from stdin
        """
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
    """Subclass from Person representing empty an place"""

    def __init__(self):
        self.name = " "
        self.sex = " "
        self.preference = None
        self.allergies = None
