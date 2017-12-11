#!/usr/bin/env python3

"""
    query_processing.py - Matches the query against the saved indexed chunks and returns a list of dictionaries with docID
    author: Nayeem Aquib
    email: nayeemaquib@bennington.edu
    date: 12/1/2017

"""

from nltk.tokenize import RegexpTokenizer
from indexed_chunks import sample_indexed_chunks_dict
from ranker import term_frequency_weighting
from ranker import inverse_document_frequency_weighting
from indexed_chunks import N
import itertools


def clean_text(dirty_text):
    lower_dirty_text = dirty_text.lower()
    regex_pattern = r"[\w']+"
    tokenizer = RegexpTokenizer(regex_pattern)
    tokens = tokenizer.tokenize(lower_dirty_text)
    unique_tokens = list(set(tokens))
    return unique_tokens


def query_match(tokens_list):
    d = {}
    for token in tokens_list:
        if token in sample_indexed_chunks_dict.keys():
            d[token] = sample_indexed_chunks_dict[token]
    return d

def term_frequency(tokens, dict_of_ids):
    d_tf = {}
    for token in tokens:
        d_tf[token] = {}
        for key in dict_of_ids[token]['doc_ID']:
            if key in d_tf:
                d_tf[token][key] += term_frequency_weighting(len(dict_of_ids[token]['doc_ID'][key]))
            else:
                d_tf[token][key] = term_frequency_weighting(len(dict_of_ids[token]['doc_ID'][key]))
    return d_tf


def inverse_document_frequency(tokens, dict_of_ids):
    d_idf = {}
    for token in tokens:
        for key in dict_of_ids[token]['doc_ID']:
            d_idf[token] = inverse_document_frequency_weighting(N, len(dict_of_ids[token]['doc_ID']))
    return d_idf

def tf_idf_weighting(d_idf, d_tf):
    new_dict = {a: {c: d * d_idf[a] for c, d in b.items()} for a, b in d_tf.items()}
    new_s = list(itertools.chain(*[b.items() for a, b in new_dict.items()]))
    d_tfidf = {a: sum(i[-1] for i in b) for a, b in
                  itertools.groupby(sorted(new_s, key=lambda x: x[0]), key=lambda x: x[0])}
    rank = {rank: key for rank, key in enumerate(sorted(d_tfidf, key=d_tfidf.get, reverse=True), 1)}
    return rank

def query_main(query):
    tokens_list = clean_text(query)
    dict_of_ids = query_match(tokens_list)
    dict_term_frequency = term_frequency(tokens_list, dict_of_ids)
    dict_inverse_document_frequency = inverse_document_frequency(tokens_list, dict_of_ids)
    tfidf_values = tf_idf_weighting(dict_inverse_document_frequency, dict_term_frequency)

    return tfidf_values

if __name__ == "__main__":
    a = query_main("American artist accomplishments")
    print(a)