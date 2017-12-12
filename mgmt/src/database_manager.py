#! /usr/bin/env python3
"""
    database_manager.py - Database Manager
    Author:
        - Hoanh An (hoanhan@bennington.edu)
    Date: 12/2/2017
"""

import psycopg2
import psycopg2.extras
from psycopg2 import sql

DATABASE = 'mgmt_db'
# USER = 'postgres'


class DatabaseManager():
    def operate_on_link_relation(self, function, link, chunk_id=None, state='pending'):
        """
        Execute basic operations on link relation
        - INSERT: Insert a given link and chunk id. Default chunk id is None state is pending
        - UPDATE_STATE: Update chunk id for a given link
        - UPDATE_STATE: Update state for a given link
        - DELETE: Delete a given link
        :param function: INSERT | UPDATE_CHUNK_ID | UPDATE_STATE | DELETE
        :param link: URL
        :param state: OK | Error
        :return: None
        """
        try:
            conn = psycopg2.connect("dbname='{0}'".format(DATABASE))


            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            if function == 'INSERT':
                cur.execute("INSERT INTO link (link, state) VALUES (%s, %s);", (link, state))
            elif function == 'UPDATE_CHUNK_ID':
                cur.execute("UPDATE link SET chunk_id = %s WHERE link = %s;", (chunk_id, link,))
            elif function == 'UPDATE_STATE':
                cur.execute("UPDATE link SET state = %s WHERE link = %s;", (state, link,))
            elif function == 'DELETE':
                cur.execute("DELETE FROM link WHERE link = %s;", (link,))
            else:
                print('NO FUNCTION FOUND')

            conn.commit()
            cur.close()
        except Exception as e:
            print(e)

    def operate_on_chunk_relation(self, function, chunk_id):
        """
        Execute basic operations on chunk relation
        - INSERT: Insert a given chunk id. Default state is None
        - DELETE: Delete a given chunk id
        :param function: INSERT | DELETE
        :param chunk_id: Chunk ID
        :param state: OK | Error
        :return: None
        """
        try:
            conn = psycopg2.connect("dbname='{0}'".format(DATABASE))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            if function == 'INSERT':
                cur.execute("INSERT INTO chunk (id) VALUES (%s);", (chunk_id,))
            elif function == 'DELETE':
                cur.execute("DELETE FROM chunk WHERE id = %s;", (chunk_id,))
            else:
                print('NO FUNCTION FOUND')

            conn.commit()
            cur.close()
        except Exception as e:
            print(e)

    def operate_on_host_relation(self, function, host, type=None, state='offline', health=None):
        """
        Execute basic operations on host relation
        - INSERT: Insert a given host and type. Default state is offline and health is None
        - UPDATE_STATE: Update state for a given host
        - UPDATE_HEALTH: Update health for a given host
        - DELETE: Delete a given host
        :param function: INSERT | UPDATE_STATE | UPDATE_HEALTH | DELETE
        :param host: Host
        :param type: Crawler | Index Builder | Index Server
        :param state: online | waiting | error | paused
        :param health: healthy | failure | probation
        :return: None
        """
        try:
            conn = psycopg2.connect("dbname='{0}'".format(DATABASE))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            if function == 'INSERT':
                cur.execute("INSERT INTO host (host, type, state) VALUES (%s, %s, %s);", (host, type, state,))
            elif function == 'UPDATE_STATE':
                cur.execute("UPDATE host SET state = %s WHERE host = %s;", (state, host,))
            elif function == 'UPDATE_HEALTH':
                cur.execute("UPDATE host SET health = %s WHERE host = %s;", (health, host,))
            elif function == 'DELETE':
                cur.execute("DELETE FROM host WHERE host = %s;", (host,))
            else:
                print('NO FUNCTION FOUND')

            conn.commit()
            cur.close()
        except Exception as e:
            print(e)

    def operate_on_crawler_relation(self, function, chunk_id, host=None, task='crawling'):
        """
        Execute basic operations on crawler relation
        - INSERT: Insert a given chunk_id and host. Default task is crawling
        - UPDATE_TASK: Update task for a given chunk_id
        - DELETE: Delete a given chunk_id
        :param function: INSERT | UPDATE_TASK | DELETE
        :param chunk_id: Chunk ID
        :param host: Host
        :param task: crawling | crawled | propagated
        :return: None
        """
        try:
            conn = psycopg2.connect("dbname='{0}'".format(DATABASE))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            if function == 'INSERT':
                cur.execute("INSERT INTO crawler (chunk_id, c_host, c_task) VALUES (%s, %s, %s);", (chunk_id, host, task,))
            elif function == 'UPDATE_HOST':
                cur.execute("UPDATE crawler SET c_host = %s WHERE chunk_id = %s;", (host, chunk_id,))
            elif function == 'UPDATE_TASK':
                cur.execute("UPDATE crawler SET c_task = %s WHERE chunk_id = %s;", (task, chunk_id,))
            elif function == 'DELETE':
                cur.execute("DELETE FROM crawler WHERE chunk_id = %s;", (chunk_id,))
            else:
                print('NO FUNCTION FOUND')

            conn.commit()
            cur.close()
        except Exception as e:
            print(e)

    def operate_on_index_builder_relation(self, function, chunk_id, host=None, task='building'):
        """
        Execute basic operations on index builder relation
        - INSERT: Insert a given chunk_id and host. Default task is building
        - UPDATE_TASK: Update task for a given chunk_id
        - DELETE: Delete a given chunk_id
        :param function: INSERT | UPDATE_TASK | DELETE
        :param chunk_id: Chunk ID
        :param host: Host
        :param task: building | built | propagated
        :return: None
        """
        try:
            conn = psycopg2.connect("dbname='{0}'".format(DATABASE))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            if function == 'INSERT':
                cur.execute("INSERT INTO index_builder (chunk_id, ib_host, ib_task) VALUES (%s, %s, %s);", (chunk_id, host, task))
            elif function == 'UPDATE_HOST':
                cur.execute("UPDATE index_builder SET ib_host = %s WHERE chunk_id = %s;", (host, chunk_id,))
            elif function == 'UPDATE_TASK':
                cur.execute("UPDATE index_builder SET ib_task = %s WHERE chunk_id = %s;", (task, chunk_id,))
            elif function == 'DELETE':
                cur.execute("DELETE FROM index_builder WHERE chunk_id = %s;", (chunk_id,))
            else:
                print('NO FUNCTION FOUND')

            conn.commit()
            cur.close()
        except Exception as e:
            print(e)

    def operate_on_index_server_relation(self, function, row, chunk_id, host):
        """
        Execute basic operations on index server relation
        - INSERT: Insert a given row, chunk id and host
        - UPDATE_ALL: Update a record for a given row, chunk id, and host
        - UPDATE_ROW: Update row (column) for a given chunk id and host
        - UPDATE_CHUNK_ID: Update chunk id for a given row and host
        - UPDATE_HOST: Update host for a given row and chunk id
        :param function: INSERT | UPDATE ROW | UPDATE CHUNK_ID | UPDATE_HOST | DELETE
        :param chunk_id: Chunk ID
        :param row: Row number
        :param host: Host
        :return: None
        """
        try:
            conn = psycopg2.connect("dbname='{0}'".format(DATABASE))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            if function == 'INSERT':
                cur.execute("INSERT INTO index_server (row, chunk_id, is_host) VALUES (%s, %s, %s);", (row, chunk_id, host,))
            elif function == 'UPDATE_ROW':
                cur.execute("UPDATE index_server SET row = %s WHERE chunk_id = %s AND is_host = %s;", (row, chunk_id, host,))
            elif function == 'UPDATE_CHUNK_ID':
                cur.execute("UPDATE index_server SET chunk_id = %s WHERE row = %s AND is_host = %s;", (chunk_id, row, host,))
            elif function == 'UPDATE_HOST':
                cur.execute("UPDATE index_server SET is_host = %s WHERE row = %s AND chunk_id = %s;", (host, row, chunk_id,))
            elif function == 'DELETE':
                cur.execute("DELETE FROM index_server WHERE row = %s AND chunk_id = %s AND is_host = %s;", (row, chunk_id, host,))
            else:
                print('NO FUNCTION FOUND')

            conn.commit()
            cur.close()
        except Exception as e:
            print(e)

    def get_relation(self, relation_name):
        """
        Get all records for a given relation
        :param relation_name: Relation name
        :return: List of dictionary
        """
        try:
            conn = psycopg2.connect("dbname='{0}'".format(DATABASE))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(sql.SQL("SELECT * FROM {} ORDER BY index").format(sql.Identifier(relation_name)))
            relation = cur.fetchall()
            cur.close()
            return relation
        except Exception as e:
            print(e)

    def get_relation_for_chunk_id(self, relation_name, chunk_id):
        """
        Return all results in a given relation for a specific chunk id
        Example:
            - get_relation_for_chunk_id(relation_name='crawler', 101) returns crawler's host for chunk id 101
            - get_relation_for_chunk_id(relation_name='index_builder', 101) returns index builder's host for chunk id 101
        :param chunk_id: Chunk ID
        :return: List of dictionary
        """
        try:
            conn = psycopg2.connect("dbname='{0}'".format(DATABASE))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(sql.SQL("SELECT * FROM {} WHERE chunk_id = %s").format(sql.Identifier(relation_name)), [chunk_id])
            results = cur.fetchall()
            cur.close()
            return results
        except Exception as e:
            print(e)

    def get_all_relations_for_all_chunks(self):
        """
        Return all relations for all chunks in chunk relation
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

    def get_relation_length(self, relation_name):
        """
        Return length of a given relation
        :param relation_name: Relation name
        :return: Int
        """
        try:
            conn = psycopg2.connect("dbname='{0}'".format(DATABASE))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(sql.SQL("SELECT COUNT(*) FROM {}").format(sql.Identifier(relation_name)))
            result = cur.fetchall()
            cur.close()
            return result[0]['count']
        except Exception as e:
            print(e)

    def get_first_n_pending_links(self, number):
        """
        Get the first number pending links
        :param number: Number of links
        :return: List of dictionary
        """
        try:
            conn = psycopg2.connect("dbname='{0}'".format(DATABASE))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("SELECT link FROM link WHERE chunk_id IS NULL AND state = 'pending' ORDER BY index LIMIT %s;", (number,))
            results = cur.fetchall()
            cur.close()
            return results
        except Exception as e:
            print(e)

    def get_first_n_crawled_chunks(self, number):
        """
        Get the first number crawled chunk ids
        :param number: Number of chunk ids
        :return: List of dictionary
        """
        try:
            conn = psycopg2.connect("dbname='{0}'".format(DATABASE))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("SELECT * FROM crawler WHERE c_task = 'crawled' ORDER BY index LIMIT %s;", (number,))
            results = cur.fetchall()
            cur.close()
            return results
        except Exception as e:
            print(e)

    def get_first_n_built_chunk_ids(self, number):
        """
        Get the first number built chunk ids
        :param number: Number of chunk ids
        :return: List of dictionary
        """
        try:
            conn = psycopg2.connect("dbname='{0}'".format(DATABASE))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("SELECT chunk_id FROM index_builder WHERE ib_task = 'built' ORDER BY index LIMIT %s;", (number,))
            results = cur.fetchall()
            cur.close()
            return results
        except Exception as e:
            print(e)

    def get_all_index_servers(self):
        """
        Get a list of index servers available in host relation.
        :return: List of dictionary
        """
        try:
            conn = psycopg2.connect("dbname='{0}'".format(DATABASE))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("SELECT * FROM host WHERE type = 'Index Server';")
            results = cur.fetchall()
            cur.close()
            return results
        except Exception as e:
            print(e)

    def get_all_index_builders(self):
        """
        Get a list of index builders available in host relation.
        :return: List of dictionary
        """
        try:
            conn = psycopg2.connect("dbname='{0}'".format(DATABASE))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("SELECT * FROM host WHERE type = 'Index Builder';")
            results = cur.fetchall()
            cur.close()
            return results
        except Exception as e:
            print(e)

    def get_all_crawlers(self):
        """
        Get a list of crawlers available in host relation.
        :return: List of dictionary
        """
        try:
            conn = psycopg2.connect("dbname='{0}'".format(DATABASE))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("SELECT * FROM host WHERE type = 'Crawler';")
            results = cur.fetchall()
            cur.close()
            return results
        except Exception as e:
            print(e)

    def get_chunk_hosts_for_index_servers(self, host):
        """
        Get all index servers for a given host
        :param host: Host url of the index server
        :return: List of dictionary
        """
        try:
            conn = psycopg2.connect("dbname='{0}'".format(DATABASE))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("SELECT * FROM index_server WHERE is_host = %s;", (host,))
            results = cur.fetchall()

            temp = []
            for chunk in results:
                temp_dict = {}
                chunk_id = chunk['chunk_id']
                temp_dict['chunk_id'] = chunk_id
                temp_dict['hosts'] = {}
                temp_dict['hosts']['c_host'] = self.get_relation_for_chunk_id('crawler', chunk_id)[0]['c_host']
                temp_dict['hosts']['ib_host'] = self.get_relation_for_chunk_id('index_builder', chunk_id)[0]['ib_host']
                temp.append(temp_dict)
            cur.close()
            return temp
        except Exception as e:
            print(e)

    def get_chunk_id_for_link(self, link):
        """
        Get chunk id for a given link
        :param link: String of the link
        :return: Link as a dictionary
        """
        try:
            conn = psycopg2.connect("dbname='{0}'".format(DATABASE))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("SELECT chunk_id FROM link WHERE link = %s;", (link,))
            result = cur.fetchall()
            cur.close()
            return result
        except Exception as e:
            print(e)

    def get_links_for_chunk_id(self, chunk_id):
        """
        Get all crawling links available for a given chunk id
        :param chunk_id: Chunk ID
        :return: List of dictionary
        """
        try:
            conn = psycopg2.connect("dbname='{0}'".format(DATABASE))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("SELECT link FROM link WHERE chunk_id = %s AND state = 'crawling';", (chunk_id,))
            result = cur.fetchall()
            cur.close()
            return result
        except Exception as e:
            print(e)

    def get_chunk_ids_for_index_server(self, host):
        """
        Get chunk ids for a given Index Server's host
        :param host: Host
        :return: Dictionary of index server host and its chunk ids
        """
        try:
            conn = psycopg2.connect("dbname='{0}'".format(DATABASE))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("SELECT * FROM index_server WHERE is_host = %s;", (host,))
            results = cur.fetchall()

            if results == []:
                return {}

            temp_dict = {}
            temp_dict['host'] = host
            temp_dict['row'] = results[0]['row']
            temp_dict['chunk_ids'] = []

            for entry in results:
                temp_dict['chunk_ids'].append(entry['chunk_id'])

            cur.close()

            return temp_dict
        except Exception as e:
            print(e)

    def clear_relation(self, relation_name):
        """
        Clear all records for a given relation
        :param relation_name: Relation name
        :return: None
        """
        try:
            conn = psycopg2.connect("dbname='{0}'".format(DATABASE))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(sql.SQL("DELETE FROM {}").format(sql.Identifier(relation_name)))
            cur.execute("ALTER SEQUENCE {0}_index_seq RESTART WITH 1;".format(relation_name))
            conn.commit()
            cur.close()
        except Exception as e:
            print(e)