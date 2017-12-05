#! /usr/bin/env python3
"""
    database_manager_test.py - Database Manager Test
    Author:
        - Hoanh An (hoanhan@bennington.edu)
    Date: 12/2/2017
"""

from mgmt.src.database_manager import DatabaseManager
from pprint import pprint

def test_link_operation():
    """
    Test link relation's basic operations.
    :return: None
    """
    db_manager = DatabaseManager()
    start_length = db_manager.get_length('link')

    # INSERT
    db_manager.operate_on_link_relation('INSERT', link='https://www.example_101.com')
    if db_manager.get_relation('link')[-1]['link'] == 'https://www.example_101.com' and db_manager.get_relation('link')[-1]['state'] == 'pending':
        print('> Link relation: Test passed for INSERT ')
    else:
        print('> Link relation: Test failed for INSERT ')

    # UPDATE STATE
    db_manager.operate_on_link_relation('UPDATE_STATE', link='https://www.example_101.com', state='crawling')
    if db_manager.get_relation('link')[-1]['state'] == 'crawling':
        print('> Link relation: Test passed for UPDATE_STATE ')
    else:
        print('> Link relation: Test failed for UPDATE_STATE ')

    # UPDATE CHUNK ID
    db_manager.operate_on_chunk_relation('INSERT', chunk_id='101c')
    db_manager.operate_on_link_relation('UPDATE_CHUNK_ID', link='https://www.example_101.com', chunk_id='101c')
    if db_manager.get_relation('link')[-1]['chunk_id'] == '101c':
        print('> Link relation: Test passed for UPDATE_CHUNK_ID ')
    else:
        print('> Link relation: Test failed for UPDATE_CHUNK_ID ')
    db_manager.operate_on_chunk_relation('DELETE', chunk_id='101c')

    # DELETE
    db_manager.operate_on_link_relation('DELETE', link='https://www.example_101.com')
    if db_manager.get_length('link') == start_length:
        print('> Link relation: Test passed for DELETE ')
    else:
        print('> Link relation: Test failed for DELETE ')

def test_chunk_operation():
    """
    Test chunk relation's basic operations.
    :return: None
    """
    db_manager = DatabaseManager()
    start_length = db_manager.get_length('chunk')

    # INSERT
    db_manager.operate_on_chunk_relation('INSERT', chunk_id='101c')
    if db_manager.get_relation('chunk')[-1]['id'] == '101c':
        print('> Chunk relation: Test passed for INSERT')
    else:
        print('> Chunk relation: Test failed for INSERT')

    # DELETE
    db_manager.operate_on_chunk_relation('DELETE', chunk_id='101c')
    if db_manager.get_length('chunk') == start_length:
        print('> Chunk relation: Test passed for DELETE')
    else:
        print('> Chunk relation: Test failed for DELETE')

def test_host_operation():
    """
    Test host relation basic operations.
    :return: None
    """
    db_manager = DatabaseManager()
    start_length = db_manager.get_length('host')

    # INSERT
    db_manager.operate_on_host_relation('INSERT', host='101.101.101.101:101', type='Crawler')
    if db_manager.get_relation('host')[-1]['host'] == '101.101.101.101:101' and db_manager.get_relation('host')[-1]['state'] == 'offline':
        print('> Host relation: Test passed for INSERT')
    else:
        print('> Host relation: Test failed for INSERT')

    # UPDATE STATE
    db_manager.operate_on_host_relation('UPDATE_STATE', host='101.101.101.101:101', state='online')
    if db_manager.get_relation('host')[-1]['state'] == 'online':
        print('> Host relation: Test passed for UPDATE_STATE')
    else:
        print('> Host relation: Test failed for UPDATE_STATE')

    # UPDATE HEALTH
    db_manager.operate_on_host_relation('UPDATE_HEALTH', host='101.101.101.101:101', health='healthy')
    if db_manager.get_relation('host')[-1]['health'] == 'healthy':
        print('> Host relation: Test passed for UPDATE_HEALTH')
    else:
        print('> Host relation: Test failed for UPDATE_HEALTH')

    # DELETE
    db_manager.operate_on_host_relation('DELETE', host='101.101.101.101:101')
    if db_manager.get_length('host') == start_length:
        print('> Host relation: Test passed for DELETE')
    else:
        print('> Host relation: Test failed for DELETE')

