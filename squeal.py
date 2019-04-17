""" Module squeal: table and database manipulation functions.

The meanings of "table" and "database" are as described in db_io.py.
"""

def num_of_rows(table):
    """(table) -> int
    Returns the number of rows in a chosen table.

    >>> table = {'m.year': ['1997', '2003', '2010']}
    >>> num_of_rows(table)
    3

    >>> table = {'o.year': ['2010', '2003', '1997', '1997']}
    >>> num_of_rows(table)
    4
    """
    #Initiates a for loop just to easily access the first item without
    #knowing what it is
    for first_item in table:
        return len(table[first_item])

def row_multiplier(table, num_of_times):
    """(table, int) -> table
    Takes a table, and returns a new table where every row is
    repeated in blocks of num_of_times. No mutation of original
    table occurs.

    >>> table = {'m.year': ['1997', '2000']}
    >>> row_multiplier(table, 2)
    {'m.year': ['1997', '1997', '2000', '2000']}
    """
    new_table = {}

    #In every column, this repeats the row num_of_times times
    for column in table:
        new_table[column] = []
        for row in table[column]:
            for times in range(num_of_times):
                new_table[column].append(row)

    return new_table

def row_repeater(table, num_of_repeats):
    """(table, int) -> table

    Takes a table, and returns a new table where the entire set of
    rows is repeated num_of_repeats times. No mutation of original
    table occurs.

    >>> table = {'m.year': ['1997', '2000']}
    >>> row_repeater(table, 2)
    {'m.year': ['1997', '2000', '1997', '2000']}
    """
    new_table = {}

    #In every column, repeats the rows over and over num_of_repeats times
    for column in table:
        new_table[column] = []
        for times in range(num_of_repeats):
            for row in table[column]:
                new_table[column].append(row)

    return new_table

def cartesian_product(table1, table2):
    """(table, table) -> table
    Combines two tables, and returns them as one table where all rows
    in table1 are matched up once with all rows in table 2. No mutation
    of original tables occurs.

    >>> table1 = {'m.year': ['1997', '2003']}
    >>> table2 = {'o.year': ['2010', '2000']}
    >>> cartesian_product(table1, table2)
    {'m.year': ['1997', '1997', '2003', '2003'],
     'o.year': ['2010', '2000', '2010', '2000']}
    """
    new_table = {}

    #These values make it very straightforward to populate our columns.
    rows1 = num_of_rows(table1)
    rows2 = num_of_rows(table2)

    #Populates new_table with the rows of table1 in groups of the number
    #of rows in table two
    new_table.update(row_multiplier(table1, rows2))

    #Populates new_table with the rows of table2 over and over
    #for each row in table1
    new_table.update(row_repeater(table2, rows1))

    return new_table

def where_same_index(column1, column2):
    """ (list of str, list of str) -> list of int

    Precondition: len(column1) = len(column2)

    Checks two columns and returns a list of all indices where
    column1 has the same value as column2.

    >>> where_same_index(['1', '1', '1'], ['1', '1', '0'])
    [0, 1]

    >>> where_same_index(['0', '1', '1'], ['1', '0', '0'])
    []
    """
    index_list = []
    number_of_rows = len(column1)

    #Appends list of indices where a match is found and returns it
    for index in range(number_of_rows):
        if column1[index] == column2[index]:
            index_list.append(index)

    return index_list

def where_greater_index(column1, column2):
    """(list of str, list of str) -> list of int

    Precondition: len(column1) = len(column2)

    Checks two columns and returns a list of all indices where
    column1 has a larger value than column2 (based on string
    comparison).

    >>> where_greater_index(['12', '23', '34'], ['34', '23', '12'])
    [2]

    >>> where_greater_index(['12', '23', '34'], ['345', '234', '123'])
    [2]
    """
    index_list = []

    #Appends list of indices where column1 is greater than column2
    for index in range(len(column1)):
        if column1[index] > column2[index]:
            index_list.append(index)

    return index_list

def where_same_value(column, value):
    """(list of str, str) -> list of int

    Checks a column for all indices where it matches the specified
    value. Returns a list of all indices where this condition is
    True.

    >>> where_same_value(['hello', 'world'], 'hello')
    [0]

    >>> where_same_value(['1', '2', '3', '4'], '5')
    []

    >>> where_same_value(['1', '1', '1'], '1')
    [0, 1, 2]
    """
    index_list = []

    #Appends list of indices where our column matches the value
    for index in range(len(column)):
        if column[index] == value:
            index_list.append(index)

    return index_list

def where_greater_value(column, value):
    """(list of str, str) -> list of int

    Checks a column for all indices where it is greater than the
    specified value (based on string comparison). Returns a list
    of all indices where this condition is True.

    >>> where_greater_value(['1', '2', '3'], '1')
    [1, 2]

    >>> where_greater_value(['1', '1', '1'], '1')
    []

    >>> where_greater_value(['1', '2', '3'], '10')
    [1, 2]
    """
    index_list = []

    #Appends list of indices where our column is greater than the value
    for index in range(len(column)):
        if column[index] > value:
            index_list.append(index)

    return index_list

