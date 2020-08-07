# -*- coding: utf-8 -*-
'''
Methods for getting messages from the database.
'''

import logging

from LogReader.db import db

log = logging.getLogger( __name__ )

collectionNamePrefix = 'simulation_'
 
def getMessages( simId ):
    '''
    Get messages that match the given parameters.
    simId: Id of the simualtion whose messages are fetched.
    Returns a list of dictionaries. None if there is no collection for the messages.
    '''
    collectionName = collectionNamePrefix +simId
    if len( db.list_collection_names( filter = { 'name': collectionName } ) ) == 0:
        return None
    
    query = {}
    result = db[ collectionName ].find( query, { '_id': 0 } )
    return list( result ) 