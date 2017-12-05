#!/usr/bin/env python3
"""
	test.py - test program for queue
	Author: Nidesh Chitrakar
"""

import requests
url = 'http://localhost:5000/get_links'

if __name__ == '__main__':
	r1 = requests.get(url)
	print(r1.text)
