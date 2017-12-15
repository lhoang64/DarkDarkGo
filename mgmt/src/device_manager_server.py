#! /usr/bin/env python3
"""
    device_manager_server.py - a central management system for the search engine
    Author:
        - Nidesh Chitrakar (nideshchitrakar@bennington.edu)
        - Hoanh An (hoanhan@bennington.edu)
    Date: 11/28/2017
"""

from flask import Flask, request, jsonify
from utils import *
from constants import number_of_links, \
    number_of_chunks, \
    number_of_rows

app = Flask(__name__)

# Distribute the index servers into rows on init
rows = distribute_index_servers()

"""
    Internal Endpoints
"""

@app.route('/', methods=['GET'])
def distribute_rows():
    """
    Distribute index server into rows
    :return:
    """
    global rows
    rows = distribute_index_servers()
    return jsonify(message="{0} rows have been distributed!".format(len(rows)))


@app.route('/get_relation/<string:relation_name>', methods=['GET'])
def get_relation(relation_name):
    """
    Get all records for relation
    :param relation_name: Relation name
    :return: List of dictionaries
    """
    result = db_manager.get_relation(relation_name)
    return jsonify(result)


@app.route('/add_hosts', methods=['POST'])
def add_hosts():
    """
    Add host data in host relation
    JSON format:
    [
        {
            'host': host_url,
            'type': host_type.
        }
    ]
    :return:
    """
    message = request.get_json()
    for component in message:
        db_manager.operate_on_host_relation('INSERT',
                                            host=component['host'],
                                            type=component['type'])
        global rows
        rows = distribute_index_servers()
    response = {'message': 'Successfully added hosts'}
    return jsonify(response), 201


@app.route('/clear_relation/<string:relation_name>', methods=['POST'])
def clear_db(relation_name):
    db_manager.clear_relation(relation_name=relation_name)
    response = {'message': 'Successfully cleared the relation'}
    return jsonify(response), 201


"""
    All Components' Endpoints
"""


@app.route("/set_state/component", methods=['POST'])
def set_component_state():
    """
    Set component state
    :return: 201 if success, 400 if fail
    """
    message = request.get_json()
    if message['state'] == 'online':
        db_manager.operate_on_host_relation('UPDATE_STATE',
                                            host=request.remote_addr,
                                            state='online')
        response = {'message': 'Successfully set state to online'}
        return jsonify(response), 201
    elif message['state'] == 'waiting':
        db_manager.operate_on_host_relation('UPDATE_STATE',
                                            host=request.remote_addr,
                                            state='waiting')
        response = {'message': 'Successfully set state to waiting'}
        return jsonify(response), 201
    elif message['state'] == 'error':
        db_manager.operate_on_host_relation('UPDATE_STATE',
                                            host=request.remote_addr,
                                            state='error')
        response = {'message': 'Successfully set state to error'}
        return jsonify(response), 201
    elif message['state'] == 'paused':
        db_manager.operate_on_host_relation('UPDATE_STATE',
                                            host=request.remote_addr,
                                            state='paused')
        response = {'message': 'Successfully set state to paused'}
        return jsonify(response), 201
    else:
        response = {'message': 'Failed to set state'}
        return jsonify(response), 201


"""
    Crawlers' Endpoints
"""


@app.route("/get_links", methods=['GET'])
def get_links():
    """
    Get num_of_links pending links from the database
    :return: JSON
    """
    # Get first n number of pending links from the database
    results = db_manager.get_first_n_pending_links(number_of_links)

    links = []
    # If there are enough links, append them to a temp list to return to Crawler
    if len(results) == number_of_links:
        # Generate a chunk id
        chunk_id = generate_chunk_id()

        # Insert to chunk relation
        db_manager.operate_on_chunk_relation('INSERT',
                                             chunk_id=chunk_id)

        # Insert to crawler relation, default task is 'crawling'
        db_manager.operate_on_crawler_relation('INSERT',
                                               host=request.remote_addr,
                                               chunk_id=chunk_id)

        #  Update state and chunk id of each link
        for record in results:
            link = record['link']
            links.append(link)

            # Update link state to 'crawling'
            db_manager.operate_on_link_relation('UPDATE_STATE',
                                                link=link,
                                                state='crawling')

            # Update link's chunk id
            db_manager.operate_on_link_relation('UPDATE_CHUNK_ID',
                                                link=link,
                                                chunk_id=chunk_id)
        return jsonify(chunk_id=chunk_id, links=links)
    else:
        return jsonify(links=[])


