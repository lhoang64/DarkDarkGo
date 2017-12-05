#! /usr/bin/env python3
"""
    database_manager_test.py - Database Manager Test
    Author:
        - Hoanh An (hoanhan@bennington.edu)
    Date: 12/2/2017
"""

from database_manager import DatabaseManager
from pprint import pprint

def test_link_operation():
    """
    Test link relation's basic operations.
    :return: None
    """
    db_manager = DatabaseManager()

    db_manager.operate_on_link_relation('INSERT', link='https://www.example_101.com')
    if db_manager.get_relation('link')[-1]['link'] == 'https://www.example_101.com':
        print('> Link relation: Test passed for INSERT ')
    else:
        print('> Link relation: Test failed for INSERT ')

    db_manager.operate_on_link_relation('UPDATE_STATE', link='https://www.example_101.com', state='crawling')
    if db_manager.get_relation('link')[-1]['state'] == 'crawling':
        print('> Link relation: Test passed for UPDATE_STATE ')
    else:
        print('> Link relation: Test failed for UPDATE_STATE ')

    db_manager.operate_on_link_relation('UPDATE_CHUNK_ID', link='https://www.example_101.com', chunk_id=1)
    if db_manager.get_relation('link')[-1]['chunk_id'] == 1:
        print('> Link relation: Test passed for UPDATE_CHUNK_ID ')
    else:
        print('> Link relation: Test failed for UPDATE_CHUNK_ID ')

    db_manager.operate_on_link_relation('DELETE', link='https://www.example_101.com')
    if db_manager.get_relation('link')[-1]['link'] != 'https://www.example_101.com':
        print('> Link relation: Test passed for DELETE ')
    else:
        print('> Link relation: Test failed for DELETE ')

def test_chunk_operation():
    """
    Test chunk relation's basic operations.
    :return: None
    """
    db_manager = DatabaseManager()

    db_manager.operate_on_chunk_relation('INSERT', chunk_id=102)
    if db_manager.get_relation('chunk')[-1]['id'] == 102:
        print('> Chunk relation: Test passed for INSERT')

    db_manager.operate_on_chunk_relation('DELETE', chunk_id=102)
    if db_manager.get_relation('chunk')[-1]['id'] != 102:
        print('> Chunk relation: Test passed for DELETE')

def test_host_operation():
    """
    Test host relation basic operations.
    :return: None
    """
    db_manager = DatabaseManager()

    db_manager.operate_on_host_relation('INSERT', host='101.101.101.101:102', type='Crawler')
    if db_manager.get_relation('host')[-1]['host'] == '101.101.101.101:102':
        print('> Host relation: Test passed for INSERT')
    else:
        print('> Host relation: Test failed for INSERT')

    db_manager.operate_on_host_relation('UPDATE_STATE', host='101.101.101.101:102', state='online')
    if db_manager.get_relation('host')[-1]['state'] == 'online':
        print('> Host relation: Test passed for UPDATE_STATE')
    else:
        print('> Host relation: Test failed for UPDATE_STATE')

    db_manager.operate_on_host_relation('UPDATE_HEALTH', host='101.101.101.101:102', health='healthy')
    if db_manager.get_relation('host')[-1]['health'] == 'healthy':
        print('> Host relation: Test passed for UPDATE_HEALTH')
    else:
        print('> Host relation: Test failed for UPDATE_HEALTH')

    db_manager.operate_on_host_relation('DELETE', host='101.101.101.101:102')
    if db_manager.get_relation('host')[-1]['host'] != '101.101.101.101:102':
        print('> Host relation: Test passed for DELETE')
    else:
        print('> Host relation: Test failed for DELETE')

