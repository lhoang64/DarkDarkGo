#!/usr/bin/env python3

"""
	seed_queue_test.py - Test Seed Queue
	Author:
	    - Nidesh Chitrakar (nideshchitrakar@bennington.edu)
	    - Hoanh An (hoanhan@bennington.edu)
	Date: 11/24/2017
"""

import requests

if __name__ == '__main__':
    IP = '10.2.18.65'
    port = 5000

    test_json1 = {
       "links":[
          "http://bing1.com/nec/sem.js",
          "http://bing2.com/nec/sem.js",
          "http://bing3.com/nec/sem.js",
          "http://bing4.com/nec/sem.js",
          "http://bing5.com/nec/sem.js",
          "http://bing6.com/nec/sem.js",
          "http://bing7.com/nec/sem.js",
          "http://bing8.com/nec/sem.js",
          "http://bing9.com/nec/sem.js",
          "http://bing10.com/nec/sem.js",
       ]
    }

    r1 = requests.post('http://{0}:{1}/add_links'.format(IP, port), json=test_json1)
    print(">> POST {0} RETURN".format(test_json1))

    r2 = requests.get('http://{0}:{1}/get_links'.format(IP, port))
    print(">> RETURN {0}".format(r2.text))