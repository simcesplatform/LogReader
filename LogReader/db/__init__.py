# -*- coding: utf-8 -*-
'''
The db pakcage is for interacting with the mongodb database.
This file initialises the database connection.
'''

import os
import logging
import pymongo

log = logging.getLogger( __name__ )
# create the database client used in this application
host = os.environ.get("MONGODB_HOST", "localhost")
port = int(os.environ.get("MONGODB_PORT", 27017))
dbName = os.environ.get("MONGODB_DATABASE", "messages")
log.info( f'Establishing connection to MongoDB. host: {host}, port: {port}, database: {dbName}.' )
client = pymongo.MongoClient( 
    host = host,
    port = port,
    tz_aware = True, # Returns datetime objects that are timezone aware.
    username = os.environ.get("MONGODB_USERNAME", None ),
    password = os.environ.get("MONGODB_PASSWORD", None ),
    appname = 'LogReader' ) # app name should be visible in some mongodb logs
# the database containing the messages and simulation information
db = client[ dbName ]