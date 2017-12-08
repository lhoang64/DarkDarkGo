#!/usr/bin/env python3
"""
    desc: demonstration of write functions for chunks with sample scraped data
"""
from chunk import Chunk

if __name__ == '__main__':
    link_0 = "http://samplelink00.com"
    title_0 = "Hello 0"
    html_0 = "<html>" \
             "<body><h1>Enter the main heading, usually the same as the title.</h1>" \
             "<p>Be <b>bold</b> in stating your key points. Put them in a list: </p>" \
             "</body>" \
             "</html>"

    link_1 = "https://somelink1.com"
    title_1 = "This is title 1"
    html_1 = "<html>" \
             "<head>Hello</head>" \
             "<body><h1>Enter the main heading, usually the same as the title.</h1>" \
             "<p>Be <b>bold</b> in stating your key points. Put them in a list: </p>" \
             "</body>" \
             "</html>"

    link_2 = "http://anotherlink2.net"
    title_2 = "Page 2"
    html_2 = "<html>" \
             "<head>Hello</head>" \
             "<body><h1>Enter the main heading, usually the same as the title.</h1>" \
             "<ul>" \
             "</ul>" \
             "</body>" \
             "</html>"

    link_3 = "http://link3.org"
    title_3 = "Number 3333"
    html_3 = "<html>" \
             "<head>This is the third page scraped</head>" \
             "<body><h1>Enter the main heading, usually the same as the title.</h1>" \
             "<p>Be <b>bold</b> in stating your key points. Put them in a list: </p>" \
             "</body>" \
             "</html>"

    link_4 = "http://lastdoc.com/04/chunk"
    title_4 = "Document 04"
    html_4 = "<html>" \
             "<head>This is the last document</head>" \
             "<body><h1>Enter the main heading, usually the same as the title.</h1>" \
             "<p>Be <b>bold</b> in stating your key points. Put them in a list: </p>" \
             "</body>" \
             "</html>"

    chunk_123 = Chunk('123')
    chunk_123.create_chunk()

    chunk_123.compute_file_header_value(0)
    chunk_123.append_to_chunk(link_0, title_0, html_0)

    chunk_123.compute_file_header_value(1)
    chunk_123.append_to_chunk(link_1, title_1, html_1)

    chunk_123.compute_file_header_value(2)
    chunk_123.append_to_chunk(link_2, title_2, html_2)

    chunk_123.compute_file_header_value(3)
    chunk_123.append_to_chunk(link_3, title_3, html_3)

    chunk_123.compute_file_header_value(4)
    chunk_123.append_to_chunk(link_4, title_4, html_4)

    print(chunk_123.header)
    chunk_123.append_header_to_chunk()