def test_crawler_operation():
    """
    Test crawler relation basic operations.
    :return: None
    """
    db_manager = DatabaseManager()
    start_length = db_manager.get_length('crawler')

    # Setup temp chunk and host for testing
    db_manager.operate_on_chunk_relation('INSERT', chunk_id='101c')
    db_manager.operate_on_host_relation('INSERT', host='101.101.101.101:101', type='Crawler')
    db_manager.operate_on_host_relation('INSERT', host='101.101.101.101:102', type='Crawler')

    # INSERT
    db_manager.operate_on_crawler_relation('INSERT', chunk_id='101c', host='101.101.101.101:101')
    if db_manager.get_relation('crawler')[-1]['chunk_id'] == '101c' and db_manager.get_relation('crawler')[-1]['c_task'] == 'crawling':
        print('> Crawler relation: Test passed for INSERT')
    else:
        print('> Crawler relation: Test failed for INSERT')

    # UPDATE HOST
    db_manager.operate_on_crawler_relation('UPDATE_HOST', chunk_id='101c', host='101.101.101.101:102')
    if db_manager.get_relation('crawler')[-1]['c_host'] == '101.101.101.101:102':
        print('> Crawler relation: Test passed for UPDATE_HOST')
    else:
        print('> Crawler relation: Test failed for UPDATE_HOST')

    # UPDATE TASK
    db_manager.operate_on_crawler_relation('UPDATE_TASK', chunk_id='101c', task='crawled')
    if db_manager.get_relation('crawler')[-1]['c_task'] == 'crawled':
        print('> Crawler relation: Test passed for UPDATE_TASK')
    else:
        print('> Crawler relation: Test failed for UPDATE_TASK')

    # DELETE
    db_manager.operate_on_crawler_relation('DELETE', chunk_id='101c')
    if db_manager.get_length('crawler') == start_length:
        print('> Crawler relation: Test passed for DELETE')
    else:
        print('> Crawler relation: Test failed for DELETE')

    # Delete temp chunk and host when finish testing
    db_manager.operate_on_chunk_relation('DELETE', chunk_id='101c')
    db_manager.operate_on_host_relation('DELETE', host='101.101.101.101:101')
    db_manager.operate_on_host_relation('DELETE', host='101.101.101.101:102')

def test_index_builder_operation():
    """
    Test index builder relation basic operations.
    :return: None
    """
    db_manager = DatabaseManager()
    start_length = db_manager.get_length('index_builder')

    # Setup temp chunk and host for testing
    db_manager.operate_on_chunk_relation('INSERT', chunk_id='101c')
    db_manager.operate_on_host_relation('INSERT', host='101.101.101.101:101', type='Index Builder')
    db_manager.operate_on_host_relation('INSERT', host='101.101.101.101:102', type='Index Builder')

    # INSERT
    db_manager.operate_on_index_builder_relation('INSERT', chunk_id='101c', host='101.101.101.101:101')
    if db_manager.get_relation('index_builder')[-1]['chunk_id'] == '101c' and db_manager.get_relation('index_builder')[-1]['ib_task'] == 'building':
        print('> Index Builder relation: Test passed for INSERT')
    else:
        print('> Index Builder relation: Test failed for INSERT')

    # UPDATE HOST
    db_manager.operate_on_index_builder_relation('UPDATE_HOST', chunk_id='101c', host='101.101.101.101:102')
    if db_manager.get_relation('index_builder')[-1]['ib_host'] == '101.101.101.101:102':
        print('> Index Builder relation: Test passed for UPDATE_HOST')
    else:
        print('> Index Builder relation: Test failed for UPDATE_HOST')

    # UPDATE TASK
    db_manager.operate_on_index_builder_relation('UPDATE_TASK', chunk_id='101c', task='built')
    if db_manager.get_relation('index_builder')[-1]['ib_task'] == 'built':
        print('> Index Builder relation: Test passed for UPDATE_TASK')
    else:
        print('> Index Builder relation: Test failed for UPDATE_TASK')

    # DELETE
    db_manager.operate_on_index_builder_relation('DELETE', chunk_id='101c')
    if db_manager.get_length('index_builder') == start_length:
        print('> Index Builder relation: Test passed for DELETE')
    else:
        print('> Index Builder relation: Test failed for DELETE')

    # Delete temp chunk and host when finish testing
    db_manager.operate_on_chunk_relation('DELETE', chunk_id='101c')
    db_manager.operate_on_host_relation('DELETE', host='101.101.101.101:101')
    db_manager.operate_on_host_relation('DELETE', host='101.101.101.101:102')

