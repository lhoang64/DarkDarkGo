#!/usr/bin/env python3
# encoding utf-8

"""
    index_server.py -
    author: Nayeem Aquib
    email: nayeemaquib@bennington.edu
    date: 12/1/2017

"""

from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# For management
@app.route('/set_component_state', methods=['POST'])
def index_server_online():
    online = request.get_json()
    return jsonify(online)

# From management
@app.route('/get_index_chunk_metadata', methods=['GET'])
def add_chunk_metadata():
    meta_json = open('chunk_metadata.json', 'r').read()
    metadata = json.loads(meta_json)
    return jsonify(metadata)

# From Index Builder
@app.route('/get_index_chunk_content', methods=['GET'])
def get_index_chunk_content():
    content_json = open('chunk_content.json', 'r').read()
    content = json.loads(content_json)
    return jsonify(content)

# API for front-end
@app.route('/get_query/search?<string:querystring>', methods=['GET'])
def get_query(querystring):
    return str(querystring)

@app.route('/get_snippet', methods=['POST'])
def get_snippet():
    pass # [{doc_id: ‘___’, title: ‘____’, url: ‘____’, text_snippet: ‘____’}...]



