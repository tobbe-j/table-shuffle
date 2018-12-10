import argparse
import sys
import random
import pandas as pd
from itertools import zip_longest
from save_table import save_tables, save_list
from print_tables import print_tables, print_person_table_list, print_allergies
from person import Person, Empty


def getArgs(argvals=None):
    """Parse the arguments from the commandline or optionally  from param"""

    parser = argparse.ArgumentParser(description="""Seating order from csv
Requieres filename of csv-file with data. To run interactively use -i.
Otherwise all columns must be specified with tags.
""")
    parser.add_argument('-i', '--interactive', help='Specify all the column'
                        'values interactivly', action='store_true')
    parser.add_argument('file', help='The csv file to read from')
    parser.add_argument('-c', '--column',
                        help='Specify name of column with names',
                        default='namn')
    parser.add_argument('-s', '--sexes', help='column for the sexes')
    parser.add_argument('-p', '--preference',
                        help='seat preference, who this person'
                        'wuold like to sit close to')
    parser.add_argument('-a', '--allergies', help='column for allergies')
    if argvals:
        return parser.parse_args(argvals)
    else:
        return parser.parse_args()


def ask_args(args):
    """Get args from stdin and add as attributes to param"""

    args.column = input("Column name for names: ")
    args.sexes = input("Column name for sexes: ")
    args.preference = input("Column name for preferences: ")
    args.allergies = input("Column name for allergies: ")


def get_tables():
    """Get table count, names and sizes from stdin and return as dict"""

    print('Setting up table count and sizes:')
    nr_tables = 0
    while (nr_tables <= 0):
        try:
            nr_tables = int(input("How many tables? "))
        except ValueError:
            pass
    nr_tables = nr_tables

    tables = {}
    for table in range(nr_tables):
        name = ""
        while type(name) is not str or len(name) <= 0:
            name = input("Name for this table? ")
        size = 0
        while(size <= 1):
            try:
                size = int(input(f"How long is table nr {table + 1}? "))
            except ValueError:
                pass
        if size > 30:
            print("\n\nWARNING: maximum table size supported is 30\n\n")
        tables[name] = size
    return tables


def balance_sex(men: list, women: list):
    """Even out th two lists to equal size and return them"""

    if len(men) > len(women):
        difference = (len(men) - len(women)) // 2
        for m in men[-difference:]:
            m.sex = 'w'
        women.extend(men[-difference:])
        del men[-difference:]
    elif len(women) > len(men):
        difference = (len(women) - len(men)) // 2
        for w in women[-difference:]:
            w.sex = 'm'
        men.extend(women[-difference:])
        del women[-difference:]
    return [men, women]


def randomize_tables(tables: dict, people: list) -> dict:
    """Create random table with the Objects from person.

    Create a random table with the Objects from person. First splits the people
    based on sex, then balance them to have eqaul amount of men and women.
    Then shuffle the lists and place the people on tables according to the data
    from the tables dict.

    Returns a dict with the table names as keys and lists of all the people in
    pairs for each table.

    Arguments:
    tables -- A dict with the names of the tables as keys and sizes of hte
    tables as values
    people -- a list of the people to be added to the tables
    """

    if sum(tables.values()) < len(people):
        print("\n\nWARNING: You have more names than space at the tables, some"
              " people will get dropped!\n\n")
    men, women = [], []
    for item in people:
        (men if item.sex is 'm' else women).append(item)
    balance_sex(men, women)
    print(f"Random seed used: {list(tables.keys())[0]},"
          f" use same number to get same shuffle")
    random.seed(list(tables.keys())[0])
    random.shuffle(men)
    random.shuffle(women)
    for person in people:
        if person.preference is not None:
            add_friend(men, women, person, tables)
    people = list(zip_longest(men, women, fillvalue=Empty()))
    for table, size in tables.items():
        tables[table] = []
        for seat in range(size):
            pair = []
            if len(people) is 0:
                pair = list((Empty(), Empty()))
            else:
                if seat % 2 is 0:
                    pair = list(people.pop(0))
                else:
                    pair = list(people.pop(0)[::-1])
            for p in pair:
                p.table = table
            tables[table].append(pair)

    return tables


