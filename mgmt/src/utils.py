#! /usr/bin/env python3
"""
    utils.py - Helper functions
    Author:
        - Nidesh Chitrakar (nideshchitrakar@bennington.edu)
        - Hoanh An (hoanhan@bennington.edu)
    Date: 11/28/2017
"""

from mgmt.src.database_manager import DatabaseManager
from pprint import pprint

id_counter = 0
number_of_rows = 3          # total number rows of Index Servers

db_manager = DatabaseManager()

def generate_chunk_id():
    """
    Generate chunk id as integer and concat with an alphabet 'c'.
    :return: String
    """
    global id_counter
    id_counter += 1
    return str(id_counter) + 'c'

def distribute_index_servers():
    """
    Distribute a list of servers to a given number of rows.
    :return: List
    """
    index_servers = db_manager.get_all_index_servers()
    number_of_index_servers = len(index_servers)
    number_of_columns = int(number_of_index_servers / number_of_rows)
    row_count = 1
    rows = []

    k = 0  # index in index_servers array
    while number_of_index_servers > 0:
        for i in range(0, number_of_rows):
            servers_in_row = []
            for j in range(0, number_of_columns):
                servers_in_row.append(index_servers[k]['host'])
                k += 1
                number_of_index_servers -= 1
            rows.append({'current_index': 0, 'row_num': row_count, 'row': servers_in_row})
            row_count += 1
        for i in range(0, number_of_index_servers):
            rows[i]['row'].append(index_servers[k]['host'])
            k += 1
            number_of_index_servers -= 1
    return rows

# rows = distribute_index_servers()

def assign_index_chunk(rows, chunk_id):
    """
    Assign chunk id to Index Servers that has been distributed into rows.
    :param chunk_id: Chunk ID
    :return: None
    """
    for row in rows:
        current_index = row['current_index']
        print('current_index = {0}'.format(current_index))
        # if index reaches the last element, reset to 0
        row['current_index'] = current_index + 1
        print('len = {0}'.format(len(row['row'])))
        if row['current_index'] >= len(row['row']):
            row['current_index'] = 0
        db_manager.operate_on_index_server_relation('INSERT',row=row['row_num'], chunk_id=chunk_id, host=row['row'][current_index])
        print(row['row'][current_index] + '\n')


if __name__ == '__main__':
    # rows_of_index_servers = distribute_index_servers()
    #
    # chunk_relation = db_manager.get_relation('chunk')
    # for chunk in chunk_relation:
    #     chunk_id = chunk['id']
    #     assign_index_chunk(rows_of_index_servers, chunk_id)

    index_server_relation = db_manager.get_relation('index_server')
    pprint(index_server_relation)