def list_of_select(split_query_list):
    """(list of str) -> list of str

    Goes through a list of commands in a query and returns a list
    of the selected column names.

    >>> list_of_select(['select', 'm.a,o.a', 'from'])
    ['m.a', 'o.a']

    >>> list_of_select(['select', 'm.a', 'from'])
    ['m.a']
    """
    #Finds where the select token is and creates an easy to iterate
    #over list
    location = split_query_list.index('select') + 1
    select_list = split_query_list[location].split(',')

    return select_list

def list_of_from(split_query_list):
    """(list of str) -> list of str

    Goes through a list of commands in a query and returns a
    list of the desired tables.

    >>> list_of_from(['from', 'm,o', 'where'])
    ['m','o']

    >>> list_of_from(['from', 'o', 'where'])
    ['o']
    """
    #Finds where the from token is, and turns it into an easy to iterate
    #over list
    location = split_query_list.index('from') + 1
    from_string = split_query_list[location]
    from_list = from_string.split(',')

    return from_list

def list_of_where(split_query_list):
    """(list of str) -> list of str

    Precondition: 'where' is in split_query_list

    Goes through a list of commands in a query and returns a
    list where the first option is a column, the second is
    an operator, and the third is either a value or another
    column.

    >>> list_of_where(['m.o', 'where', 'm.a>o.a'])
    ['m.a', '>', 'o.a']

    >>> list_of_where(['m.o', 'where', "m.a='Toy", 'Story', "3'"])
    ['m.a', '=', "'Toy Story 3'"]
    """
    location = split_query_list.index('where') + 1
    where_string = split_query_list[location]

    #This rectifies any spaces in the 'value'
    if len(split_query_list) > location:
        for rest_of_value in split_query_list[location+1:]:
            #Spaces need to be replaced
            where_string += (' ' + rest_of_value)

    #Splits the query based on the operator, and then writes that
    #operator in between the two other parts
    if '=' in where_string:
        where_list = where_string.split('=')
        where_list.insert(1, '=')
    elif '>' in where_string:
        where_list = where_string.split('>')
        where_list.insert(1, '>')

    return where_list

def simplify_query(query):
    """(str) -> list of list of str

    Takes a valid query and outputs a list with 3 distinct blocks.
    First is a list of columns for 'select', second is a list of
    tables for 'from', and third is a list of a column, operator, and
    column/value for 'where'.

    >>> simplify_query("select m.a,o.a from m,o where m.a=o.a")
    [['m.a', 'o.a'], ['m', 'o'], ['m.a', '=', 'o.a']]

    >>> simplify_query("select * from m,o")
    [['*'], ['m','o'], []]

    >>> simplify_query("select m.a,o.a from m,o where m.a='s p a c e s'")
    [['m.a', 'o.a'], ['m', 'o'], ['m.a', '=', "'s p a c e s'"]]
    """
    query_list = []
    query = query.split()

    #Now that the query is split, all that needs to be done
    #is writing the desired elements to the list in order.
    query_list.append(list_of_select(query))
    query_list.append(list_of_from(query))

    #This conditional prevents errors if 'where' isn't present
    if 'where' in query:
        query_list.append(list_of_where(query))
    else:
        query_list.append([])

    return query_list

def apply_from(table_names, database):
    """(list of str, list of table) -> table

    Takes a list of table names, finds those tables in a database,
    and outputs the cartesian product of all those tables.

    >>> database =  {'ex1', {'m.year': ['1997', '2003']},
    ... 'ex2', {'o.year': ['2010', '2000']}}
    >>> apply_from('ex1', 'ex2')
    {'m.year': ['1997', '1997', '2003', '2003'],
     'o.year': ['2010', '2000', '2010', '2000']}
    """
    #The purpose of creating a list of the tables is to essentially
    #remove the .csv from the key. This makes it infinitely easier
    #to apply the cartesian product properly.
    table_list = []

    for name in table_names:
        table = database[name+'.csv']
        table_list.append(table)

    compendium = table_list[0]

    #Applies cartesian_product as many times as needed
    if len(table_list) > 1:
        for next_table in table_list[1:]:
            compendium = cartesian_product(compendium, next_table)
        return compendium
    else:
        return compendium

