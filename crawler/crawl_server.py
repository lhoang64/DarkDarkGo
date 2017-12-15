#!/usr/bin/env python3
"""
    This is what holds the crawlign module together. It creates the crawler,
        runs it, and listens for messages from management.

    Nov, 28, 2017 - Matt Jones matthewjones@bennington.edu
"""
import argparse
import logging
from _thread import start_new_thread
from os import environ

from flask import Flask, jsonify, send_from_directory

from crawler import Crawler
from util.util import Host
from chunk_reader import read_chunk

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', type=int, required=True)
parser.add_argument('-t', '--threads', type=int, required=True)
parser.add_argument('-u', '--user-agent', required=True)
parser.add_argument('--queue-host', required=True)
parser.add_argument('--queue-port', type=int, required=True)
parser.add_argument('--mgmt-host', required=True)
parser.add_argument('--mgmt-port', type=int, required=True)
args = parser.parse_args()

queue = Host(args.queue_host, args.queue_port)
management = Host(args.mgmt_host, args.mgmt_port)

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

crawler = Crawler(
        args.threads,
        args.user_agent,
        queue,
        management
        )

start_new_thread(crawler.run, ())

app = Flask(__name__)

UPLOAD_FOLDER = '/data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

'''
@app.route('/get_chunks')
def get_chunks():
    return jsonify(crawler.get_chunks())

@app.route('/get_chunk')
def get_chunk():
    # TODO We're going to have to wait until I can familiarize myself
    #    with the chunk API before doign this.
    id = request.args.get('chunk_id', type=int)
    pass
'''

@app.route('/is_crawling')
def is_crawling():
    return jsonify(crawler.running.is_set())

@app.route('/get_health')
def get_health():
    if crawler.running.is_set():
        resp = {'status': 'healthy'}
        return jsonify(resp)
    else:
        resp = {'status': 'failure'}
        return jsonify(resp)
    
@app.route('/crawl', methods=['POST'])
def crawl():
    crawler.running.set()

@app.route('/stop', methods=['POST'])
def stop():
    crawler.running.clear()

@app.route('/get_chunks', methods=['GET'])
def get_chunks():
    """
    Returns a JSON representation of the chunks stored on the crawler.
    """
    chunks = read_chunk.get_chunks()
    resp = {'chunks': chunks}
    return jsonify(resp)

@app.route('/get_chunk/<chunk_id>', methods=['GET'])
def get_chunk(chunk_id):
    """
    Returns a chunk file corresponding to the requested chunk id.
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], chunk_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=args.port)
