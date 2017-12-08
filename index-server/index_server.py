#!/usr/bin/env python3
# encoding utf-8

"""
    index_server.py -
    author: Nayeem Aquib
    email: nayeemaquib@bennington.edu
    date: 12/1/2017

"""

import requests
from flask import Flask, jsonify, request
from query_match import query_main

app = Flask(__name__)
s = requests.Session()

# REMINDER: Change this mgmt IP address once Mgmt is set up
mgmt_ip_addr = '172.10.10.18'

# For management
s.post('http://{0}:5000/set_state/component'.format(mgmt_ip_addr), json={"state": "online"})

@app.route('/get_health_status', methods=['GET'])
def is_healthy():
    return True


# For front-end
@app.route('/get_query/search?<string:querystring>', methods=['GET'])
def get_query(querystring):
    dict_of_ids = query_main(querystring)
    return dict_of_ids

@app.route('/get_snippet', methods=['POST'])
def get_snippet():
    pass # [{doc_id: ‘___’, title: ‘____’, url: ‘____’, text_snippet: ‘____’}...]



