#!/usr/bin/env python3
"""
    index_builder_server.py - Index Builder for Web Search Engine
    Author: Dung Le (dungle@bennington.edu)
    Date: 12/01/2017
"""

from flask import Flask, request, jsonify
import json

app = Flask(__name__)

'''
    GET indexed chunk to Index Server
'''
@app.route('/indexed_chunk/<string:chunk_id>', methods=['GET'])
def get_indexed_chunk(chunk_id):
    file_name = '/sample_files/indexed_files/indexed_' + chunk_id + '.json'
    indexed_data = open(file_name, encoding='utf-8').read()
    indexed_chunk = json.loads(indexed_data)
    return jsonify(indexed_chunk)

    
