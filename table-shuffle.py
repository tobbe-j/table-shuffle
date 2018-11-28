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


def define_sex(names: list) -> dict:
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


def randomize_tables(tables: dict) -> dict:
    people = define_sex(names)
    [shuffle(v) for (k, v) in people.items()]
    for table, size in tables.items():
        tables[table] = []
        for seat in range(size):
            try:
                if seat % 2 is 0:
                    tables[table].append([people['men'].pop(0),
                                         people['women'].pop(0)])
                else:
                    tables[table].append([people['women'].pop(0),
                                         people['men'].pop(0)])
            except IndexError:
                print('Out of people')
                tables[table].extend([" ", " "])

    return tables


if __name__ == '__main__':
    args = getArgs()
    data = args.file
    names = args.column
    try:
        df = pd.read_csv(data)
    except FileNotFoundError:
        print("Could not find file, exiting")
        sys.exit()
    try:
        names = df[names]
    except KeyError as ke:
        print(f"Could not find column {ke.args}, exiting")
        sys.exit()
    print_tables(randomize_tables(get_tables()))
