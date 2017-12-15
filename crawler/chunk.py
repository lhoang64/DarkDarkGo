#!/usr/bin/env python3
"""
    desc: Chunk class, defines how to create and write data to a chunk
          Chunks are binary files. The last 20 bytes of a chunk is the header that can be used to seek to specific
          documents in the chunk.
"""
import os
import logging

class Chunk:
    def __init__(self, chunk_id):
        self.chunk_id = chunk_id
        self.header = []
        self.path = '/data/{0}'.format(chunk_id)  # './{}'.format(chunk_id)
        self.documents = []
        self.log = logging.getLogger()

    def create_chunk(self):
        """
        Given a chunk_id, create a new chunk file
        :return: none
        """
        new_chunk = open(self.path, 'wb')
        new_chunk.close()

    def append_to_chunk(self):
        """
        Append documents to chunk, data appended includes document_header and crawler data.
        :return: none
        """
        if os.path.exists(self.path):
            with open(self.path, 'ab') as f:
                for document in self.documents:
                    for value in document['doc_header']:
                        f.write(value)
                    f.write(document['doc_data'])
        else:
            raise Exception('Chunk does not exist')

    def create_document(self, link, title, html):
        """
        Create document, append document to list for to be writen to chunk one all docs have been created.
        :param link: string
        :param title: string
        :param html: string
        :return: list of documents
        """
        data = link + title + html
        bin_data = data.encode('utf-8')
        doc_header = self.__compute_doc_header(link, title, html)
        document = {'doc_header': doc_header, 'doc_data': bin_data}
        #if len(self.documents) < 5:
        self.documents.append(document)
        #else:
            # TODO: Move extra documents to new chunk
            # for now if crawler tries to add too many documents to a chunk an exception is raised
            #raise Exception('Max document count exceeded for chunk {}. Cannot append ')
        return self.documents

    def append_header_to_chunk(self):
        """
        Called when all documents have been writen to chunk, appends header to end of chunk.
        Header is fixed length(20 bytes), every 4 bytes represents a document.
        Reading from left to right the documents go from 0 to 4.
        :return: none
        """
        if len(self.header):
            with open(self.path, 'ab') as f:
                for header_value in self.header:
                    f.write(header_value[0])    # append document_int_value
                    f.write(header_value[1])    # append document start offset
        else:
            raise Exception('Cannot append empty header to chunk.')

    def compute_file_header_value(self, doc_int_value):
        """
        Calculates the documents start offset. Document start = length of all content prior to document
        :param doc_int_value: 0-4 int value
        :return: list contain byte objects
        """
        file_size = 0
        for document in self.documents:
            file_size += 14 + len(document['doc_data'])
        doc_start_offset = file_size.to_bytes(3, byteorder='big')
        bin_doc_int = doc_int_value.to_bytes(1, byteorder='big')
        header_val = [bin_doc_int, doc_start_offset]
        self.header.append(header_val)
        return self.header

    def __compute_doc_header(self, link, title, html):
        """
        Calculates the document header, document header is a 14 byte long value that means:
        doc_length(2 bytes), doc_start_offset(2 bytes), link_start(2 bytes), link_length(1 byte), title_start(2 bytes),
        title_length(1 byte), html_start(2 bytes), html_length(2_bytes)
        :param link: string
        :param title: string
        :param html: string
        :return: array of byte objects
        """
        file_size = 0
        for document in self.documents:
            file_size += 14 + len(document['doc_data'])

        doc_header_length = 14
        doc_length = len(link) + len(title) + len(html)
        doc_start = doc_header_length + file_size
        link_start = doc_header_length
        title_start = doc_header_length + len(link)
        html_start = doc_header_length + len(link) + len(title)
        try:
            bin_doc_length = doc_length.to_bytes(2, byteorder='big')
            bin_doc_start = doc_start.to_bytes(2, byteorder='big')
            bin_link_start = link_start.to_bytes(2, byteorder='big')
            bin_link_len = len(link).to_bytes(1, byteorder='big')
            bin_title_start = title_start.to_bytes(2, byteorder='big')
            bin_title_len = len(title).to_bytes(1, byteorder='big')
            bin_html_start = html_start.to_bytes(2, byteorder='big')
            bin_html_len = len(html).to_bytes(2, byteorder='big')
            doc_header = [bin_doc_length, bin_doc_start, bin_link_start, bin_link_len, bin_title_start, bin_title_len,
                          bin_html_start, bin_html_len]
            return doc_header
        except OverflowError as e:
            self.log.debug(e)
            self.log.debug('doc_length = {0}, link_length = {1}, title_length = {2}, html_length = {3}'.format(
                doc_length, len(link), len(title), len(html)
            ))

