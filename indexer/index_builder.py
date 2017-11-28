#!/usr/bin/env python3
"""
    index_builder.py - Index Builder for Web Search Engine
    Author: Dung Le (dungle@bennington.edu)
    Date: 11/25/2017
"""

import json
import nltk
import bs4
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

word_lists = []
indexed_words = []
entries = []
urls = []
stop_words = set(stopwords.words('english'))
stop_words.update('.', '?', '-', '\'', '\:', ';', ',', '!', '<', '>', '%', '$', '\"', '/', '(', ')', '[', ']', '|', 
                  '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 's', 't', 're', 'm', 'c', 'b', '”', '“', '’')

with open('chunk_1.json', encoding='utf-8') as data_file:
    chunk_data = json.load(data_file)

    chunk_id = chunk_data["chunk_id"]

    for entry in chunk_data["entries"]:
        # A dictionary of entry_id and url entries
        entry_url = {}
        entry_url["entry_id"] = entry["entry_id"]
        entry_url["url"] = entry["url"]
        urls.append(entry_url)

        # Strip all html tags
        html_doc = entry["raw_data"]
        soup = BeautifulSoup(html_doc, 'html.parser')
        content = soup.get_text()

        # All the text for one entry in the chunk
        all_text = entry["title"] + ' ' + content
        all_words_in_one_entry = nltk.word_tokenize(all_text.lower())
        unique_words_in_one_entry = set(all_words_in_one_entry)
        all_unique_words_in_one_entry = list(unique_words_in_one_entry)

        # Array containing tuples of word + entry_id
        entry_array = []
        for word in all_unique_words_in_one_entry:
            word_tuple = (word, entry["entry_id"])
            entry_array.append(word_tuple)

        entries += entry_array

        word_lists += all_words_in_one_entry

    # Remove all the stopwords
    # print(entries[:500])
    unique_words = set(word_lists)
    unique_words = unique_words.difference(stop_words)
    word_counts = nltk.FreqDist(word_lists)

    # Only choose words with frequency count >= 3
    '''
    for word in unique_words:
        if word_counts[word] >= 3:
            indexed_words.append((word, word_counts[word]))
    '''
    for word in unique_words:
        indexed_word = {}
        entry_ids = []
        if word_counts[word] >= 3:
            indexed_word['word'] = word
            indexed_word['chunk_ID'] = chunk_id
            indexed_word['word_count'] = word_counts[word]

            for tup in entries:
                if word == tup[0]:
                    entry_ids.append(tup[1])
                    indexed_word['entry_ID'] = entry_ids

        if indexed_word:
            indexed_words.append(indexed_word)

print(len(indexed_words))
print(indexed_words[:10])

with open('indexed_chunk_1.json', 'w') as file:
    json.dump(indexed_words, file)

with open('urls_chunk_1.json', 'w') as url_file:
    json.dump(urls, url_file)
