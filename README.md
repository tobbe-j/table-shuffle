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
The script currently supports outputting the result in different forms in the terminal, and also saving a version of the tables with everyone in their right places. The saved version also supports coloring peoples names accoring to their allergies.

You can alos manually swap places for two people if you have requirements where some people need to sit.
```
Choose action:
swap NAME OTHER -- swap places for two people
print_table -- print tables to console
print_list -- print list of which person sits in which table
print_allergies -- prints list of all peolpe with alleriges
save_table -- save tables as a pdf
save_allergy_table -- same as save table but people with allergies will have
                      colored names
exit -- exit script
```
