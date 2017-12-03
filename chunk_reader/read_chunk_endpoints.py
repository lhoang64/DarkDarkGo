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
    resp = jsonify(chunk_content)
    return resp

@app.route('/get_document/<document_id>', methods=['GET'])
def get_document(document_in):
    # need to confirm with other teams with id format is
    chunk_id = 'some portion of document_id'
    doc_id = 'some portion of document_id'
    document = read_chunk.get_doc(chunk_id, doc_id)
    resp = jsonify(document)
    return resp

@app.route('/get_link/<document_id>', methods=['GET'])
def get_link(document_id):
    chunk_id = 'some portion of document_id'
    doc_id = 'some portion of document_id'
    link = read_chunk.get_link(chunk_id, doc_id)
    resp = jsonify(link)
    return resp

@app.route('/get_title/<document_id>', methods=['GET'])
def get_title(document_id):
    chunk_id = 'some portion of document_id'
    doc_id = 'some portion of document_id'
    title = read_chunk.get_title(chunk_id, doc_id)
    resp = jsonify(title)
    return resp

@app.route('/get_raw_html/<document_id>', methods=['GET'])
def get_raw_html(document_id):
    chunk_id = 'some portion of document_id'
    doc_id = 'some portion of document_id'
    raw_html = read_chunk.get_raw_html(chunk_id, doc_id)
    resp = jsonify(raw_html)
    return resp
