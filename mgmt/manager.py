#!/usr/bin/env python3
"""
        manager.py - Manager manages Watchdog and Collection Service.
        Author:
            - Hoanh An (hoanhan@bennington.edu)
            - Nidesh Chitrakar (nideshchitrakar@bennington.edu)
        Date: 11/25/2017
"""

from flask import Flask
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/get_link')
def get_link():
    return True

@app.route('/get_links?n')
def get_links():
    return True

@app.route('/add_link')
def add_link():
    return True

@app.route('/add_links')
def add_links():
    return True

@app.route('/add_crawled_link')
def add_crawled_link():
    return True

@app.route('/add_chunk_metadata')
def add_chunk_metadata():
    return True

@app.route('/get_content_chunk')
def get_content_chunk():
    return True

@app.route('/add_index_chunk')
def add_index_chunk():
    return True

@app.route('/add_query_stats')
def add_query_stats():
    return True

@app.route('/get_servers_map')
def get_servers_map():
    return True

if __name__ == '__main__':
    app.run()
