import argparse
import sys
from random import shuffle
import readchar
import pandas as pd
from print_tables import print_tables


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


def define_sex(names: list, sexes: list) -> dict:
    if sexes is not None:
        people_s = list(zip(names, sexes))
        women = [x[0] for x in list(people_s) if x[1] is 'w']
        men = [x[0] for x in list(people_s) if x[1] is not 'w']
        print(len(women) + len(men))
        names = []
    else:
        women = []
        men = []
    for name in names:
        print(f"Is {name} a man/Woman? (M/w) ")
        if readchar.readchar() is 'w':
            women.append(name)
        else:
            men.append(name)
    if len(men) > len(women):
        difference = (len(men) - len(women)) // 2
        women.extend(men[-difference:])
        del men[-difference:]
    elif len(women) > len(men):
        difference = len(women) - len(men)
        men.extend(women[-difference:])
        del women[-difference:]
    return {'men': men, 'women': women}


def randomize_tables(tables: dict, sexes=None) -> dict:
    people = define_sex(names, sexes)
    [shuffle(v) for (k, v) in people.items()]
    for table, size in tables.items():
        tables[table] = []
        for seat in range(size):
            pair = []
            if seat % 2 is 0:
                if people['men']:
                    pair.append(people['men'].pop(0))
                else:
                    pair.append(' ')
                if people['women']:
                    pair.append(people['women'].pop(0))
                else:
                    pair.append(' ')
            else:
                if people['women']:
                    pair.append(people['women'].pop(0))
                else:
                    pair.append(' ')
                if people['men']:
                    pair.append(people['men'].pop(0))
                else:
                    pair.append(' ')
            tables[table].append(pair)

    return tables


def add_friend(men: list, women: list, friend: str) -> None:
    pass


if __name__ == '__main__':
    args = getArgs()
    data = args.file
    names = args.column
    if args.sexes is None:
        sexes = None
    else:
        sexes = args.sexes

    preference = args.preference
    try:
        df = pd.read_csv(data)
    except FileNotFoundError:
        print("Could not find file, exiting")
        sys.exit()
    try:
        names = df[names]
        if sexes is not None:
            sexes = df[sexes]
    except KeyError as ke:
        print(f"Could not find column {ke.args}, exiting")
        sys.exit()
    print_tables(randomize_tables(get_tables(), sexes))