def test_crawler_operation():
    """
    Test crawler relation basic operations.
    :return: None
    """
    db_manager = DatabaseManager()

    db_manager.operate_on_crawler_relation('INSERT', chunk_id=101)
    if db_manager.get_relation('crawler')[-1]['chunk_id'] == 101:
        print('> Crawler relation: Test passed for INSERT')
    else:
        print('> Crawler relation: Test failed for INSERT')

    db_manager.operate_on_crawler_relation('UPDATE_TASK', chunk_id=101, task='crawled')
    if db_manager.get_relation('crawler')[-1]['c_task'] == 'crawled':
        print('> Crawler relation: Test passed for UPDATE_TASK')
    else:
        print('> Crawler relation: Test failed for UPDATE_TASK')

    db_manager.operate_on_crawler_relation('DELETE', chunk_id=101)
    if db_manager.get_relation('crawler')[-1]['chunk_id'] != 101:
        print('> Crawler relation: Test passed for DELETE')
    else:
        print('> Crawler relation: Test failed for DELETE')

def test_index_builder_operation():
    """
    Test index builder relation basic operations.
    :return: None
    """
    db_manager = DatabaseManager()

    db_manager.operate_on_index_builder_relation('INSERT', chunk_id=101)
    if db_manager.get_relation('index_builder')[-1]['chunk_id'] == 101:
        print('> Index Builder relation: Test passed for INSERT')
    else:
        print('> Index Builder relation: Test failed for INSERT')

    db_manager.operate_on_index_builder_relation('UPDATE_HOST', chunk_id=101, host='10.10.127.102:5000')
    if db_manager.get_relation('index_builder')[-1]['ib_host'] == '10.10.127.102:5000':
        print('> Index Builder relation: Test passed for UPDATE_HOST')
    else:
        print('> Index Builder relation: Test failed for UPDATE_HOST')

    db_manager.operate_on_index_builder_relation('UPDATE_TASK', chunk_id=101, task='built')
    if db_manager.get_relation('index_builder')[-1]['ib_task'] == 'built':
        print('> Index Builder relation: Test passed for UPDATE_TASK')
    else:
        print('> Index Builder relation: Test failed for UPDATE_TASK')

    db_manager.operate_on_index_builder_relation('DELETE', chunk_id=101)
    if db_manager.get_relation('index_builder')[-1]['chunk_id'] != 101:
        print('> Index Builder relation: Test passed for DELETE')
    else:
        print('> Index Builder relation: Test failed for DELETE')

def test_index_server_operation():
    """
    Test index server basic operations.
    :return: None
    """
    db_manager = DatabaseManager()

    db_manager.operate_on_index_server_relation('INSERT', row=0, chunk_id=101)
    if db_manager.get_relation('index_server')[-1]['chunk_id'] == 101:
        print('> Index Server relation: Test passed for INSERT')
    else:
        print('> Index Server relation: Test failed for INSERT')

    db_manager.operate_on_index_server_relation('UPDATE_ROW', row=3, chunk_id=101, host='101.101.101.101:101')
    if db_manager.get_relation('index_server')[-1]['row'] == 3:
        print('> Index Server relation: Test passed for UPDATE_ROW')
    else:
        print('> Index Server relation: Test failed for UPDATE_ROW')

    db_manager.operate_on_index_server_relation('UPDATE_CHUNK_ID', chunk_id=1, row=3,  host='101.101.101.101:101')
    if db_manager.get_relation('index_server')[-1]['chunk_id'] == 1:
        print('> Index Server relation: Test passed for UPDATE_CHUNK_ID')
    else:
        print('> Index Server relation: Test failed for UPDATE_CHUNK_ID')

    db_manager.operate_on_index_server_relation('UPDATE_HOST', host='10.10.127.101:5000', row=3, chunk_id=1)
    if db_manager.get_relation('index_server')[-1]['is_host'] == '10.10.127.101:5000':
        print('> Index Server relation: Test passed for UPDATE_HOST')
    else:
        print('> Index Server relation: Test failed for UPDATE_HOST')

    db_manager.operate_on_index_server_relation('DELETE', row=3, chunk_id=1, host='10.10.127.101:5000')
    if db_manager.get_relation('index_server')[-1]['chunk_id'] != 1:
        print('> Index Server relation: Test passed for DELETE')
    else:
        print('> Index Server relation: Test failed for DELETE')

if __name__ == '__main__':
    test_link_operation()
    test_chunk_operation()
    test_host_operation()
    test_crawler_operation()
    test_index_builder_operation()
    test_index_server_operation()
