#!/usr/bin/env python3
"""
    desc: Include these endpoints in the crawler server so other teams can access content chunk files of crawler machines.
          To read content off chunk file, use the chunk_reader module.
"""

from flask import Flask, jsonify, send_from_directory
from chunk_reader import read_chunk

app = Flask(__name__)
UPLOAD_FOLDER = '/data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/get_chunks', methods=['GET'])
def get_chunks():
    chunks = read_chunk.get_chunks()
    resp = {'chunks': chunks}
    return jsonify(resp)

@app.route('/get_chunk/<chunk_id>', methods=['GET'])
def get_chunk(chunk_id):
    return send_from_directory(app.config['UPLOAD_FOLDER'], chunk_id)