@app.route("/set_state/link", methods=['POST'])
def set_link_state():
    """
    Set link state
    :return: 201 if success, a new pending link if fail
    """
    message = request.get_json()
    if message['state'] == 'crawled':
        db_manager.operate_on_link_relation('UPDATE_STATE',
                                            message['link'],
                                            state='crawled')
        response = {'message': 'Successfully set state to crawled'}
        return jsonify(response), 201
    elif message['state'] == 'error':
        # Update state to error
        db_manager.operate_on_link_relation('UPDATE_STATE',
                                            message['link'],
                                            state='error')

        # Find the chunk id for that link
        chunk_id = db_manager.get_chunk_id_for_link(message['link'])[0]['chunk_id']

        # Get a new pending link
        new_link = db_manager.get_first_n_pending_links(1)[0]['link']

        # Update link state to 'crawling'
        db_manager.operate_on_link_relation('UPDATE_STATE',
                                            link=new_link,
                                            state='crawling')

        # Update link's chunk id
        db_manager.operate_on_link_relation('UPDATE_CHUNK_ID',
                                            link=new_link,
                                            chunk_id=chunk_id)

        return jsonify(link=new_link)
    else:
        response = {'message': 'Failed to set state'}
        return jsonify(response), 201


@app.route("/add_links", methods=['POST'])
def add_links():
    """
    Add links to database
    :return: 201 if successful, 200 if no links to add
    """
    links = request.get_json()
    if links['links']:
        for link in links['links']:
            db_manager.operate_on_link_relation('INSERT', link=link)

        response = {'message': 'Successfully added links to database'}
        return jsonify(response), 201
    else:
        response = {'message': 'There are no links to add'}
        return jsonify(response), 200


@app.route("/set_state/content_chunk", methods=['POST'])
def set_content_chunk_state():
    """
    Set content chunk state.
    :return: 201 if successful, 400 if fail
    """
    message = request.get_json()
    if message['state'] == "crawled":
        chunk_id = message['chunk_id']

        # Get all links for that chunk id
        links = db_manager.get_links_for_chunk_id(chunk_id=chunk_id)

        # Update state of all links to 'crawled'
        for entry in links:
            link = entry['link']
            db_manager.operate_on_link_relation('UPDATE_STATE',
                                                link=link,
                                                state='crawled')

        # Update Crawler's chunk id task to 'crawled'
        db_manager.operate_on_crawler_relation('UPDATE_TASK',
                                               chunk_id=chunk_id,
                                               task='crawled')

        response = {'message': 'Successfully updated state to crawled'}
        return jsonify(response), 201
    elif message['state'] == "propagated":
        chunk_id = message['chunk_id']

        # Update Crawler's chunk id task to 'propagated'
        db_manager.operate_on_crawler_relation('UPDATE_TASK',
                                               chunk_id=chunk_id,
                                               task='propagated')

        response = {'message': 'Successfully updated state to propagated'}
        return jsonify(response), 201
    else:
        response = {'message': 'There is no state available'}
        return jsonify(response), 400


@app.route('/get_chunks/unpropagated', methods=['GET'])
def get_unpropagated_chunks():
    """
    Get a list of un-propagated chunks
    :return: List of chunk ids
    """
    results = db_manager.get_first_n_built_chunk_ids(number_of_chunks)
    temp = []
    for chunk in results:
        temp.append(chunk['chunk_id'])
    return jsonify(chunks=temp)


"""
    Index Builders' and Servers' Endpoints
"""


