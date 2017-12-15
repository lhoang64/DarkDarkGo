#!/usr/bin/env python3

"""
    desc: API for getting/reading information from chunks, knowing the chunk's id
"""
import os
from chunk_reader.constants import PATH

def get_chunk_header(chunk_id):
    """
    Given a chunk_id, get the header of the chunk. If chunk cannot before, return a NoneType object.
    :param chunk_id: string
    :return: dictionary or None
    chunk_map = {0: int, 1: int, 2: int, 3: int, 4: int}
    """
    path = PATH
    chunk_path = os.path.join(path, chunk_id)
    if os.path.exists(chunk_path):
        chunk_map = {}
        with open(chunk_path, 'rb') as chunk:
            chunk.seek(0, 2)
            chunk_size = chunk.tell()
            chunk.seek(chunk_size - 20)
            header = chunk.read(20)
            for i in range(0, 20, 4):
                bin_doc_id = header[i:i+1]
                bin_doc_offset = header[i+1:i+4]
                doc_id = int.from_bytes(bin_doc_id, byteorder='big')
                doc_offset = int.from_bytes(bin_doc_offset, byteorder='big')
                chunk_map[doc_id] = doc_offset
        return chunk_map
    else:
        for root, dirs, files in os.walk('/'):
            if chunk_id in files:
                chunk_map = {}
                with open(chunk_path, 'rb') as chunk:
                    chunk.seek(0, 2)
                    chunk_size = chunk.tell()
                    chunk.seek(chunk_size - 20)
                    header = chunk.read(20)
                    for i in range(0, 20, 4):
                        bin_doc_id = header[i:i + 1]
                        bin_doc_offset = header[i + 1:i + 4]
                        doc_id = int.from_bytes(bin_doc_id, byteorder='big')
                        doc_offset = int.from_bytes(bin_doc_offset, byteorder='big')
                        chunk_map[doc_id] = doc_offset
                return chunk_map
            else:
                return None

def get_document_header(chunk_map, doc_id, chunk_id):
    """
    Given a chunk_map, doc_id, get the header with is the first 14 bytes of a document.
    Return a dictionary of header values used to locate values in document.
    If chunk cannot be found, return a NoneType object.
    :param chunk_map: dictionary of doc_ids and their offsets
    :param doc_id: int
    :return: dictionary or None
    doc_map = {'doc_length': int, 'doc_offset': int, 'link_start': int, 'link_length': int, 'title_start': int,
               'title_length': int, 'html_start': int, 'html_length': int}
    """
    doc_map = {}
    path = PATH
    chunk_path = os.path.join(path, chunk_id)
    if os.path.exists(chunk_path):
        with open(chunk_path, 'rb') as chunk:
            chunk.seek(chunk_map[doc_id])
            doc_header = chunk.read(14)
            doc_length = int.from_bytes(doc_header[0:2], byteorder='big')
            doc_offset = int.from_bytes(doc_header[2:4], byteorder='big')
            link_start = int.from_bytes(doc_header[4:6], byteorder='big')
            link_length = int.from_bytes(doc_header[6:7], byteorder='big')
            title_start = int.from_bytes(doc_header[7:9], byteorder='big')
            title_length = int.from_bytes(doc_header[9:10], byteorder='big')
            html_start = int.from_bytes(doc_header[10:12], byteorder='big')
            html_length = int.from_bytes(doc_header[12:14], byteorder='big')

            doc_map['doc_length'] = doc_length
            doc_map['doc_offset'] = doc_offset
            doc_map['link_start'] = link_start
            doc_map['link_length'] = link_length
            doc_map['title_start'] = title_start
            doc_map['title_length'] = title_length
            doc_map['html_start'] = html_start
            doc_map['html_length'] = html_length
        return doc_map
    else:
        # search file system for chunk, not ideal so chunks should be stored in /data
        for root, dirs, files in os.walk('/'):
            if chunk_id in files:
                with open(os.path.join(root, chunk_id), 'rb') as chunk:
                    chunk.seek(chunk_map[doc_id])
                    doc_header = chunk.read(14)
                    doc_length = int.from_bytes(doc_header[0:2], byteorder='big')
                    doc_offset = int.from_bytes(doc_header[2:4], byteorder='big')
                    link_start = int.from_bytes(doc_header[4:6], byteorder='big')
                    link_length = int.from_bytes(doc_header[6:7], byteorder='big')
                    title_start = int.from_bytes(doc_header[7:9], byteorder='big')
                    title_length = int.from_bytes(doc_header[9:10], byteorder='big')
                    html_start = int.from_bytes(doc_header[10:12], byteorder='big')
                    html_length = int.from_bytes(doc_header[12:14], byteorder='big')

                    doc_map['doc_length'] = doc_length
                    doc_map['doc_offset'] = doc_offset
                    doc_map['link_start'] = link_start
                    doc_map['link_length'] = link_length
                    doc_map['title_start'] = title_start
                    doc_map['title_length'] = title_length
                    doc_map['html_start'] = html_start
                    doc_map['html_length'] = html_length
                return doc_map
            else:
                return None

