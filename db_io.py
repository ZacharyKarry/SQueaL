"""Module db_io: functions for I/O on tables and databases.

A table file has a .csv extension.

We define "table" to mean this:

    dict of {str: list of str}

Each key is a column name from the table and each value is the list of strings
in that column from top row to bottom row.

We define "database" to mean this:

    dict of {str: table}

Each key is the name of the .csv file without the extension.  Each value is
the corresponding table as defined above.
"""

import glob


def print_csv(table):
    """ (table) -> NoneType

    Print a representation of table in the same format as a table file.
    """

    columns = list(table.keys())
    print(','.join(columns))

    for i in range(len(table[columns[0]])):
        cur_column = []
        for column in columns:
            cur_column.append(table[column][i])
        print(','.join(cur_column))

# Write your read_table and read_database functions below.
def read_table(file):
    """(file open for reading) -> table

    Takes an open .csv file and returns a table (aka. a dictionary where
    the key is a column header, and and the associated values are a list
    of the items in the column in order)
    """
    table = {}

    #Creates a list of lists, where the first list is of column titles
    #and subsequent lists are the items in each of those columns in order
    #for example [[c1, c2, c3],[1, 2, 3],[1, 2, 3]...
    lines = file.readlines()
    rows = []
    for line in lines:
        temprow = line.strip()
        rows.append(temprow.split(','))

    #Creates the column in the table using an item in the first list,
    #and then populates each of those columns with its items
    count = 0
    column_headers = rows[0]
    for header in column_headers:
        table[header] = []
        for row in rows[1:]:
            table[header].append(row[count])
        count += 1

    return table

def read_database():
    """() -> database

    When called returns a database, which is a compendium of all tables
    stored in a dictionary where the key is the filename and the value
    is the table.
    """
    #Makes a list of all table files in the directory
    files = glob.glob('*csv')
    database = {}

    #Opens each file and creates a table, then puts it into a dictionary
    #where the key is the filename
    for file in files:
        csv_table = open(file)
        database[file]=read_table(csv_table)
    return database




# Use glob.glob('*.csv') to return a list of csv filenames from
#   the current directory.