@app.route("/set_state/index_chunk", methods=['POST'])
def set_index_chunk_state():
    """
    Set the given state for index chunk
    :return: 201 if successful, 400 if fail
    """
    message = request.get_json()
    if message['state'] == "built":
        # Update index chunk state to 'built'
        db_manager.operate_on_index_builder_relation('UPDATE_TASK',
                                                     chunk_id=message['chunk_id'],
                                                     host=request.remote_addr,
                                                     task=message['state'])

        # Assign content and index chunks to index servers after the index is built
        assign_index_chunk(rows, message['chunk_id'])

        response = {'message': 'Successfully updated state to built'}
        return jsonify(response), 201
    elif message['state'] == "propagated":
        # Update index chunk state to 'propagated'
        db_manager.operate_on_index_builder_relation('UPDATE_TASK',
                                                     chunk_id=message['chunk_id'],
                                                     task=message['state'])

        response = {'message': 'Successfully updated state to propagated'}
        return jsonify(response), 201
    else:
        response = {'message': 'There is no state available'}
        return jsonify(response), 400


@app.route("/get_metadata/content_chunk", methods=['GET'])
def get_content_chunk():
    """
    Get metadata for 5 chunks on each request
    :return: List of metadata, empty list if no content chunks
    """
    # Get the first number_of_chunks crawled chunk ids
    results = db_manager.get_first_n_crawled_chunks(number_of_chunks)

    temp_chunks = []
    if len(results) != 0:
        for chunk in results:
            temp_dict = {'chunk_id': chunk['chunk_id'],
                         'host': chunk['c_host']}
            temp_chunks.append(temp_dict)

            # Insert to index builder relation and mark chunk as 'building'
            db_manager.operate_on_index_builder_relation('INSERT',
                                                         chunk['chunk_id'],
                                                         host=request.remote_addr,
                                                         task='building')

        return jsonify(temp_chunks)
    else:
        return jsonify([])


@app.route("/get_chunks", methods=['POST'])
def get_chunks():
    """
    Get the hosts of the content and index chunks assigned to an index server
    :return: List of dictionary of hosts, empty list if no chunks assigned
    """
    # requester = request.remote_addr
    requester = request.get_json()['host']

    # Get all index servers for requester
    results = db_manager.get_chunk_hosts_for_index_servers(requester)

    return jsonify(results)


@app.route("/get_map", methods=['GET'])
def get_map():
    """
    Get a map of the index servers and chunks assigned to them
    :return: List representing a map of the index servers
    """
    # Get a list of index servers
    index_servers = db_manager.get_all_index_servers()

    temp = []
    try:
        for i in range(number_of_rows):
            temp.append([])
        for server in index_servers:
            index_server_host = server['host']

            # Get chunk ids for a given Index Server's host
            temp_dict = db_manager.get_chunk_ids_for_index_server(host=index_server_host)

            if len(temp_dict) != 0:
                index = temp_dict['row'] - 1
                temp[index].append({'host': temp_dict['host'],
                                    'chunk_ids': temp_dict['chunk_ids']})
    except Exception as e:
        temp = []
        print(e)
    return jsonify(temp)


"""
    WatchDog's Endpoints
"""


@app.route("/set_health", methods=['POST'])
def set_health():
    """
    Sets the health status for components; called by watchdogs
    :return: None
    """
    message = request.get_json()

    # Update the health status in the database
    db_manager.operate_on_host_relation('UPDATE_HEALTH',
                                        host=message['host'],
                                        health=message['status'])
    db_manager.operate_on_host_relation('UPDATE_STATE',
                                        host=message['host'],
                                        state=message['state'])
    response = {'message': 'Successfully updated health'}
    return jsonify(response), 201


@app.route("/get_health", methods=['GET'])
def get_health():
    """
    Sets the health status for components; called by watchdogs
    :return: None
    """
    response = {'status': 'healthy'}
    return jsonify(response), 201


if __name__ == '__main__':
    app.run()
