# -*- coding: utf-8 -*-
'''
Contains functions for querying information about simulations.
'''
import logging
from LogReader.db import db

# simulation attribute names
simIdAttr = 'SimulationId'
startTimeAttr = 'startTime'
endTimeAttr = 'endTime'

log = logging.getLogger( __name__ )
# name of the collection containing information about simulations
simCollection = 'simulations'

def getSimulations( start = None, end = None ):
    '''
    Get simulations. Without parameters returns all simulations.
    start (datetime): If given gets simulations that have been started on or after the given time.
    end (datetime): If given returns simulations that have been started on or beforre the given time.
    Returns a list of dictionaries.
    '''
    query = {} # MongoDB query, If no parameters will be used as is.
        
    if start:
        query[ startTimeAttr ] = { '$gte':  start } 
        
    if end:
        # there may or may not be already something for start time in the query 
        query.setdefault( startTimeAttr, {} )['$lte'] = end
    
    log.debug( f'Getting simulations with params start {start}, end: {end}. Using mongo query {query}.' )    
    # Get all attributes except the MongoDB id.
    result = db[simCollection].find( query, { '_id': 0 } )
    return list( result )