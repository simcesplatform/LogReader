# -*- coding: utf-8 -*-
'''
Contains functions for querying information about simulations.
'''
import logging
from LogReader.db import db

log = logging.getLogger( __name__ )
# name of the collection containing information about simulations
simCollection = 'simulations'

def getSimulations():
    '''
    Used to get all simulations.
    Returns a list of dictionaries.
    '''
    log.debug( 'Getting all simulations.' )
    # query all. Get all attributes except the MongoDB id.
    result = db[simCollection].find( {}, { '_id': 0 } )
    return list( result )