#!/usr/bin/env python3
"""
    index_builder_final.py - Index Builder for Web Search Engine
    Author: Dung Le (dungle@bennington.edu)
    Date: 11/30/2017
"""

import json
import nltk
import bs4
import os
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

class Index_Builder:
    def __init__(self, chunk_id, content_chunk):
        """
            num_threads: number of threads being used for indexing
                         (none for the moment)
            chunk_id: a string of chunk_id
            content_chunk: file name/directory of content chunk get from crawler
        """
        # self.num_threads = num_threads
        self.chunk_id = chunk_id
        self.content_chunk = content_chunk

    def index_builder(self, chunk_data):
        """
            Preparation includes:
                Strip all html tags from raw content of pages
                Concatenate page content and title, tokenize
                Create an array of url for each word
                Remove all stop words + get frequency of each word in the chunk 
        """
        word_lists = []
        indexed_words = {}
        entries = []
        stop_words = set(stopwords.words('english'))
        stop_words.update('.', '?', '-', '\'', '\:', ';', ',', '!', '<', '>', '%', '$', '\"', '/', '(', ')', '[', ']', '|', 
                          '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 's', 't', 're', 'm', 'c', 'b', '”', '“', '’')

        for entry in chunk_data:
            # Strip all html tags
            html_doc = entry["html"]
            soup = BeautifulSoup(html_doc, 'html.parser')
            content = soup.get_text()

            # All the text for one entry in the chunk
            all_text = entry["title"] + ' ' + content
            all_words_in_one_entry = nltk.word_tokenize(all_text.lower())
            word_count_in_entry = nltk.FreqDist(all_words_in_one_entry)
            unique_words_in_one_entry = set(all_words_in_one_entry)
            all_unique_words_in_one_entry = list(unique_words_in_one_entry)

            # Array containing tuples of word + word_count + entry_id
            entry_array = []
            for word in all_unique_words_in_one_entry:
                word_positions = []
                for pos, w in enumerate(all_words_in_one_entry):
                    if w == word:
                        word_positions.append(pos)
                word_tuple = (word, word_count_in_entry[word], entry["doc_id"], word_positions)
                entry_array.append(word_tuple)

            entries += entry_array

            word_lists += all_words_in_one_entry

        # Remove all the stopwords
        unique_words = set(word_lists)
        unique_words = unique_words.difference(stop_words)
        word_counts = nltk.FreqDist(word_lists)

        """
            Indexing includes:
                Only choose words with frequency > = 3
                Append all the urls into an array for the same word
                NOTE: list of urls for each word is already ranked by word frequency in each doc
                      (should I normalize word frequency?)
                indexed_words is a list of all words indexed, along with their corresponding
                word_count and list of urls
        """
        # Only choose words with frequency count >= 3
        for word in unique_words:
            indexed_word_info = {}
            entry_ids = []
            if word_counts[word] >= 3:
                indexed_word_info['word_count'] = word_counts[word]

                for tup in entries:
                    if word == tup[0]:
                        entry_ids.append(tup[1:])
                        # within each tuple (word_count + entry_id + word_positions),
                        # rank each document id based on the frequency of word in that document
                        doc_ids = {}
                        for en_id in sorted(entry_ids, reverse=True):
                            doc_ids[en_id[1]] = en_id[2]
                        # the value of key 'doc_ID' is now ranked
                        indexed_word_info['doc_ID'] = doc_ids

            if indexed_word_info:
                indexed_words[word] = indexed_word_info

        return indexed_words

    def run(self):
        # Start indexing
        indexed_words = self.index_builder(self.content_chunk)

        # Open new file to write indexed chunk into
        file_name = 'sample_files/indexed_files/indexed_' + self.chunk_id + '.json'
        with open(file_name, 'w') as indexed_file:
            json.dump(indexed_words, indexed_file)
        indexed_file.close()

