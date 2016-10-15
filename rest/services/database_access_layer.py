#!/usr/bin/env python

import mysql.connector
from mysql.connector import connection
from mysql.connector import pooling
from mysql.connector import errorcode
from abc import ABCMeta, abstractmethod
import logging
import singleton

logging.basicConfig(filename='dal.log', filemode='w', level=logging.DEBUG)


#@singleton.Singleton
#class database_layer(object):
#    def __init__(self):
#        # Collection of connections
#        self.connections = {}
#        logging.info('Database Layer Initialised')
#
    # expect { 'type' : { 'connecting_object': [Connection] } }
#    def add(self, **connect):
#        try:
#            if self.key in connect.type not in self.connections:
#                if not isinstance(connect.type.value, Connection):
#                    raise TypeError("Not a connection object!")
#                self.connections[connect.type.key] = connect.type.value
#            else:
#                raise self.ExistingConnectionError("Already Existing Connection!")
#        except TypeError as e:
#            logging.debug("DatabaseLayer.add returned TypeError: " + e.args)
#        except self.ExistingConnectionError as e:
#            logging.debug("DatabaseLayer.add returned ExistingConnectionError:" + e.value)

    # expect { { 'type' : {'connecting_object': [Connection] }, 'killall' : bool }
    # if 'killall' : 'true', close everything
 #   def remove(self, **connect):
        # find then close the connection
#       if connect.killall.value is 'true':
#           for connections in self.connections:
#                connections.close()

#    def find(self, **connect):
#        return

#    class ExistingConnectionError(Exception):
#        def __init__(self, value):
#            self.value = value

#        def __str__(self):
#            return repr(self.value)


#class Connection(object):
#    def __init__(self):
#        self.config = {'user': 'mothership', 'passwd': 'homeone', 'db': 'drone'}
#
#    def connect(self):
#        try:
#            self.connection = connection
#            self.connection.connect(**self.config)
#        except mysql.connector.Error as err:
#            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#                print("Something is wrong with your user name or password")
#            elif err.errno == errorcode.ER_BAD_DB_ERROR:
#                print("Database does not exist")
#            else:
#                print(err)
#        else:
#            self.connection.close()
#
#    @classmethod
#    def close(self):
#        # Close the database connection
#        pass


# Base Class
# All DAL users inherit this class

"""All services using connection should inherit this code."""
dbconfig = {"database": "drone",
            "user"    : "mothership",
            "passwd"  : "homeone"   }

pool = mysql.connector.pooling.MySQLConnectionPool

class Connector(object):
    def __init__(self):
        self.connection = None;

        return

    # add to connection pool
    def connect(self):
        self.connection = pool.get_connection(    pool_name="dronepool",
                                                            pool_size=4,
                                                            **dbconfig)
        self.cursor = connection.cursor()
        return

    # close the connection
    def disconnect(self):
        self.connection.close()
        return
