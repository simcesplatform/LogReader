# -*- coding: utf-8 -*-
'''
Methods for getting messages from the database.
'''

import logging

from LogReader.db import db

epochNumAttr = 'EpochNumber'
processAttr = 'SourceProcessId'
warningsAttr = 'Warnings'

log = logging.getLogger( __name__ )

collectionNamePrefix = 'simulation_'
 
def getMessages( simId, epoch  = None, startEpoch = None, endEpoch = None, process = None, onlyWarnings = False ):
    '''
    Get messages that match the given parameters.
    simId: Id of the simulation whose messages are fetched.
    epoch (int): Return messages from the given epoch.  
    startEpoch (integer): Return messages from and after the given epoch.
    endEpoch (integer): Return messages from and before the given epoch.
    process (list): List of source process ids. Returns messages whose source process id is in the list.
    onlyWarnings (boolean): If True return only messages which contain warnings. 
    Returns a list of dictionaries. None if there is no collection for the messages.
    '''
    log.debug( f'Get messages for simulation {simId} with parameters epoch: {epoch}, startEpoch: {startEpoch}, endEpoch: {endEpoch}, process: {process}, onlyWarnings: {onlyWarnings},.' )
    collectionName = collectionNamePrefix +simId
    if len( db.list_collection_names( filter = { 'name': collectionName } ) ) == 0:
        log.debug( f'No collection with name {collectionName}.')
        return None
    
    query = {}
    if epoch != None:
        query[epochNumAttr] = epoch
    
    if startEpoch != None:
        query[epochNumAttr] = { '$gte': startEpoch }
        
    if endEpoch != None:
        query.setdefault( epochNumAttr, {} )['$lte'] = endEpoch
    
    if process:
        query[ processAttr ] = { '$in': process }
        
    if onlyWarnings == True:
        query[ warningsAttr ] = { '$exists': True }
        
    log.debug( f'Getting messages from collection {collectionName} with query: {query}.')    
    result = db[ collectionName ].find( query, { '_id': 0 } )
    return list( result ) 