"""
Process SQuEaL queries from the keyboard and print the results.
"""

import db_io
import squeal

def main():
    """ () -> NoneType

    Ask for queries from the keyboard; stop when empty line is received. For
    each query, process it and use db_io.print_csv to print the results.
    """
    #Loads all tables in current directory
    database = db_io.read_database()

    #Continually asks for and processes queries until nothing is entered
    query = input('Please enter a query (or press return to exit):')
    while query != '':
        table = squeal.process_query(query, database)
        db_io.print_csv(table)
        query = input('Please enter a query (or press return to exit):')


if __name__ == '__main__':
    main()
