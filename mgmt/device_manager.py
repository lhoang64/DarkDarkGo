#! /usr/bin/env python3
"""
    device_manager.py - a central management system for the search engine
    Author: mgmt
    Date: 11/28/2017
"""

from flask import Flask, request, jsonify
from queue import Queue

app = Flask(__name__)
q = Queue()     # queue stores seed urls
n = 10          # num of links in a chunk
c_id = 0        # chunk id starts at 0 and increases incrementally

# a temp starting set of links
links = ["https://vinaora.com/at/vulputate/vitae/nisl/aenean/lectus/pellentesque.js",
        "https://google.fr/massa.js",
        "http://bing.com/nec/sem.js"]

# insert these temp links to the queue
def insert_from_array(q, linksArray):
    for link in linksArray:
        q.put(link)
insert_from_array(q, links)

# call this endpoint to add seed urls to the queue
@app.route("/add_links", methods=['POST'])
def add_links_to_queue():
    """
        Adds links from an array that is sent to the endpoint to the queue.
    """
    links_from_crawler = request.get_json()
    for link in links_from_crawler['links']:
        if link not in q:
            q.put(link)

# call this endpoint to get n seed urls from the queue
# returns json with a chunk id and set of n links
@app.route("/get_links", methods=['GET'])
def get_links_from_queue():
    """
        Creates an array of seed urls from the queue and retuns them along with the
        chunk id of the chunk to be created.
        :return: json containing the chunk id and the collection of seeds
    """
    temp_links = {}
    if q.qsize() <= n:
        # throws exception code 01 when queue doesn't have enough seed urls
        temp_links = {'exception': 01}
        return jsonify(temp_links)
    else:
        temp_links['c_id'] = generate_chunk_id()
        temp_links['links'] = []
        for i in range(0,n):
            temp_links['links'].append(q.get())
        print(temp_links)
        return jsonify(temp_links)


# temporary storage for state data. will connect a db to them in the future
comp_states = {}    # dictionary to store the location and states for components
seed_states = {}    # dictionary to store states for seeds
cc_states = {}      # dictionary to store the location and states for content chunks
ic_states = {}      # dictionary to store the location and states for index chunks

# call these endpoint to declare your states to the device manager
# manages the states for crawler, index builders, index servers, chunks, seeds
@app.route("/set_state/comp/", methods=['POST'])
def set_comp_state():
    """
        Sets the states for components (crawler, index builders, index servers)
    """
    message = request.get_json()
    comp_states['host'] = request.url
    comp_states['type'] = message['type']
    comp_states['state'] = message['state']

@app.route("/set_state/seed/", methods=['POST'])
def set_seed_state():
    """
        Sets the states for seeds
    """
    message = request.get_json()
    seed_states['host'] = request.url
    seed_states['state'] = message['state']

@app.route("/set_state/cc/", methods=['POST'])
def set_cc_state():
    """
        Sets the states for content chunks
    """
    message = request.get_json()
    cc_states['host'] = request.url
    cc_states['state'] = message['state']

@app.route("/set_state/ic/", methods=['POST'])
def set_ic_state():
    """
        Sets the states for index chunks
    """
    message = request.get_json()
    ic_states['host'] = request.url
    ic_states['state'] = message['state']

@app.route("/set_health", methods=['POST'])
def set_ic_state():
    """
        Sets the health status for components. Endpoint called by watchdogs
    """
    message = request.get_json()
    comp_states['health'] = message['health']

# temp chunk id function
def generate_chunk_id():
    """
        Generates chunk id. Right now it is an integer that starts at 0 and increases
        by one.
        :return: chunk id as integer
    """
    return c_id + 1


if __name__ == '__main__':
    app.run(host='0.0.0.0')
