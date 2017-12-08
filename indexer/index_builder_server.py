#!/usr/bin/env python3
"""
    index_builder_server.py - Index Builder for Web Search Engine
    Author: Dung Le (dungle@bennington.edu)
    Date: 12/01/2017
"""

from flask import Flask, send_from_directory

app = Flask(__name__)
UPLOAD_FOLDER = 'sample_files/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

'''
    GET indexed chunk to Index Server
'''
@app.route('/indexed_chunk/<string:chunk_id>', methods=['GET'])
def get_indexed_chunk(chunk_id):
    file_path = app.config['UPLOAD_FOLDER'] + 'indexed_files/'
    return send_from_directory(file_path, chunk_id)

'''
    GET content chunk to Index Server
'''
@app.route('/content_chunk/<string:chunk_id>', methods=['GET'])
def get_content_chunk(chunk_id):
    file_path = app.config['UPLOAD_FOLDER'] + 'content_files/'
    return send_from_directory(file_path, chunk_id)

'''
    GET health status for Mgmt
'''
@app.route('/get_health', methods=['GET'])
def is_healthy():
    return True
