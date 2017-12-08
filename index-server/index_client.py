#!/usr/bin/env python3
# encoding utf-8

"""
    index_server.py -
    author: Nayeem Aquib
    email: nayeemaquib@bennington.edu
    date: 12/1/2017

"""

import requests
from read_chunk import get_chunks

s = requests.Session()

# REMINDER: Change these IP addresses once they are set up
mgmt_ip_addr = '172.10.10.18'
crawler_ip_addr = '192.10.10.18'
index_builder_ip_addr = '192.10.10.19'

# From Management
with open("index_chunk_metadata.txt") as outfile:
    get_index_chunk_metadata = s.get('http://{0}:5000/get_chunks_metadata'.format(mgmt_ip_addr))  # list of dicts
#     [{
#         "chunk_id": "101c",
#         "hosts": {
#                     "c_host": "http://101.101:101:101:5000",
#                     "ib_host": "http://101.101:101:102:5000"
#                   }
#     }
# ]

    outfile.write(str(get_index_chunk_metadata))
    outfile.close()

# From Index Builder
# TODO: Both index and content chunks will be saved in the disk. Will be done after the stream is on.
# with open("index_chunk_metadata.txt") as infile:

get_indexed_chunk = s.get('http://{0}:6000/indexed_chunk/<string:chunk_id>'.format(index_builder_ip_addr))
get_content_chunk = s.get('http://{0}:7000/content_chunk/<string:chunk_id>'.format(crawler_ip_addr))

