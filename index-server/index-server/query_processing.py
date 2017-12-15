#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    query_processing.py - Matches the query against the saved indexed chunks and returns a dictionary of {rank: "docID"}
    author: Nayeem Aquib
    email: nayeemaquib@bennington.edu
    date: 12/1/2017

"""

from nltk.tokenize import RegexpTokenizer


import itertools

from indexed_chunks import sample_indexed_chunks_dict
from ranker import term_frequency_weighting
from ranker import inverse_document_frequency_weighting
from indexed_chunks import N



def clean_text(dirty_text):
    """
        Given a string, this function tokenizes the words of that string.
        :param dirty_text: string
        :return: list
        input = "American artist accomplishments american"
        output = ['accomplishments', 'american', 'artist']
    """

    lower_dirty_text = dirty_text.lower()
    regex_pattern = r"[\w']+"
    tokenizer = RegexpTokenizer(regex_pattern)
    tokens = tokenizer.tokenize(lower_dirty_text)
    unique_tokens = list(set(tokens))
    return unique_tokens


def query_match(tokens_list):
    """
        Given a list of tokens, this function matches all the tokens with the tokens saved in the index-server
        :param tokens_list: list
        :return: dictionary
        input = ['accomplishments', 'american', 'artist']
        output = {'accomplishments': {'doc_ID': {'11-abc1': [45, 108, 456]}, 'word_count': 3}, 'american': {'doc_ID': {'11-abc1': [281, 442], '12-abc1': [808]},
                  'word_count': 3}, 'artist': {'doc_ID': {'14-abc1': [122, 580, 979]}, 'word_count': 3}}
    """

    d_qm = {}
    for token in tokens_list:
        if token in sample_indexed_chunks_dict.keys():
            d_qm[token] = sample_indexed_chunks_dict[token]
    return d_qm

def term_frequency(tokens, dict_of_ids):
    """
           Given a list of tokens and dict-of-ids this function returns a dictionary of logarithmic term frequency
           :param tokens: list
           :param dict_of_ids: dictionary
           :return: dictionary
           input = ['accomplishments', 'american', 'artist']
           input = {'accomplishments': {'doc_ID': {'11-abc1': [45, 108, 456]}, 'word_count': 3}, 'american': {'doc_ID': {'11-abc1': [281, 442], '12-abc1': [808]},
                  'word_count': 3}, 'artist': {'doc_ID': {'14-abc1': [122, 580, 979]}, 'word_count': 3}}
           output = {'accomplishments': {'11-abc1': 0.47712125471966244}, 'american': {'11-abc1': 0.3010299956639812, '12-abc1': 0.0}, 'artist': {'14-abc1': 0.47712125471966244}}
       """

    d_tf = {}
    for token in set(dict_of_ids.keys()):
        d_tf[token] = {}
        for key in dict_of_ids[token]['doc_ID']:
            if key in d_tf:
                d_tf[token][key] += term_frequency_weighting(len(dict_of_ids[token]['doc_ID'][key]))
            else:
                d_tf[token][key] = term_frequency_weighting(len(dict_of_ids[token]['doc_ID'][key]))
    return d_tf


def inverse_document_frequency(tokens, dict_of_ids):
    """
           Given a list of tokens and dict-of-ids this function returns a dictionary of logarithmic inverse document frequency
           :param tokens: list
           :param dict_of_ids: dictionary
           :return: dictionary
           input = ['accomplishments', 'american', 'artist']
           input = {'accomplishments': {'doc_ID': {'11-abc1': [45, 108, 456]}, 'word_count': 3}, 'american': {'doc_ID': {'11-abc1': [281, 442], '12-abc1': [808]},
                  'word_count': 3}, 'artist': {'doc_ID': {'14-abc1': [122, 580, 979]}, 'word_count': 3}}
           output = {'accomplishments': 3.0, 'american': 2.6989700043360187, 'artist': 3.0}
    """

    d_idf = {}
    for token in set(dict_of_ids.keys()):
        for key in dict_of_ids[token]['doc_ID']:
            d_idf[token] = inverse_document_frequency_weighting(N, len(dict_of_ids[token]['doc_ID']))
    return d_idf

def tf_idf_weighting(d_idf, d_tf):
    """
          Given two dicts(dict of tf and dict of idf), this function returns the ranks of the documents
          :param d_idf: dictionary
          :param d_tf: dictionary
          :return: dictionary of {ranks: 'doc_ID'}
          input = {'accomplishments': 3.0, 'american': 2.6989700043360187, 'artist': 3.0}
          input = {'accomplishments': {'11-abc1': 0.47712125471966244}, 'american': {'11-abc1': 0.3010299956639812, '12-abc1': 0.0}, 'artist': {'14-abc1': 0.47712125471966244}}
          output = {1: '11-abc1', 2: '14-abc1', 3: '12-abc1'}
       """

    new_dict = {a: {c: d * d_idf[a] for c, d in b.items()} for a, b in d_tf.items()}
    new_lst = list(itertools.chain(*[b.items() for a, b in new_dict.items()]))
    d_tfidf = {a: sum(i[-1] for i in b) for a, b in
               itertools.groupby(sorted(new_lst, key=lambda x: x[0]), key=lambda x: x[0])}
    ranks = {rank: key for rank, key in enumerate(sorted(d_tfidf, key=d_tfidf.get, reverse=True), 1)}
    return ranks


def query_main(query):
    tokens_list = clean_text(query)
    dict_of_ids = query_match(tokens_list)
    dict_term_frequency = term_frequency(tokens_list, dict_of_ids)
    dict_inverse_document_frequency = inverse_document_frequency(tokens_list, dict_of_ids)
    tfidf_values_ranks = tf_idf_weighting(dict_inverse_document_frequency, dict_term_frequency)
    return tfidf_values_ranks

if __name__ == "__main__":
    test_query = query_main("American artist test and what")
    print(test_query)
