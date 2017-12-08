#!/usr/bin/env python3
# encoding utf-8

"""
    query_match.py - Matches the query against the saved indexed chunks and returns a list of dictionaries with docID
    author: Nayeem Aquib
    email: nayeemaquib@bennington.edu
    date: 12/1/2017

"""

from nltk.tokenize import RegexpTokenizer
from indexed_chunks import sample_indexed_chunks_dict


def clean_text(dirty_text):
    lower_dirty_text = dirty_text.lower()
    regex_pattern = r"[\w']+"
    tokenizer = RegexpTokenizer(regex_pattern)
    tokens = tokenizer.tokenize(lower_dirty_text)
    return tokens


def query_match(tokens_list):
    d = {}
    for token in tokens_list:
        if token in sample_indexed_chunks_dict.keys():
            d[token] = sample_indexed_chunks_dict[token]
    return d

def query_main(query):
    tokens_list = clean_text(query)
    dict_of_ids = query_match(tokens_list)
    return dict_of_ids

if __name__ == "__main__":
    a = clean_text("American artist accomplishments")
    b = query_match(a)
    print(b)