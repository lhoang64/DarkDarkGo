#! /usr/bin/env python3
"""
    device_manager_server.py - a central management system for the search engine
    Author:
        - Nidesh Chitrakar (nideshchitrakar@bennington.edu)
        - Hoanh An (hoanhan@bennington.edu)
    Date: 11/28/2017
"""

from flask import Flask, request, jsonify
from mgmt.src.database_manager import DatabaseManager
from mgmt.src.utils import *
from pprint import pprint

app = Flask(__name__)

number_of_links = 5             # number of links to be sent to Crawler
number_of_chunks = 5            # number of chunks to be sent to Index Builder
number_of_components = 5        # number of components monitored by one Watchdog
number_of_rows = 3              # number of rows for Index Servers

db_manager = DatabaseManager()

"""
    Internal Endpoints
"""

@app.route('/get_relation/<string:relation_name>', methods=['GET'])
def get_relation(relation_name):
    """
    Get all records for relation.
    :param relation_name: Relation name.
    :return: List of dictionary
    """
    result = db_manager.get_relation(relation_name)
    return jsonify(result)

"""
    All Components' Endpoints
"""
@app.route("/set_state/component", methods=['POST'])
def set_component_state():
    """
    Set component state.
    :return: 201 if success, 400 if fail.
    """
    message = request.get_json()
    if message['state'] == 'online':
        db_manager.operate_on_host_relation('UPDATE_STATE', host=request.remote_addr, state='online')
        response = {'message': 'Successfully set state to online'}
        return jsonify(response), 201
    elif message['state'] == 'waiting':
        db_manager.operate_on_host_relation('UPDATE_STATE', host=request.remote_addr, state='waiting')
        response = {'message': 'Successfully set state to waiting'}
        return jsonify(response), 201
    elif message['state'] == 'error':
        db_manager.operate_on_host_relation('UPDATE_STATE', host=request.remote_addr, state='error')
        response = {'message': 'Successfully set state to error'}
        return jsonify(response), 201
    elif message['state'] == 'paused':
        db_manager.operate_on_host_relation('UPDATE_STATE', host=request.remote_addr, state='paused')
        response = {'message': 'Successfully set state to paused'}
        return jsonify(response), 201
    else:
        response = {'message': 'Fail to set state'}
        return jsonify(response), 201

"""
    Crawler's Endpoints
"""

@app.route("/get_links", methods=['GET'])
def get_links():
    """
    Get 5 pending links from the database.
    :return: JSON
    """
    # Get first n number of pending link from the database
    results = db_manager.get_first_n_pending_links(number_of_links)

    links = []
    # If there are enough link, append them to a temp list to return to Crawler.
    if len(results) == number_of_links:
        # Generate a chunk id
        chunk_id = generate_chunk_id()

        # Insert to chunk relation
        db_manager.operate_on_chunk_relation('INSERT', chunk_id=chunk_id)

        # Insert to crawler relation, default task is crawling
        db_manager.operate_on_crawler_relation('INSERT', host=request.remote_addr , chunk_id=chunk_id)

        #  Update state and chunk id of each link
        for record in results:
            link = record['link']
            links.append(link)

            # Update state as crawling
            db_manager.operate_on_link_relation('UPDATE_STATE', link=link, state='crawling')

            # Update chunk id
            db_manager.operate_on_link_relation('UPDATE_CHUNK_ID', link=link, chunk_id=chunk_id)
        return jsonify(links=links)
    else:
        return jsonify(links=[])

