#! /usr/bin/env python3
"""
    database_manager.py - Database Manager
    Author:
        - Hoanh An (hoanhan@bennington.edu)
    Date: 12/2/2017
"""

import psycopg2
import psycopg2.extras

DATABASE = 'mgmt_db'
USER = 'postgres'
HOST = 'localhost'

class DatabaseManager():
    def get_relation(self, relation_name):
        """
        Get all records for a given relation.
        :param relation_name: Relation name
        :return: List of rows where each row is a dictionary
        """
        try:
            conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}'".format(DATABASE, USER, HOST))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("SELECT * FROM {0} ORDER BY index;".format(relation_name))
            links = cur.fetchall()
            cur.close()
            return links
        except Exception as e:
            print(e)

    def operate_on_chunk_relation(self, function, chunk_id):
        """
        Execute basic operations on chunk relation.
        - INSERT: Insert a given chunk id. Default state is None.
        - DELETE: Delete a given chunk id.
        :param function: INSERT | DELETE
        :param chunk_id: Chunk ID
        :param state: OK | Error
        :return: None
        """
        try:
            conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}'".format(DATABASE, USER, HOST))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            if function == 'INSERT':
                cur.execute("INSERT INTO chunk VALUES (DEFAULT, {0});".format(chunk_id))
            elif function == 'DELETE':
                cur.execute("DELETE FROM chunk WHERE id = {0};".format(chunk_id))
            else:
                print('NO FUNCTION FOUND')

            conn.commit()
            cur.close()
        except Exception as e:
            print(e)

    def operate_on_link_relation(self, function, link, chunk_id=None, state=None):
        """
        Execute basic operations on link relation.
        - INSERT: Insert a given link and chunk id. Default chunk id is None state is pending.
        - UPDATE_STATE: Update chunk id for a given link.
        - UPDATE_STATE: Update state for a given link.
        - DELETE: Delete a given link.
        :param function: INSERT | UPDATE_CHUNK_ID | UPDATE_STATE | DELETE
        :param link: URL
        :param state: OK | Error
        :return: None
        """
        try:
            conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}'".format(DATABASE, USER, HOST))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            if function == 'INSERT':
                cur.execute("INSERT INTO link VALUES (DEFAULT, '{0}', DEFAULT, 'pending');".format(link))
            elif function == 'UPDATE_CHUNK_ID':
                cur.execute("UPDATE link SET chunk_id = '{0}' WHERE link = '{1}';".format(chunk_id, link))
            elif function == 'UPDATE_STATE':
                cur.execute("UPDATE link SET state = '{0}' WHERE link = '{1}';".format(state, link))
            elif function == 'DELETE':
                cur.execute("DELETE FROM link WHERE link = '{0}';".format(link))
            else:
                print('NO FUNCTION FOUND')

            conn.commit()
            cur.close()
        except Exception as e:
            print(e)

    def operate_on_host_relation(self, function, host, type=None, state=None, health=None):
        """
        Execute basic operations on host relation.
        - INSERT: Insert a given host and type. Default state and health is None.
        - UPDATE_STATE: Update state for a given host.
        - UPDATE_HEALTH: Update health for a given host.
        - DELETE: Delete a given host.
        :param function: INSERT | UPDATE_STATE | UPDATE_HEALTH | DELETE
        :param host: Host
        :param type: Crawler | Index Builder | Index Server
        :param state: online | waiting | error | paused
        :param health: healthy | failure | probation
        :return: None
        """
        try:
            conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}'".format(DATABASE, USER, HOST))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            if function == 'INSERT':
                cur.execute("INSERT INTO host VALUES (DEFAULT, '{0}', '{1}');".format(host, type))
            elif function == 'UPDATE_STATE':
                cur.execute("UPDATE host SET state = '{0}' WHERE host = '{1}';".format(state, host))
            elif function == 'UPDATE_HEALTH':
                cur.execute("UPDATE host SET health = '{0}' WHERE host = '{1}';".format(health, host))
            elif function == 'DELETE':
                cur.execute("DELETE FROM host WHERE host = '{0}';".format(host))
            else:
                print('NO FUNCTION FOUND')

            conn.commit()
            cur.close()
        except Exception as e:
            print(e)

    def operate_on_crawler_relation(self, function, chunk_id, host='101.101.101.101:101', task=None):
        """
        Execute basic operations on crawler relation.
        - INSERT: Insert a given chunk_id and host. Default host is '101.101.101.101:101'. Default task is None.
        - UPDATE_TASK: Update task for a given chunk_id.
        - DELETE: Delete a given chunk_id.
        :param function: INSERT | UPDATE_TASK | DELETE
        :param chunk_id: Chunk ID
        :param host: Host
        :param task: crawling | crawled | propagated
        :return: None
        """
        try:
            conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}'".format(DATABASE, USER, HOST))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            if function == 'INSERT':
                cur.execute("INSERT INTO crawler VALUES (DEFAULT, {0}, '{1}');".format(chunk_id, host))
            elif function == 'UPDATE_TASK':
                cur.execute("UPDATE crawler SET c_task = '{0}' WHERE chunk_id = {1};".format(task, chunk_id))
            elif function == 'DELETE':
                cur.execute("DELETE FROM crawler WHERE chunk_id = {0};".format(chunk_id))
            else:
                print('NO FUNCTION FOUND')

            conn.commit()
            cur.close()
        except Exception as e:
            print(e)

    def operate_on_index_builder_relation(self, function, chunk_id, host='101.101.101.101:101', task=None):
        """
        Execute basic operations on index builder relation.
        - INSERT: Insert a given chunk_id and host. Default host is '101.101.101.101:101', default task is None.
        - UPDATE_TASK: Update task for a given chunk_id.
        - DELETE: Delete a given chunk_id.
        :param function: INSERT | UPDATE_TASK | DELETE
        :param chunk_id: Chunk ID
        :param host: Host
        :param task: building | built | propagated
        :return: None
        """
        try:
            conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}'".format(DATABASE, USER, HOST))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            if function == 'INSERT':
                cur.execute("INSERT INTO index_builder VALUES (DEFAULT, {0}, '{1}');".format(chunk_id, host))
            elif function == 'UPDATE_HOST':
                cur.execute("UPDATE index_builder SET ib_host = '{0}' WHERE chunk_id = {1};".format(host, chunk_id))
            elif function == 'UPDATE_TASK':
                cur.execute("UPDATE index_builder SET ib_task = '{0}' WHERE chunk_id = {1};".format(task, chunk_id))
            elif function == 'DELETE':
                cur.execute("DELETE FROM index_builder WHERE chunk_id = {0};".format(chunk_id))
            else:
                print('NO FUNCTION FOUND')

            conn.commit()
            cur.close()
        except Exception as e:
            print(e)

    def operate_on_index_server_relation(self, function, chunk_id, row=0, host='101.101.101.101:101'):
        """
        Execute basic operations on index server relation.
        - INSERT: Insert a given row, chunk id and host. Default host is '101.101.101.101:101', default row is 0.
        - UPDATE_ROW: Update row for a given chunk id and host.
        - UPDATE_CHUNK_ID: Update chunk id for a given row and host.
        - UPDATE_HOST: Update host for a given row and chunk id.
        :param function: INSERT | UPDATE ROW | UPDATE CHUNK_ID | UPDATE_HOST | DELETE
        :param chunk_id: Chunk ID
        :param row: Row number
        :param host: Host
        :return: None
        """
        try:
            conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}'".format(DATABASE, USER, HOST))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            if function == 'INSERT':
                cur.execute("INSERT INTO index_server VALUES (DEFAULT, {0}, {1}, '{2}');".format(row, chunk_id, host))
            elif function == 'UPDATE_ROW':
                cur.execute("UPDATE index_server SET row = {0} WHERE chunk_id = {1} AND is_host = '{2}';".format(row, chunk_id, host))
            elif function == 'UPDATE_CHUNK_ID':
                cur.execute("UPDATE index_server SET chunk_id = {0} WHERE row = {1} AND is_host = '{2}';".format(chunk_id, row, host))
            elif function == 'UPDATE_HOST':
                cur.execute("UPDATE index_server SET is_host = '{0}' WHERE row = {1} AND chunk_id = {2};".format(host, row, chunk_id))
            elif function == 'DELETE':
                cur.execute("DELETE FROM index_server WHERE chunk_id = {0};".format(chunk_id))
            else:
                print('NO FUNCTION FOUND')

            conn.commit()
            cur.close()
        except Exception as e:
            print(e)

    def get_relation_for_chunk_id(self, relation_name, chunk_id):
        """
        Return all results in a given relation for a specific chunk id.
        For example:
            - get_relation_for_chunk_id(relation_name='crawler', 101) returns crawler's host for chunk id 101
            - get_relation_for_chunk_id(relation_name='index_builder', 101) returns index builder's host for chunk id 101
        :param chunk_id: Chunk ID
        :return: List
        """
        try:
            conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}'".format(DATABASE, USER, HOST))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("SELECT * FROM {0} WHERE chunk_id = {1};".format(relation_name, chunk_id))

            results = cur.fetchall()
            cur.close()
            return results
        except Exception as e:
            print(e)

    def get_all_relations_for_all_chunks(self):
        """
        Return all relations for all chunks in chunk relation.
        :return: List of dictionary
        """
        results = []
        chunks = self.get_relation('chunk')
        for chunk in chunks:
            temp_dict = {}
            chunk_id = chunk['id']

            links = self.get_relation_for_chunk_id('link', chunk_id=chunk_id)
            crawler = self.get_relation_for_chunk_id('crawler', chunk_id=chunk_id)
            index_builder = self.get_relation_for_chunk_id('index_builder', chunk_id=chunk_id)
            index_server = self.get_relation_for_chunk_id('index_server', chunk_id=chunk_id)

            temp_dict['chunk_id'] = chunk_id
            temp_dict['links'] = links
            temp_dict['crawler'] = crawler
            temp_dict['index_builder'] = index_builder
            temp_dict['index_server'] = index_server

            results.append(temp_dict)

        return results

    def get_length(self, relation_name):
        """
        Return length of a given relation.
        :param relation_name: Relation name
        :return: Int
        """
        try:
            conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}'".format(DATABASE, USER, HOST))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("SELECT COUNT(*) FROM {0};".format(relation_name))
            result = cur.fetchall()
            cur.close()
            return result[0]['count']
        except Exception as e:
            print(e)

    def get_first_n_pending_links(self, number):
        """
        Get first number of links for a given state.
        :param number: Number of links
        :return: List of rows where each row is a dictionary which has a link
        """
        try:
            conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}'".format(DATABASE, USER, HOST))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("SELECT * FROM link WHERE chunk_id IS NULL AND state = 'pending' ORDER BY index LIMIT {0};".format(number))
            results = cur.fetchall()
            cur.close()
            return results
        except Exception as e:
            print(e)

    def get_first_n_crawled_chunk_ids(self, number):
        """
        Get first number of crawled chunk ids
        :param number: Number of chunk ids
        :return: List of rows where each row is a dictionary which has chunk id
        """
        try:
            conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}'".format(DATABASE, USER, HOST))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("SELECT * FROM crawler WHERE c_task = 'crawled' ORDER BY index LIMIT {0};".format(number))
            results = cur.fetchall()
            cur.close()
            return results
        except Exception as e:
            print(e)

    def get_index_servers_from_host(self):
        """
        Return a list of index servers available in host relation.
        :return: List of rows where each row is a dictionary that has index server
        """
        try:
            conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}'".format(DATABASE, USER, HOST))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("SELECT * FROM host WHERE type = 'Index Server';")
            results = cur.fetchall()
            cur.close()
            return results
        except Exception as e:
            print(e)

    def delete_first_row(self, relation_name):
        """
        Delete first row for a given relation.
        :param relation_name: Relation name
        :return: None
        """
        try:
            conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}'".format(DATABASE, USER, HOST))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("DELETE FROM {0} WHERE ctid IN (SELECT ctid FROM {0} ORDER BY index LIMIT 1);".format(relation_name))
            conn.commit()
            cur.close()
        except Exception as e:
            print(e)

    def __delete_relation__(self, relation_name):
        """
        Delete relation.
        :param relation_name: Relation name
        :return: None
        """
        try:
            conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}'".format(DATABASE, USER, HOST))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("DELETE FROM {0};".format(relation_name))
            conn.commit()
            cur.close()
        except Exception as e:
            print(e)