def get_chunks():
    """
    Called on a crawler instance, crawler will then look on disk in the location that it stores its chunks and return
    a list of chunk ids it holds currently on disk.
    :return: list of ids
    """
    path = PATH
    chunks = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))] # list of all files in that directory
    return chunks

def get_chunk(chunk_id):
    """
    Given a chunk_id, return the contents of that chunk in json format
    If the chunk was not found when generating chunk_map, return None
    :param chunk_id: string
    :return: list of dictionaries, each dictionary represents a document in the chunk or None
    """
    chunk_content = []
    try:
        chunk_map = get_chunk_header(chunk_id)
        for key in chunk_map:
            doc_content = get_doc(chunk_id, key)
            chunk_content.append(doc_content)
        return chunk_content
    except TypeError:
        return None

def get_doc(chunk_id, doc_id):
    """
    Given a chunk_id and a doc_id, return the content of the document is json format.
    If the chunk was not found when generating chunk_map, return None
    :param chunk_id: string
    :param doc_id: int
    :return: dictionary or None
    """
    path = PATH
    chunk_path = os.path.join(path, chunk_id)
    chunk_map = get_chunk_header(chunk_id)
    doc_map = get_document_header(chunk_map, doc_id, chunk_id)
    doc_content = {'doc_id': doc_id}
    try:
        with open(chunk_path, 'rb') as chunk:
            chunk.seek(chunk_map[doc_id])
            chunk.seek(doc_map['doc_offset'], 0)
            bin_link = chunk.read(doc_map['link_length'])
            bin_title = chunk.read(doc_map['title_length'])
            bin_html = chunk.read(doc_map['html_length'])
            doc_content['link'] = bin_link.decode('utf-8')
            doc_content['title'] = bin_title.decode('utf-8')
            doc_content['html'] = bin_html.decode('utf-8')
        return doc_content
    except TypeError:
        return None

def get_link(chunk_id, doc_id):
    """
    Given a chunk_id and doc_id, return the link contained in the document
    If the chunk was not found when generating chunk_map, return None
    :param chunk_id: string
    :param doc_id: int
    :return: dictionary or None
    """
    path = PATH
    chunk_path = os.path.join(path, chunk_id)
    chunk_map = get_chunk_header(chunk_id)
    doc_map = get_document_header(chunk_map, doc_id, chunk_id)
    link = {}
    try:
        with open(chunk_path, 'rb') as chunk:
            chunk.seek(chunk_map[doc_id])
            chunk.seek(doc_map['link_start'], 1)
            bin_data = chunk.read(doc_map['link_length'])
            link['link'] = bin_data.decode('utf-8')
        return link
    except TypeError:
        return None

def get_title(chunk_id, doc_id):
    """
    Given a chunk_id and doc_id, return the title contained in the document
    If the chunk was not found when generating chunk_map, return None
    :param chunk_id: string
    :param doc_id: int
    :return: dictionary or None
    """
    path = PATH
    chunk_path = os.path.join(path, chunk_id)
    chunk_map = get_chunk_header(chunk_id)
    doc_map = get_document_header(chunk_map, doc_id, chunk_id)
    title = {}
    try:
        with open(chunk_path, 'rb') as chunk:
            chunk.seek(chunk_map[doc_id])
            chunk.seek(doc_map['title_start'], 1)
            bin_data = chunk.read(doc_map['title_length'])
            title['title'] = bin_data.decode('utf-8')
        return title
    except TypeError:
        return None

def get_raw_html(chunk_id, doc_id):
    """
    Given a chunk_id and doc_id, return the raw html contained in the document
    If the chunk was not found when generating chunk_map, return None
    :param chunk_id: string
    :param doc_id: int
    :return: dictionary or None
    """
    path = PATH
    chunk_path = os.path.join(path, chunk_id)
    chunk_map = get_chunk_header(chunk_id)
    doc_map = get_document_header(chunk_map, doc_id, chunk_id)
    html = {}
    try:
        with open(chunk_path, 'rb') as chunk:
            chunk.seek(chunk_map[doc_id])
            chunk.seek(doc_map['html_start'], 1)
            bin_data = chunk.read(doc_map['html_length'])
            html['html'] = bin_data.decode('utf-8')
        return html
    except TypeError:
        return None