@app.route("/set_state/link", methods=['POST'])
def set_link_state():
    """
    Set link state.
    :return: 201 if success, a new pending link if fail.
    """
    message = request.get_json()
    if message['state'] == 'crawled':
        db_manager.operate_on_link_relation('UPDATE_STATE', message['link'], state='crawled')
        response = {'message': 'Successfully set state to crawled'}
        return jsonify(response), 201
    elif message['state'] == 'error':
        # Update state to error
        db_manager.operate_on_link_relation('UPDATE_STATE', message['link'], state='error')

        # Find the chunk id for that link
        chunk_id = db_manager.get_chunk_id_for_link(message['link'])[0]['chunk_id']

        # Get a new pending link
        new_link = db_manager.get_first_n_pending_links(1)[0]['link']

        # Update state as crawling
        db_manager.operate_on_link_relation('UPDATE_STATE', link=new_link, state='crawling')

        # Update chunk id
        db_manager.operate_on_link_relation('UPDATE_CHUNK_ID', link=new_link, chunk_id=chunk_id)

        return jsonify(link=new_link)
    else:
        response = {'message': 'Fail to set state'}
        return jsonify(response), 201

@app.route("/add_links", methods=['POST'])
def add_links():
    """
    Add links to database.
    :return: None
    """
    links = request.get_json()
    if links['links'] != []:
        for link in links['links']:
            db_manager.operate_on_link_relation('INSERT', link=link)
        response = {'message': 'Successfully add links to database'}
        return jsonify(response), 201
    else:
        response = {'message': 'There is no links to add'}
        return jsonify(response), 200

@app.route("/set_state/content_chunk", methods=['POST'])
def set_content_chunk_state():
    """
    Set content chunk state.
    :return: 201 if successful, 400 if fail.
    """
    message = request.get_json()
    if message['state'] == "crawled":
        chunk_id = message['chunk_id']

        # Get all links for that chunk id
        links = db_manager.get_links_for_chunk_id(chunk_id=chunk_id)

        # Update state of all links to crawled
        for entry in links:
            link = entry['link']
            db_manager.operate_on_link_relation('UPDATE_STATE', link=link, state='crawled')

        # Update Crawler's chunk id task to crawled
        db_manager.operate_on_crawler_relation('UPDATE_TASK', chunk_id=chunk_id, task='crawled')

        response = {'message': 'Successfully update state to crawled'}
        return jsonify(response), 201
    else:
        response = {'message': 'There is no state available'}
        return jsonify(response), 400

@app.route("/set_state/index_chunk", methods=['POST'])
def set_ic_state():
    """
        Sets the states for index chunks
    """
    message = request.get_json()
    db_manager.operate_on_index_builder_relation('UPDATE_TASK', chunk_id=message['chunk_id'], host=request.remote_addr,
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
    chunks = db_manager.get_first_n_crawled_chunk_ids(number_of_chunks)
    temp_chunks = []
    for chunk in chunks:
        temp_dict = {}
        temp_dict['chunk_id'] = chunk['chunk_id']
        temp_dict['host'] = chunk['c_host']
        temp_chunks.append(temp_dict)
    return jsonify(temp_chunks)


@app.route("/get_chunks", methods=['GET'])
def get_chunks():
    """
    return the hosts of the content and index chunks assigned to an index server
    :return: an array of dictionary of hosts
    """
    requester = request.remote_addr
    results = db_manager.get_chunk_ids_for_index_servers(requester)
    return jsonify(results)


@app.route('/get_chunks/unpropagated', methods=['GET'])
def get_unpropagated_chunks():
    """

    :return:
    """
    results = db_manager.get_first_n_built_chunk_ids(number_of_chunks)
    temp = []
    for chunk in results:
        temp.append(chunk['chunk_id'])
    return jsonify(chunks=temp)


@app.route("/get_map", methods=['GET'])
def get_map():
    index_server_relation = db_manager.get_relation('index_server')
    temp = []
    # for i in range(0,number_of_rows):
    #     temp.append([])
    # for entry in index_server_relation:
    #     if entry['row'] == 1:
    #         temp_dict = {'host': entry['is_host'], 'chunk_id': entry['chunk_ids']}
    return jsonify(temp)


if __name__ == '__main__':
    app.run()
    # distribute_index_servers()
    # print(distribute_index_servers())
    # pprint(rows)
    # pprint(chunk_relation)
    # pprint(index_server_relation)
    # for chunk in chunk_relation:
    #     chunk_id = chunk['id']
    #     assign_index_chunk(chunk_id)
    # pprint(rows)