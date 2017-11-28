#!/usr/bin/env python3

test_doc_id_0 = 0
test_link_0 = "http://temp_link0.com/"
test_title_0 = "Test Title"
test_data_0 = "<div title='buyer-name'>Carson Busses</div>" \
            "<span class='item-price'>$29.95</span>"
test_doc_id_1 = 1
test_link_1 = "http://temp_link1.com/"
test_title_1 = "Test Title1"
test_data_1 = "<div title='buyer-name'>Carson Busses</div>" \
            "<span class='item-price'>$29.95</span>"
test_doc_id_2 = 2
test_link_2 = "http://temp_link2.com/"
test_title_2 = "Test Title02"
test_data_2 = "<div title='buyer-name'>Carson Busses</div>" \
            "<span class='item-price'>$29.95</span>"

def create_chunk(chunk_id):
    '''
    Given a chunk_id, create a new chunk and write file version number to first 3 bytes of file
    :param chunk_id: string value
    :return:
    '''
    new_chunk = open(chunk_id, 'wb')
    version = b'1.0'
    new_chunk.write(version)
    new_chunk.close()

def append_to_header(chunk_id, header_value, doc_int_value):
    '''
    Given the chunk_id, h
    :param chunk_id:
    :param header_value:
    :param doc_int_value:
    :return:
    '''
    with open(chunk_id, 'rb+') as f:
        f.seek(4+(doc_int_value*4))
        f.write(header_value)

def compute_file_header_value(doc_int_value):
    '''
    Calculates the documents start offset.
    :param doc_int_value:
    :return: byte value
    '''

def append_to_chunk(chunk_id, link, title, html):
    '''
    Append crawler data to end of chunk
    :param chunk_id:
    :param link:
    :param title:
    :param html:
    :return:
    '''
    with open(chunk_id, 'ab') as f:
        data = link + title + html
        bin_data = data.encode('utf-8')
        doc_header = compute_doc_header(link, title, html)
        f.write(doc_header)
        f.write(bin_data)

def compute_doc_header(link, title, html):
    '''
    Calculates the document header
    :param link:
    :param title:
    :param html:
    :return: byte value
    '''
    header_length = 'some bytes'
    doc_length = len(link) + len(title) + len(html)
    doc_start = 0
    link_start = header_length
    title_starts = header_length + len(link)
    html_start = header_length + len(link) + len(title)
    return




