#!/usr/bin/env python3

"""
    idx_server.py -
    author: Nayeem Aquib
    email: nayeemaquib@bennington.edu
    date: 12/1/2017

"""

import time
import schedule
import requests
from flask import Flask, jsonify, request
from threading import Thread

from query_processing import query_main
from indexed_chunks import snippet_builder

app = Flask(__name__)

s = requests.Session()

mgmt_ip_addr = '54.159.82.218'
index_builder_ip_addr = '54.174.171.194'
crawler_ip_addr = '52.90.210.211'

# For test
@app.route('/', methods=['GET'])
def hello_world():
    return jsonify(message="Hello World!")

# For management
online = s.post('http://{0}:5000/set_state/component'.format(mgmt_ip_addr), json={"state": "online"})
print(online.json())

@app.route('/get_health', methods=['GET'])
def is_healthy():
    return jsonify(status = "healthy")

# From Management and Index-builder
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

def get_chunks():
    chunk_metadata = s.get('http://{0}:5000/get_chunks'.format(mgmt_ip_addr))  # list of dicts
    print(chunk_metadata)
    crawler_host_dict = {}
    ib_host_dict = {}
    indexed_chunk = []
    content_chunk = []

    for item in chunk_metadata:
        crawler_host_dict[item['chunk_id']] = item['hosts']['c_host']
        ib_host_dict[item['chunk_id']] = item['hosts']['ib_host']

    for k, v in ib_host_dict.items():
        indexed_chunk.append(s.get('{1}/indexed_chunk/{0}'.format(k, v)))
        content_chunk.append(s.get('{1}/content_chunk/{0}'.format(k, v)))

    return (indexed_chunk, content_chunk)


# For front-end
@app.route('/getdocids/search', methods=['GET'])
def get_query():
    q = request.args.get('q')
    dict_of_ids_with_ranks = query_main(q)
    return jsonify(dict_of_ids_with_ranks)

@app.route('/get_snippet', methods=['GET'])
def get_snippet():
    id_ = request.args.get('id')
    snippets = snippet_builder(id_)
    return jsonify(snippets)


if __name__ == '__main__':
    schedule.every(10).seconds.do(get_chunks)
    t = Thread(target=run_schedule())
    t.start()
    app.run(debug = True, port = 5000)

