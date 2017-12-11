#!/usr/bin/env python3
"""
    testing.py - Automated test tool for REST endpoints
    Author: Dung Le (dungle@bennington.edu)
    Date: 12/02/2017
"""

import requests
import json
import time
from index_builder_final import Index_Builder
from read_chunk import get_chunk

# REMINDER: Change this mgmt IP address once Mgmt is set up
mgmt_ip_addr = '54.159.82.218'

# Test Endpoint 1: Update online status to Mgmt
online = requests.post('http://{0}:5000/set_state/component'.format(mgmt_ip_addr), json={"state": "online"})
print(online.json())

while True:
    # Test Endpoint 2: Get content chunk metadata from Mgmt
    metadata = requests.get('http://{0}:5000/get_metadata/content_chunk'.format(mgmt_ip_addr))
    #print(metadata.json())

    chunk_ids = []
    crawler_ip_addrs = []
    try:
        for item in metadata.json():
            chunk_id = item['chunk_id']
            chunk_ids.append(chunk_id)

        for item in metadata.json():
            host = item['host']
            crawler_ip_addrs.append(host)
    except json.decoder.JSONDecodeError:
        time.sleep(5)
        continue

    # print(chunk_ids)
    # print(crawler_ip_addrs)

    # Test Endpoint 3: Get content chunk from Crawler
    for i in range(len(chunk_ids)):
        id_ = chunk_ids[i]
        content_data = requests.get('http://{0}:5000/get_chunk/{1}'.format(crawler_ip_addrs[i], id_), stream=True)
        # print(content_data.json())

        # Save the content chunk from Crawler into local json files
        # (Not very confident whether this is needed)
        with open('sample_files/content_files/{0}'.format(id_), 'wb') as content_file:
            content_file.write(content_data.content)
        content_file.close()

        # Call function get_chunk from read_chunk.py to get a dictionary
        # that contains 'doc_id', 'link', 'title' and 'html' for 5 documents.
        content_chunk = get_chunk(id_)
        
        # Call class Index_Builder to build index chunk
        indexer = Index_Builder(id_, content_chunk)
        indexer.run()

        # Test Endpoint 4: Update status of index chunk to Mgmt
        data = {"chunk_id": id_, "state": "built"}
        index_chunk_metadata = requests.post('http://{0}:5000/set_state/index_chunk'.format(mgmt_ip_addr), json=data)
        # print(index_chunk_metadata.json())
