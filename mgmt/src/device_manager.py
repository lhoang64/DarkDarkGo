#! /usr/bin/env python3
"""
    device_manager.py - a central management system for the search engine
    Author: Nidesh Chitrakar (nideshchitrakar@bennington.edu)
    Date: 11/28/2017
"""

from flask import Flask, request, jsonify
from database_manager import DatabaseManager
from threading import Thread
import random
from pprint import pprint

app = Flask(__name__)
n = 5           # num of links in one chunk
c_id = 0        # chunk id starts at 0 and increases incrementally
host = 'http://0.0.0.0:5000'
wd_n = 5        # num of components monitored by one watchdog
chunk_number = 5        # num of chunks to be sent to the index builder
is_row_num = 3      # total number of index server rows

db_manager = DatabaseManager()  # manages db

link_relation = db_manager.get_relation('link')
host_relation = db_manager.get_relation('host')
chunk_relation = db_manager.get_relation('chunk')
crawler_relation = db_manager.get_relation('crawler')
index_builder_relation = db_manager.get_relation('index_builder')
index_server_relation = db_manager.get_relation('index_server')

# temp chunk id function
def generate_chunk_id():
    """
        Generates chunk id. Right now it is an integer that starts at 0 and increases
        by one.
        :return: chunk id as integer
    """
    c_id += 1
    return str(c_id) + 'c'

def distribute_index_servers():
    index_servers = db_manager.get_index_servers_from_host()
    num_index_servers = len(index_servers)      # num of index servers in the system
    num_cols = int(num_index_servers / is_row_num)
    row_count = 1
    rows = []
    k = 0  # index in index_servers array
    while num_index_servers > 0:
        for i in range(0, is_row_num):
            servers_in_row = []
            for j in range(0, num_cols):
                servers_in_row.append(index_servers[k]['host'])
                k += 1
                num_index_servers -= 1
            rows.append({'current_index':0, 'row_num':row_count, 'row':servers_in_row})
            row_count += 1
        for i in range(0, num_index_servers):
            rows[i]['row'].append(index_servers[k]['host'])
            k += 1
            num_index_servers -= 1
    return rows

rows = distribute_index_servers()

def assign_index_chunk(chunk_id):
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

# call this endpoint to add seed urls to the queue
@app.route("/add_links", methods=['POST'])
def add_links_to_queue():
    """
        Adds links from an array that is sent to the endpoint to the queue.
    """
    links_from_crawler = request.get_json()
    for link in links_from_crawler['links']:
        db_manager.operate_on_link_relation('INSERT',url=link)


# call this endpoint to get n seed urls from the queue
# returns json with a chunk id and set of n links
@app.route("/get_links", methods=['GET'])
def get_links_from_queue():
    """
        Creates an array of seed urls from the queue and retuns them along with the
        chunk id of the chunk to be created.
        :return: json containing the chunk id and the collection of seeds
    """
    links =  db_manager.get_first_n_pending_links(5)
    if len(link_relation) < n:
        return jsonify(links=[])
    else:
        temp_list = []
        for link in links:
            temp_list.append(link['link'])
        return jsonify(links=temp_list)


@app.route("/get_links/<int:num>", methods=['GET'])
def get_n_links_from_queue(num):
    links =  db_manager.get_first_n_pending_links(num)
    return jsonify(links=links)


# call these endpoint to declare your states to the device manager
# manages the states for crawler, index builders, index servers, chunks, seeds
@app.route("/set_state/component", methods=['POST'])
def set_comp_state():
    """
        Sets the states for components (crawler, index builders, index servers)
    """
    message = request.get_json()
    db_manager.operate_on_host_relation('UPDATE_STATE',host=request.url,state=message['state'])


@app.route("/set_state/seed", methods=['POST'])
def set_seed_state():
    """
        Sets the states for seeds
    """
    message = request.get_json()
    db_manager.operate_on_link_relation('UPDATE_STATE',url=message['link'],state=message['state'])


@app.route("/set_state/content_chunk", methods=['POST'])
def set_cc_state():
    """
        Sets the states for content chunks
    """
    message = request.get_json()
    db_manager.operate_on_crawler_relation('UPDATE_TASK',chunk_id=message['chunk_id'],host=request.url,task=message['state'])


@app.route("/set_state/index_chunk", methods=['POST'])
def set_ic_state():
    """
        Sets the states for index chunks
    """
    message = request.get_json()
    db_manager.operate_on_index_builder_relation('UPDATE_TASK', chunk_id=message['chunk_id'], host=request.url,
                                           task=message['state'])
    if message['state'] == 'built':
        assign_index_chunk(message['chunk_id'])


@app.route("/set_health", methods=['POST'])
def set_health():
    """
        Sets the health status for components. Endpoint called by watchdogs
    """
    message = request.get_json()
    db_manager.operate_on_host_relation('UPDATE_HEALTH',host=message['host'],health=message['status'])


@app.route("/get_metadata/content_chunk", methods=['GET'])
def get_content_chunk():
    host = request.url
    chunks = db_manager.get_first_n_crawled_chunk_ids(chunk_number)
    temp_chunks = []
    for chunk in chunks:
        temp_dict = {}
        temp_dict['chunk_id'] = chunk['chunk_id']
        temp_dict['host'] = chunk['c_host']
        temp_chunks.append(temp_dict)
    return jsonify(temp_chunks)


@app.route("/get_chunks", methods=['GET'])
def get_index_chunks():
    return 0


@app.route("/get_map", methods=['GET'])
def get_map():
    results = db_manager.get_all_relations_for_all_chunks()
    return jsonify(results)



if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # print(distribute_index_servers())
    # pprint(rows)
    # pprint(chunk_relation)
    # pprint(index_server_relation)
    for chunk in chunk_relation:
        chunk_id = chunk['id']
        assign_index_chunk(chunk_id)
    pprint(rows)

    # pprint(get_map)