# -*- coding: utf-8 -*-
'''
Methods for getting messages from the database.
'''

import logging

from LogReader.db import db

epochNumAttr = 'EpochNumber'

log = logging.getLogger( __name__ )

collectionNamePrefix = 'simulation_'
 
def getMessages( simId, epoch  = None ):
    '''
    Get messages that match the given parameters.
    simId: Id of the simualtion whose messages are fetched.
    epoch (int): Return messages from the given epoch.  
    Returns a list of dictionaries. None if there is no collection for the messages.
    '''
    log.debug( f'Get messages for simulation {simId} with parameters epoch: {epoch},.' )
    collectionName = collectionNamePrefix +simId
    if len( db.list_collection_names( filter = { 'name': collectionName } ) ) == 0:
        log.debug( f'No collection with name {collectionName}.')
        return None
    
    query = {}
    if epoch != None:
        query[epochNumAttr] = epoch
    
    log.debug( f'Getting messages from collection {collectionName} with query: {query}.')    
    result = db[ collectionName ].find( query, { '_id': 0 } )
    return list( result ) 