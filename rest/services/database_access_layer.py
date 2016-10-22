#!/usr/bin/env python

import mysql.connector
from mysql.connector import connection
from mysql.connector import pooling
from mysql.connector import errorcode
from abc import ABCMeta, abstractmethod
import logging
import singleton

logging.basicConfig(filename='dal.log', filemode='w', level=logging.DEBUG)

# Base Class
# All DAL users inherit this class

# """All services using connection should inherit this code."""
dbconfig = {"database": "Drone_Surveying_System",
            "user"    : "root",
            "passwd"  : "admin"}

pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="dronepool",
                                                  pool_size=4,
                                                  **dbconfig)

class connector(object):
    def __init__(self):
        self.connection = None
        logging.basicConfig(filename='dbmsql.log', level=logging.DEBUG)
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
        self.cursor = self.connection.cursor()
        return

    # close the connection
    def disconnect(self):
        self.connection.close()
        return

testConnector = connector()
testConnector.connect()

testQuery = "SELECT * from Mission;"

print(testConnector.cursor(dictionary=True).execute(testQuery))
testConnector.disconnect()
