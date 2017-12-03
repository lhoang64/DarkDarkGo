#!/usr/bin/env python3
"""
    mgmt_server.py - Management server for testing
    Author: Dung Le (dungle@bennington.edu)
    Date: 12/02/2017
"""

from flask import Flask, request, jsonify
import json

app = Flask(__name__)

'''
    /set_component_state: allow index builder to report its state
    when waking up 
'''
@app.route('/set_component_state', methods=['POST'])
def is_index_builder_online():
    online = request.get_json()
    return jsonify(online)

'''
    /get_content_chunk_metadata: allow index builder to get the content
    chunk metadata
'''
@app.route('/get_content_chunk_metadata', methods=['GET'])
def add_chunk_metadata():
    meta_json = open('chunk_metadata.json', 'r').read()
    metadata = json.loads(meta_json)
    return jsonify(metadata)

'''
    /set_index_chunk_metadata: allow index builder to update state of chunk
    when it is done with indexing
'''
@app.route('/set_index_chunk_metadata', methods=['POST'])
def indexed_chunk_status():
    index_chunk_metadata = request.get_json()
    return jsonify(index_chunk_metadata)