def apply_select(where_table, column_list):
    """(table, list of str) -> table

    Takes a list of column names, and selects those columns from a
    table that has already had from and where applied to it.

    ex_table = {'hello': ['1', '2', '3'], 'world': ['4', '5', '6']}
    >>> apply_select(ex_table, ['hello']
    {'hello': ['1', '2', '3']}

    ex_table = {'hello': ['1', '2', '3'], 'world': ['4', '5', '6']}
    >>> apply_select(ex_table, ['*'])
    {'hello': ['1', '2', '3'], 'world': ['4', '5', '6']}
    """
    output_table = {}

    #It doesn't need to alter the table at all if all columns are
    #selected (denoted by '*')
    if '*' in column_list:
        return where_table
    else:
        #Populates a new table with the selected tables.
        for column in column_list:
            output_table[column] = where_table[column]
        return output_table

def where_conditions_location(cartesian_table, conditions_list):
    """(table, list of str) -> list of int

    Determines which condition needs to be applied in the where
    token, and returns a list of rows where that particular
    condition is satisfied in the supplied table (which has already
    had cartesian_product applied to it).

    >>> table = {'m.y': ['1997', '1997', '2003', '2003'],
    ... 'o.y': ['2003', '1997', '2003', '1997']}
    >>> where_conditions_location(table, ['m.y', '=', 'o.y'])
    [1, 2]

    >>> table = {'m.y': ['1997', '1997', '2003', '2003'],
    ... 'o.y': ['2003', '1997', '2003', '1997']}
    >>> where_conditions_location(table, ['m.y', '>', "'2002'"])
    [2, 3]
    """
    operator = conditions_list[1]
    column_list = []
    column_list.append(cartesian_table[conditions_list[0]])

    #This part determines the format of the where token
    if conditions_list[2] in cartesian_table:
        column_list.append(cartesian_table[conditions_list[2]])
        value = ''
    else:
        value = conditions_list[2].strip("'")

    #Then based on the format, we just apply the proper operation
    return apply_operation(column_list, operator, value)

def apply_operation(column_list, operator, value):
    """(list of list, str, str) -> list

    Takes a list of columns, and applies the appropriate 'where'
    operation to them, based on what the operator is and whether
    the comparison is with a value or another column.

    >>> column_list = [['hello', 'hello'], ['hello', 'hello']]
    >>> apply_operation(column_list, '=', '')
    [0, 1]

    >>> column_list = [['hello', 'world'], ['how', 'you doin?']]
    >>> apply_operation(column_list, '=', '')
    []

    >>> column_list = [['how', 'you doin?']]
    >>> apply_operation(column_list, '=', 'you doin?')
    [1]
    """
    column1 = column_list[0]

    #Empty value implies that it is a column comparison
    if value == '':
        column2 = column_list[1]

    #This may seem complicated, but it is really just the 4
    #possible formats for where.
    if operator == "=" and value == '':
        return where_same_index(column1, column2)
    elif operator == "=" and  value != '':
        return where_same_value(column1, value)
    elif operator == ">" and value == '':
        return where_greater_index(column1, column2)
    elif operator == ">" and value != '':
        return where_greater_value(column1, value)

def apply_where(cartesian_table, conditions_list):
    """(table, list of str) -> table

    Takes the specified conditions from the where token and
    applies them to a "cartesian_product" table.

    >>> cartesian_table = {'a' : ['x', 'y', 'x', 'y'],
    ... 'b' : ['x', 'x', 'y', 'y']}
    >>> apply_where(cartesian_table, ['a', '=', 'b'])
    {'a': ['x', 'y'], 'b': ['x', 'y']}

    >>> cartesian_table = {'a' : ['x', 'y', 'x', 'y'],
    ... 'b' : ['x', 'x', 'y', 'y']}
    >>> apply_where(cartesian_table, ['a', '>', "'x'"])
    {'a': ['y', 'y'], 'b': ['x', 'y']}
    """
    #Row_list is essentially a list where the indicies of values meet
    #whatever our specified conditions are
    row_list = where_conditions_location(cartesian_table, conditions_list)
    new_table = {}

    #This then uses row_list to make a new table with only the rows
    #that we want
    for column in cartesian_table:
        new_table[column] = []
        for row in row_list:
            new_table[column].append(cartesian_table[column][row])
    return new_table

def process_query(query, database):
    """(str) -> table

    Takes a query, and applies it on the current database. Returns
    the final table that conforms to the query.

    >>> database =  {'ex1', {'m.year': ['1997', '2003']},
    ... 'ex2', {'o.year': ['2010', '2000']}}
    >>>process_query('select * from ex1,ex2 where m.year='1997')
    {'m.year' : ['1997', '1997'], 'o.year' : ['2010', '2000']}
    """
    simple_query = simplify_query(query)

    #For clarity in operations using a simplified query list of list
    select_place = 0
    from_place = 1
    where_place = 2

    #In order to get the right result we need to apply from, then
    #where, then select.
    step_from = apply_from(simple_query[from_place], database)

    #This part is checking if there is a where token and applying it
    #if necessary
    if simple_query[where_place] != []:
        step_where = apply_where(step_from, simple_query[where_place])
    else:
        step_where = step_from

    step_select = apply_select(step_where, simple_query[select_place])

    return step_select
