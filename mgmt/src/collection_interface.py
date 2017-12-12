#! /usr/bin/env python3
"""
    collection_interface.py - Collect stats in database and display it on a webpage
    Author:
        - Hoanh An (hoanhan@bennington.edu)
    Date: 12/3/2017
"""

from database_manager import DatabaseManager
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

db_manager = DatabaseManager()

@app.route('/', methods=['GET'])
def get_overview():
    results = db_manager.get_all_relations_for_all_chunks()
    return render_template('overview.html', data=results)

if __name__ == '__main__':
    app.run()