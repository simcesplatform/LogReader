# -*- coding: utf-8 -*-
'''
Methods for getting messages from the database.
'''

import logging

import pymongo

from LogReader.db import db

epochNumAttr = 'EpochNumber'
processAttr = 'SourceProcessId'
warningsAttr = 'Warnings'
epochStartAttr = 'StartTime'
epochEndAttr = 'EndTime'
topicAttr = 'Topic'
epochTopic = 'Epoch'

log = logging.getLogger( __name__ )

collectionNamePrefix = 'simulation_'

def _getMessageCollectionName( simId ): 
    '''
    Returns the name of the collection where the messages of the simulation run, whose id is given, are stored.
    '''
    return collectionNamePrefix +simId

def getMessages( simId, epoch  = None, startEpoch = None, endEpoch = None, process = None, onlyWarnings = False, toSimDate = None, fromSimDate = None ):
    '''
    Get messages that match the given parameters.
    simId: Id of the simulation whose messages are fetched.
    epoch (int): Return messages from the given epoch.  
    startEpoch (integer): Return messages from and after the given epoch.
    endEpoch (integer): Return messages from and before the given epoch.
    process (list): List of source process ids. Returns messages whose source process id is in the list.
    onlyWarnings (boolean): If True return only messages which contain warnings. 
    fromSimDate (datetime): Return messages from and after the epoch that contains the given date.
    toSimDate (datetime): Return messages from and before the epoch that contains the given date.
    Returns a list of dictionaries. None if there is no collection for the messages.
    '''
    log.debug( f'Get messages for simulation {simId} with parameters epoch: {epoch}, startEpoch: {startEpoch}, endEpoch: {endEpoch}, process: {process}, onlyWarnings: {onlyWarnings},. fromSimDate: {fromSimDate}, toSimDate: {toSimDate}' )
    collectionName = _getMessageCollectionName( simId )
    if len( db.list_collection_names( filter = { 'name': collectionName } ) ) == 0:
        log.debug( f'No collection with name {collectionName}.')
        return None
    
    query = {}
    if fromSimDate or toSimDate:
        startEpoch, endEpoch = _getEpochsForSimDates( simId, fromSimDate, toSimDate )
        epoch = None # This is not relevant with these parameters.
        
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

def _getEpochsForSimDates( simId, fromSimDate = None, toSimDate = None ):
    '''
    Internal helper method for finding the relevant epochs when fromSimDate and toSimDate are used with getMessages
    Returns a tuple containing the first and last epoch numbers. The epoch number is None if there is no epoch.
    '''
    startEpoch = None
    endEpoch = None
    collectionName = _getMessageCollectionName( simId )
    if fromSimDate:
        # query for first epoch that contains the fromSimDate
        query = {
            topicAttr: epochTopic,
            epochStartAttr:  { '$lte': fromSimDate },
            epochEndAttr: { '$gt': fromSimDate }
        }
        
        # we need only the epoch number from the first returned message when they are sorted in ascending order by epoch start time.
        result = db[ collectionName ].find( query, [ epochNumAttr ], limit = 1 ).sort( epochStartAttr, pymongo.ASCENDING )
        try:
            startEpoch = result.next()[ epochNumAttr ]
            
        except StopIteration:
            # no result
            pass
        
    if toSimDate:
        # find the last epoch containing the toSimDate
        query = {
            topicAttr: epochTopic,
            epochStartAttr:  { '$lt': toSimDate },
            epochEndAttr: { '$gte': toSimDate }
        }
        
        # we need only the epoch number from the first returned message when they are sorted in descending order by epoch start time.
        result = db[ collectionName ].find( query, [ epochNumAttr ], limit = 1 ).sort( epochStartAttr, pymongo.DESCENDING )
        try:
            endEpoch = result.next()[ epochNumAttr ]
            
        except StopIteration:
            # no result
            pass
        
    return startEpoch, endEpoch