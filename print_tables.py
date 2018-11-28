"""
Prints the tables in terminal

Empty tables will be the same size and have the word empty on them
"""


def print_tables(tables: dict) -> None:
    for name, table in tables.items():
        print(f"\n{' ' * 30}{name}\n\n")
        if type(table) is int:
            print("""                        +--------------+
                        |      E       |
                        |      M       |
                        |      P       |
                        |      T       |
                        |      Y       |
                        +--------------+

                  """)
            continue

        for row in table:
            if row is table[0]:
                pad = 20 - len(row[0])
                print(f"{' ' * pad}{row[0]}    +---------------+    {row[-1]}")
                print(f"{' ' * 24}|{' ' * 15}|")
            elif row is table[-1]:
                pad = 20 - len(row[0])
                print(f"{' ' * pad}{row[0]}    +---------------+    {row[-1]}")
                print("\n\n\n")
            else:
                pad = 20 - len(row[0])
                print(f"{' ' * pad}{row[0]}    |               |    {row[-1]}")
                print(f"{' ' * 24}|{' ' * 15}|")
