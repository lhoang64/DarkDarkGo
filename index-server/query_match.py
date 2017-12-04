#!/usr/bin/env python3
# encoding utf-8

"""
    query_match.py - Matches the query against the saved indexed chunks and returns a list of dictionaries with docID
    author: Nayeem Aquib
    email: nayeemaquib@bennington.edu
    date: 12/1/2017

"""

from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from chunk_data import indexed_chunk_list


def clean_text(dirty_text):
    regex_pattern = r"[\w']+"
    tokenizer = RegexpTokenizer(regex_pattern)
    stemmer = PorterStemmer()
    tokens = tokenizer.tokenize(dirty_text)
    return tokens


def main(query):
    # sample returned query
    # dirty_query = {'id': 1,
    #          'text': 'within this set'}

    dirty_text = query['text']
    clean_query_tokens = clean_text(dirty_text)

    # sample returned indexed chunk
    # indexed_chunk_list = [{'doc_ID': ['12-abc1', '14-abc1'], 'word': 'within', 'word_count': 3},
    #                  {'doc_ID': ['13-abc1'], 'word': 'struck', 'word_count': 4},
    #                  {'doc_ID': ['11-abc1'], 'word': 'set', 'word_count': 3}]

    query_doc_list = [dict for dict in indexed_chunk_list for token in clean_query_tokens if dict["word"] == token]
    # This list will return [{'doc_ID': ['12-abc1', '14-abc1'], 'word': 'within', 'word_count': 3}, {'doc_ID': ['11-abc1'], 'word': 'set', 'word_count': 3}]

    return query_doc_list

if __name__ == "__main__":
    # query = get from front end
    # main(query)
    pass