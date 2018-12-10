# Table Shuffle

This is a simple script for doing seating order for parties etc.

It reads data from a csv-file with names and randomly shuffles them around tables of user defined count and size.

## Installation
Make sure you have python and pip installed.

```
# Clone this repo: 
git clone https://github.com/tobbe-j/table-shuffle.git

# Go into the directory:
cd tabel-shuffle/

# install python dependencies: 
pip install -r requirements.txt
```

## Usage
The script needs the filename of the csv-file and also the names of the columns with the data.
The script can either be used by supplying all the required column names with their appropriate flag or by using the `-i` interactive flag to input the column names interactively.
To see these options in the terminal `-h` or `--help` can be used.
The column are:


| Column | Flag | Usage | Required |
| --- | --- | --- | --- |
| Names | `-c` or `--column` | The most important one with the names of all the people. | Yes |
| Sexes | `-s` or `--sexes`| A column with either 'm' or 'w' for man/woman. If no column is supplied this can also be filled in interacively | No |
| Preference | `-p` or `--preference` | Wishes for who everyone would like to sit close to | No |
| Allergies | `-a` or `--alleriges` | Information about allergies or every person. | No |

Example:

`python table_shuffle.py "party-list.csv" -i` or 

`python table_shuffle.py "party-list.csv" -c "names" -s "m/w" -p "buddy" -a "allergies"`

You then need to specify table count and names and sizes for all tables. The tables will be filled as far aspossible with all people available and then be empty at the end.

## Output formats
The script currently supports outputting the result in different forms in the terminal for viewing and editing the seating order. When the order is ready it can be saves as a pdf in a couple of different ways. It can be saved as tables with or without coloring of peoples names o show alleriges. It can also be saved as a alphabetically ordered list of all people showing which table they sit in. A list with all people with allergies can also be saved. 

You can also manually swap places for two people if you have requirements where some people need to sit.
```
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
```
### Limitations
There are some limitations for how people can be seated.

The script can only automatically add one avec per person. If many people form
an avec-chain it will also fail. The rest of the preferences need to be added
manually (using the swap command).

The script has a hard time coloring people with multiple allergies, those need
to be checked manually.

The maximum table size is 30 - otherwise the table will not fit on one page
when saved.
