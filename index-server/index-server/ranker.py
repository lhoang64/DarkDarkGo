#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    ranker.py - Matches the query against the saved indexed chunks and returns a list of dictionaries with docID
    author: Nayeem Aquib
    email: nayeemaquib@bennington.edu
    date: 12/1/2017

"""

import math

def term_frequency_weighting(tf):
    return 1 + math.log10(tf)

def inverse_document_frequency_weighting(N, df):
    return math.log10(N/df)