#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
import os


from query_processing import query_main
from indexed_chunks import snippet_builder
from read_chunk import get_chunk

try:
    os.makedirs("content_files")
except OSError:
    if not os.path.isdir("content_files"):
        raise

app = Flask(__name__)

s = requests.Session()

mgmt_ip_addr = '54.159.82.218'
index_builder_ip_addr = '54.174.171.194'
crawler_ip_addr = '52.90.210.211'

THE_IDX = {}
content_chunk_list = []

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
    global content_chunk_list

    for item in chunk_metadata:
        crawler_host_dict[item['chunk_id']] = item['hosts']['c_host']
        ib_host_dict[item['chunk_id']] = item['hosts']['ib_host']

    print("crawler_host_dict:{0}".format(crawler_host_dict))
    print("ib_host_dict:{0}".format(ib_host_dict))

    for k, v in ib_host_dict.items():
        json_file = requests.get('http://{1}:5000/indexed_chunk/indexed_{0}.json'.format(k, v))
        THE_IDX.update(json_file.json()) # Saving to the main index as a dictionary
        print("Index recorded for chunk: {0}".format(k))

    for k, v in crawler_host_dict.items():
        content_data = requests.get('http://{1}:5000/get_chunk/{0}'.format(k, v), stream=True)
        with open("content_files/{0}".format(k), "wb") as f:
            f.write(content_data.content)
        f.close
        print("Content file created for chunk: {0}".format(k))

        content_chunk = get_chunk("content_files/{0}".format(k))
        content_chunk_list += content_chunk



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

