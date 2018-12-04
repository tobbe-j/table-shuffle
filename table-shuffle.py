import argparse
import sys
import random
import pandas as pd
from itertools import zip_longest
from save_table import save_tables
from print_tables import print_tables, print_person_table_list, print_allergies
from person import Person, Empty


def getArgs(argvals=None):
    parser = argparse.ArgumentParser(description='Seating order from csv')
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


def get_tables():
    print('Setting up table count and sizes:')
    nr_tables = 0
    while (type(nr_tables) is not int or nr_tables <= 0):
        nr_tables = int(input("How many tables? "))

    tables = {}
    for table in range(nr_tables):
        name = ""
        while type(name) is not str or len(name) <= 0:
            name = input("Name for this table? ")
        size = 0
        while(type(size) is not int or size <= 0):
            size = int(input(f"How long is table nr {table + 1}? "))
            tables[name] = size
    return tables


def balance_sex(men: list, women: list):
    if len(men) > len(women):
        difference = (len(men) - len(women)) // 2
        for m in men[-difference:]:
            m.sex = 'w'
        women.extend(men[-difference:])
        del men[-difference:]
    elif len(women) > len(men):
        difference = len(women) - len(men)
        for w in women[-difference:]:
            w.sex = 'm'
        men.extend(women[-difference:])
        del women[-difference:]
    return [men, women]


def randomize_tables(tables: dict, people: list) -> dict:
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
            add_friend(men, women, person)
    people = list(zip_longest(men, women, fillvalue=Empty()))
    for table, size in tables.items():
        tables[table] = []
        for seat in range(size):
            pair = ()
            if len(people) is 0:
                pair = (Empty(), Empty())
            else:
                if seat % 2 is 0:
                    pair = people.pop(0)
                else:
                    pair = people.pop(0)[::-1]
            for p in pair:
                p.table = table
            tables[table].append(pair)

    return tables


def add_friend(men: list, women: list, host: Person) -> None:
    print(f"Adding friend to {host}")
    friend = {x.name: x for x in men + women}.get(host.preference, "")
    if type(friend) is str or host.sits_with_friend or friend.sits_with_friend:
        print("returning")
        return
    host.sits_with_friend = True
    friend.sits_with_friend = True
    if host.sex is friend.sex:
        if host.sex is 'm':
            swap_list = men
        else:
            swap_list = women
        host_index = swap_list.index(host)
        friend_index = swap_list.index(friend)
        if host_index + 2 < len(swap_list):
            (swap_list[friend_index],
             swap_list[host_index + 1]) = (swap_list[host_index + 1],
                                           swap_list[friend_index])
        else:
            (swap_list[friend_index],
             swap_list[host_index - 1]) = (swap_list[host_index - 1],
                                           swap_list[friend_index])
    else:
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


if __name__ == '__main__':
    args = getArgs()
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
        if allergies is not None:
            df['allergies'] = df[allergies]
        else:
            df['allergies'] = [None for x in df['names']]
    except KeyError as ke:
        print(f"Could not find column {ke.args}, exiting")
        sys.exit()
    people = [Person(i, df) for i in range(len(df.index))]
    tables = randomize_tables(get_tables(), people)
    while True:
        outputstyle = input("""Choose output format:
print_table -- print tables to console
print_list -- print list of which person sits in which table
print_allergies -- prints list of all peolpe with alleriges
save_table -- save tables as a pdf
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
        elif outputstyle == '' or outputstyle == 'exit':
            print("Exiting...")
            sys.exit()
