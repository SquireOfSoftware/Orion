#!/usr/bin/env python

import mysql
from abc import ABCMeta, abstractmethod
import logging
import singleton

logging.basicConfig(filename='dal.log', filemode='w', level=logging.DEBUG)

@Singleton
class database_layer(object):
    def __init__(self):
        #Collection of connections
        self.connections = {}
        logging.info('Database Layer Initialised')

    #expect { 'type' : { 'connecting_object': [Connection] } }
    def add(self, **connect):
        try:
            if key in connect.type not in self.connections:
                if not isinstance(connect.type.value, Connection):
                    raise TypeError("Not a connection object!") 
                self.connections[connect.type.key] = connect.type.value
            else:
                raise ExistingConnectionError("Already Existing Connection!") 
        except TypeError as e:
            logging.debug("DatabaseLayer.add returned TypeError: " + e.args)
        except ExistingConnectionError as e:
            logging.debug("DatabaseLayer.add returned ExistingConnectionError:" + e.value)

    #expect { { 'type' 'connecting_object': [Connection] } }
    #if 'killall' : 'true', close everything
    def remove(self, **connect):
        #find then close the connection
        if connect.killall.value is 'true':
            for connections in self.connections:
                 connections.close()

    class ExistingConnectionError(Exception):
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return repr(self.value)

class Connection(object):
    def __init__(self):
        self.config = { 'user' : 'mothership', 'passwd' : 'homeone', 'db' : 'drone' }

    def connect(self):
        try:
            self.connection = connector;
            self.connection.connect(**self.config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            cnx.close()
    @classmethod
    def close(self):
    #Close the database connection
        pass
