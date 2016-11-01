#!/usr/bin/env python

import mysql.connector
from mysql.connector import pooling
from mysql.connector import errorcode
import logging

logging.basicConfig(filename='dal.log', filemode='w', level=logging.DEBUG)

# Base Class
# All DAL users inherit this class

# """All services using connection should inherit this code."""
dbconfig = {"database": "Drone_Surveying_System",
            "user"    : "root",
            "password"  : "default"}

pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="dronepool",
                                                  pool_size=4,
                                                  **dbconfig)

class connector(object):
    def __init__(self):
        self.connection = None
        logging.basicConfig(filename='dbmsql.log', level=logging.DEBUG)
        print "Connector out"
        self.cursor = None
        return

    # add to connection pool
    def connect(self):
        try:
            logging.info('Attempting Connection to mysql db')
            self.connection = pool.get_connection()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logging.debug('Access denied')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logging.debug('Database does not exist')
            else:
                logging.debug(err)
        self.cursor = self.connection.cursor(prepared=True)
        return

    # close the connection
    def disconnect(self):
        self.cursor.close()
        self.connection.close()
        return

    def cursor(self):
        return self.cursor

    def connection(self):
        return self.connection