def test_index_server_operation():
    """
    Test index server basic operations.
    :return: None
    """
    db_manager = DatabaseManager()
    start_length = db_manager.get_length('index_server')

    # Setup temp chunk and host for testing
    db_manager.operate_on_chunk_relation('INSERT', chunk_id='101c')
    db_manager.operate_on_chunk_relation('INSERT', chunk_id='102c')
    db_manager.operate_on_host_relation('INSERT', host='101.101.101.101:101', type='Index Server')
    db_manager.operate_on_host_relation('INSERT', host='101.101.101.101:102', type='Index Server')

    # INSERT
    db_manager.operate_on_index_server_relation('INSERT', row=101, chunk_id='101c', host='101.101.101.101:101')
    if db_manager.get_relation('index_server')[-1]['chunk_id'] == '101c' and db_manager.get_relation('index_server')[-1]['row'] == 101:
        print('> Index Server relation: Test passed for INSERT')
    else:
        print('> Index Server relation: Test failed for INSERT')

    # UPDATE ROW
    db_manager.operate_on_index_server_relation('UPDATE_ROW', row=102, chunk_id='101c', host='101.101.101.101:101')
    if db_manager.get_relation('index_server')[-1]['row'] == 102:
        print('> Index Server relation: Test passed for UPDATE_ROW')
    else:
        print('> Index Server relation: Test failed for UPDATE_ROW')

    # UPDATE CHUNK ID
    db_manager.operate_on_index_server_relation('UPDATE_CHUNK_ID', chunk_id='102c', row=102, host='101.101.101.101:101')
    if db_manager.get_relation('index_server')[-1]['chunk_id'] == '102c':
        print('> Index Server relation: Test passed for UPDATE_CHUNK_ID')
    else:
        print('> Index Server relation: Test failed for UPDATE_CHUNK_ID')

    # UPDATE HOST
    db_manager.operate_on_index_server_relation('UPDATE_HOST', host='101.101.101.101:102', row=102, chunk_id='102c')
    if db_manager.get_relation('index_server')[-1]['is_host'] == '101.101.101.101:102':
        print('> Index Server relation: Test passed for UPDATE_HOST')
    else:
        print('> Index Server relation: Test failed for UPDATE_HOST')

    # DELETE
    db_manager.operate_on_index_server_relation('DELETE', row=102, chunk_id='102c', host='101.101.101.101:102')
    if db_manager.get_length('index_server') == start_length:
        print('> Index Server relation: Test passed for DELETE')
    else:
        print('> Index Server relation: Test failed for DELETE')

    # Delete temp chunk and host when finish testing
    db_manager.operate_on_chunk_relation('DELETE', chunk_id='101c')
    db_manager.operate_on_chunk_relation('DELETE', chunk_id='102c')
    db_manager.operate_on_host_relation('DELETE', host='101.101.101.101:101')
    db_manager.operate_on_host_relation('DELETE', host='101.101.101.101:102')

if __name__ == '__main__':
    test_link_operation()
    test_chunk_operation()
    test_host_operation()
    test_crawler_operation()
    test_index_builder_operation()

    db_manager = DatabaseManager()
    results = db_manager.get_all_relations_for_all_chunks()
    pprint(results)
