"""
Prints the tables in terminal

Empty tables will be the same size and have the word empty on them
"""


def print_tables(tables: dict) -> None:
    for name, table in tables.items():
        print(f"\n{' ' * 30}{name}\n\n")
        if len(table[0][0]) is 0:
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
                pad = 20 - len(row[0])
                print(f"{' ' * pad}{row[0]}    +---------------+    {row[-1]}")
                print(f"{' ' * 24}|{' ' * 15}|")
            elif idx is (len(table)-1):
                pad = 20 - len(row[0])
                print(f"{' ' * pad}{row[0]}    +---------------+    {row[-1]}")
                print("\n\n\n")
            else:
                pad = 20 - len(row[0])
                print(f"{' ' * pad}{row[0]}    |               |    {row[-1]}")
                print(f"{' ' * 24}|{' ' * 15}|")
