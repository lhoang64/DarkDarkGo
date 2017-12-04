#!/usr/bin/env python3
"""
    desc: These endpoints are necessary to read content from chunks, machines hosting chunk files need to have these
          endpoints as well as the read_chunk.py module
"""

from flask import Flask, jsonify
from chunk_reader import read_chunk
app = Flask(__name__)

@app.route('/get_chunks', methods=['GET'])
def get_chunks():
    chunks = read_chunk.get_chunks()
    resp = {'chunks': chunks}
    return resp

@app.route('/get_chunk/<chunk_id>', methods=['GET'])
def get_chunk(chunk_id):
    chunk_content = read_chunk.get_chunk(chunk_id)
    if chunk_content:
        resp = jsonify(chunk_content)
        return resp, 200
    else:
        message = 'Chunk {} not found'.format(chunk_id)
        return message, 500


@app.route('/get_document/<document_id>', methods=['GET'])
def get_document(document_id):
    chunk_id = document_id[0:len(document_id)-1]
    doc_id = int(document_id[len(document_id)-1])
    document = read_chunk.get_doc(chunk_id, doc_id)
    if document:
        resp = jsonify(document)
        return resp, 200
    else:
        message = 'Chunk {} not found'.format(document_id)
        return message, 500

@app.route('/get_link/<document_id>', methods=['GET'])
def get_link(document_id):
    chunk_id = document_id[0:len(document_id) - 1]
    doc_id = int(document_id[len(document_id) - 1])
    link = read_chunk.get_link(chunk_id, doc_id)
    if link:
        resp = jsonify(link)
        return resp
    else:
        message = 'Chunk {} not found'.format(document_id)
        return message, 500

@app.route('/get_title/<document_id>', methods=['GET'])
def get_title(document_id):
    chunk_id = document_id[0:len(document_id) - 1]
    doc_id = int(document_id[len(document_id) - 1])
    title = read_chunk.get_title(chunk_id, doc_id)
    if title:
        resp = jsonify(title)
        return resp
    else:
        message = 'Chunk {} not found'.format(document_id)
        return message, 500

@app.route('/get_raw_html/<document_id>', methods=['GET'])
def get_raw_html(document_id):
    chunk_id = document_id[0:len(document_id) - 1]
    doc_id = int(document_id[len(document_id) - 1])
    raw_html = read_chunk.get_raw_html(chunk_id, doc_id)
    if raw_html:
        resp = jsonify(raw_html)
        return resp
    else:
        message = 'Chunk {} not found'.format(document_id)
        return message, 500
