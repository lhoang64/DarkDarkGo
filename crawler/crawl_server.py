"""
    This is what holds the crawlign module together. It creates the crawler,
        runs it, and listens for messages from management.

    Nov, 28, 2017 - Matt Jones matthewjones@bennington.edu
"""
import argparse
from _thread import start_new_thread
from os import environ

from flask import Flask, jsonify

from crawler import Crawler
from util.util import Host

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', type=int, required=True)
parser.add_argument('-t', '--threads', type=int, required=True)
parser.add_argument('-u', '--user-agent', required=True)
parser.add_argument('--queue-host', required=True)
parser.add_argument('--queue-port', type=int, required=True)
parser.add_argument('--mgmt-host', required=True)
parser.add_argument('--mgmt-port', type=int, required=True)
args = parser.parse_args()
print(args)

#port = environ.get('LISTEN_PORT')
#thread_num = int(environ.get('CRAWLER_THREADS'))
#user_agent = environ.get('USERAGENT')
#queue_host = environ.get('QUEUE_HOST')
#queue_port = environ.get('QUEUE_PORT')
#mgmt_host = environ.get('MANAGEMENT_HOST')
#mgmt_port = environ.get('MANAGEMENT_PORT')

queue = Host(args.queue_host, args.queue_port)
management = Host(args.mgmt_host, args.mgmt_port)

crawler = Crawler(
        args.threads,
        args.user_agent,
        queue,
        management
        )

start_new_thread(crawler.run, ())

app = Flask(__name__)

app.run(port=args.port)

@app.route('/get_chunks')
def get_chunks():
    return jsonify(crawler.get_chunks())

@app.route('/get_chunk')
def get_chunk():
    # TODO We're going to have to wait until I can familiarize myself
    #    with the chunk API before doign this.
    pass

@app.route('/is_crawling')
def is_crawling():
    return jsonify(crawler.running.is_set())

@app.route('/crawl', methods=['POST'])
def crawl():
    crawler.running.set()

@app.route('/stop', methods=['POST'])
def stop():
    crawler.running.clear()
