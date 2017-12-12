#! /usr/bin/env python3
"""
    utils.py - Helper functions
    Author:
        - Nidesh Chitrakar (nideshchitrakar@bennington.edu)
        - Hoanh An (hoanhan@bennington.edu)
    Date: 11/28/2017
"""

from database_manager import DatabaseManager
from constants import number_of_rows

id_counter = 0

db_manager = DatabaseManager()

def generate_chunk_id():
    """
    Generate chunk id as integer and concat with an alphabet 'c'
    :return: String
    """
    global id_counter
    id_counter += 1
    return str(id_counter) + 'c'


def distribute_index_servers():
    """
    Distribute a list of index servers to a set number of rows
    :return: List
    """
    rows = []

    index_servers = db_manager.get_all_index_servers()
    try:
        number_of_index_servers = len(index_servers)
        number_of_columns = int(number_of_index_servers / number_of_rows)
        row_count = 1

        k = 0  # the index in index_servers array
        while number_of_index_servers > 0:
            for i in range(0, number_of_rows):
                servers_in_row = []
                for j in range(0, number_of_columns):
                    servers_in_row.append(index_servers[k]['host'])
                    k += 1
                    number_of_index_servers -= 1
                rows.append({'current_index': 0,
                             'row_num': row_count,
                             'row': servers_in_row})
                row_count += 1
            for i in range(0, number_of_index_servers):
                rows[i]['row'].append(index_servers[k]['host'])
                k += 1
                number_of_index_servers -= 1
    except Exception as e:
        print(e)

    return rows


def assign_index_chunk(rows, chunk_id):
    """
    Assign chunk id to Index Servers that has been distributed into rows
    :param rows: Array of index servers representing rows
    :param chunk_id: Chunk ID to assign
    :return: None
    """
    for row in rows:
        current_index = row['current_index']

        # if index reaches the last element, reset to 0
        row['current_index'] = current_index + 1

        if row['current_index'] >= len(row['row']):
            row['current_index'] = 0
        db_manager.operate_on_index_server_relation(function='INSERT',
                                                    row=row['row_num'],
                                                    chunk_id=chunk_id,
                                                    host=row['row'][current_index])
