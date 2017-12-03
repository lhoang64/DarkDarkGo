#!/usr/bin/env python3
"""
    crawler_server.py - Crawler server for testing
    Author: Dung Le (dungle@bennington.edu)
    Date: 12/02/2017
"""

from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/get_chunk/<string:chunk_id>', methods=['GET'])
def get_chunk(chunk_id):
    file_name = chunk_id + '.json'
    content_json = open(file_name, 'r').read()
    content_chunk = json.loads(content_json)
    return jsonify(content_chunk)