def add_friend(men: list, women: list, host: Person, tables: dict) -> None:
    """Move the avec of the host close to the host"""

    print(f"Adding friend to {host.name}")
    friend = {x.name: x for x in men + women}.get(host.preference, "")
    if type(friend) is str or host.sits_with_friend or friend.sits_with_friend:
        print(f"Warning: {host.name} or {friend.name} already sits with a"
              f"friend, you need to edit this manually.")
        return
    host.sits_with_friend = True
    friend.sits_with_friend = True
    if host.sex is friend.sex:
        # Host and friend will sit diagonally opposite to each other
        if host.sex is 'm':
            swap_list = men
        else:
            swap_list = women
        host_index = swap_list.index(host)
        friend_index = swap_list.index(friend)
        # Checks that friend will not be slit at ends between two tables
        i_sum = 0
        will_be_split = False
        for name, length in tables.items():
            i_sum += length
            if host_index + 1 is i_sum:
                will_be_split = True

        if host_index + 2 < len(swap_list) and not will_be_split:
            (swap_list[friend_index],
             swap_list[host_index + 1]) = (swap_list[host_index + 1],
                                           swap_list[friend_index])
        else:
            (swap_list[friend_index],
             swap_list[host_index - 1]) = (swap_list[host_index - 1],
                                           swap_list[friend_index])
    else:
        # Host and friend will sit opposite to each other
        if host.sex is 'm':
            host_list = men
            other_list = women
        else:
            host_list = women
            other_list = men
        host_index = host_list.index(host)
        friend_index = other_list.index(friend)
        (other_list[friend_index],
         other_list[host_index]) = (other_list[host_index],
                                    other_list[friend_index])


def swap_places(tables: dict, a: str, b: str) -> None:
    """Swap places of two people based on their names"""

    a_i = []
    b_i = []
    for name, table in tables.items():
        for idx, pair in enumerate(table):
            if pair[0].name == a:
                a_i.extend([name, idx, 0])
            if pair[1].name == a:
                a_i.extend([name, idx, 1])
            if pair[0].name == b:
                b_i.extend([name, idx, 0])
            if pair[1].name == b:
                b_i.extend([name, idx, 1])
    if len(a_i) + len(b_i) > 0:
        (tables[a_i[0]][a_i[1]][a_i[2]],
         tables[b_i[0]][b_i[1]][b_i[2]]) = (tables[b_i[0]][b_i[1]][b_i[2]],
                                            tables[a_i[0]][a_i[1]][a_i[2]])


if __name__ == '__main__':
    args = getArgs()
    if args.interactive:
        ask_args(args)
    data = args.file
    names = args.column
    sexes = args.sexes
    preference = args.preference
    allergies = args.allergies

    try:
        df = pd.read_csv(data)
    except FileNotFoundError:
        print("Could not find file, exiting")
        sys.exit()
    try:
        df['names'] = df[names]
        if sexes is not None:
            df['sexes'] = df[sexes]
        if preference is not None:
            df['preference'] = df[preference]
        else:
            df['preference'] = [None for x in df['names']]
        if allergies is not None:
            df['allergies'] = df[allergies]
        else:
            df['allergies'] = [None for x in df['names']]
    except KeyError as ke:
        print(f"Could not find column {ke.args[0]}, exiting")
        sys.exit()
    people = [Person(i, df) for i in range(len(df.index))]
    tables = randomize_tables(get_tables(), people)
    while True:
        outputstyle = input("""

Choose action:
swap NAME OTHER -- swap places for two people
print_table -- print tables to console
print_list -- print list of which person sits in which table
print_allergies -- prints list of all peolpe with alleriges
save_table -- save tables as a pdf
save_allergy_table -- same as save table but people with allergies will have
                      colored names
save_list -- save a list of all people and which table they sit in
save_allergy_list -- save a list of all people with allergies
exit -- exit script

 """)
        if outputstyle == 'print_table':
            print_tables(tables)
        elif outputstyle == 'print_list':
            print_person_table_list(tables)
        elif outputstyle == 'print_allergies':
            print_allergies(tables)
        elif outputstyle == 'save_table':
            save_tables(tables)
        elif outputstyle == 'save_allergy_table':
            save_tables(tables, allergies=True)
        elif outputstyle == 'save_list':
            save_list(tables)
        elif outputstyle == 'save_allergy_list':
            save_list(tables, allergies=True)
        elif outputstyle.split(" ")[0] == "swap":
            _, name1, name2 = outputstyle.split(" ")
            swap_places(tables, name1, name2)
            print_tables(tables)
        elif outputstyle == '' or outputstyle == 'exit':
            print("Exiting...")
            sys.exit()
