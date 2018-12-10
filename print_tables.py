"""Functions for displaying data from seating order tables in the terminal.

Different functions for printing data from a dict of tables in the terminal
All the functions take a dict as param, which has the table names as
keys and lists of pairs of people as values.
"""


def print_tables(tables: dict) -> None:
    """Print the tables with peoples names and allergies."""
    for name, table in tables.items():
        print(f"\n{' ' * 55}{name}\n\n")
        if len(table[0][0].name) is 0:
            print("""                        +--------------+
                        |      E       |
                        |      M       |
                        |      P       |
                        |      T       |
                        |      Y       |
                        +--------------+

                  """)
            continue

        for idx, row in enumerate(table):
            if idx is 0:
                pad = 50 - len(row[0].name)
                print(f"{' ' * pad}{row[0].name}    +---------------+"
                      f"    {row[-1].name}")
                if row[0].allergies is not None:
                    al1 = row[0].allergies
                else:
                    al1 = ""
                if row[1].allergies is not None:
                    al2 = row[1].allergies
                else:
                    al2 = ""
                al_pad = 52 - len(al1)
                print(f"{' ' * al_pad}{al1}  |{' ' * 15}|  {al2}")
            elif idx is (len(table)-1):
                pad = 50 - len(row[0].name)
                print(f"{' ' * pad}{row[0].name}    +---------------+"
                      f"    {row[-1].name}")
                print("\n\n\n")
            else:
                pad = 50 - len(row[0].name)
                print(f"{' ' * pad}{row[0].name}    |               |"
                      f"    {row[-1].name}")
                if row[0].allergies is not None:
                    al1 = row[0].allergies
                else:
                    al1 = ""
                if row[1].allergies is not None:
                    al2 = row[1].allergies
                else:
                    al2 = ""
                al_pad = 52 - len(al1)
                print(f"{' ' * al_pad}{al1}  |{' ' * 15}|  {al2}")


def print_person_table_list(tables: dict) -> None:
    """Print a list  of all the people and their table name.

    Print a list in alphabetical order by surname of all the people displaying
    name and table name for everyone.
    """

    people = []
    for name, table in tables.items():
        for pair in table:
            people.extend(pair)
    people.sort(key=lambda x: x.name)
    print(f"\n\n\nPERSON -- TABLE\n")
    for person in people:
        if person.name is not " ":
            pad = 20 - len(person.name)
            print(f"{person.name}{' ' * pad} -- {person.table}")


def print_allergies(tables: dict) -> None:
    """Print a list of all the people with their allergies."""

    people = []
    for name, table in tables.items():
        for pair in table:
            people.extend(pair)
    people.sort(key=lambda x: x.name.split(" ")[-1])
    print(f"\n\n\nPERSON -- TABLE -- ALLERGIES\n")
    for person in people:
        if person.name is not " " and person.allergies is not None:
            pad = 20 - len(person.name)
            print(f"{person.name}{' ' * pad}  --  {person.table}  --  "
                  f"{person.allergies}")
