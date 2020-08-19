# -*- coding: utf-8 -*-
'''
Processor for get messages requests.
'''

import logging

import falcon

from LogReader import utils

log = logging.getLogger( __name__ )

class MsgController(object):
    '''
    Process requests about messages.
    '''

    def __init__(self, messageStore ):
        '''
        Initialize message request processor.
        messageStore: Module with method for getting messages.
        '''
        self._messageStore = messageStore
    
    def on_get(self, req, resp, simId ):
        '''
        Get messages for simulation:
        simId: Simulation id from the URL path.
        '''
        log.debug( f'Get messages for simulation with id {simId} with parameters {req.params}.' )
        result = getMessagesWithParams( self._messageStore, simId, req.params )
        # result None means that there is no simulation with the id (no corresponding mongodb collection for the messages)
        if result == None:
            raise falcon.HTTPNotFound( title = 'Simulation not found.', description = f'Simulation with id {simId} not found.' )
        
        resp.media = result
        
def getMessagesWithParams( messageStore, simId, params ):
    '''
    Get messages for given simulation filtered by params.
    simId (Str): Sumlation id.
    params (dict): Parameters for getting messages from for example query parameters from a falcon HTTP request. 
    Retuns list of messages or None if there is no simulation corresponding to the given id.
    Raises falcon.HTTPBadRequest if there are invalid values for sim dates, epoch numbers or onlyWarnings.
    '''
    # process and validate possible fromSimDate and toSimDate date parameters  
    fromSimDate, toSimDate = utils.processDateParams( params, 'fromSimDate', 'toSimDate' )
    # Get possible epoch filtering parameters and check that they are integers.
    epoch = utils.paramToInt( 'epoch', params )
    startEpoch = utils.paramToInt( 'startEpoch', params )
    endEpoch = utils.paramToInt( 'endEpoch', params )
    
    # get possible process ids and separate comma separated values into a list if the value is not already a list.
    process = params.get( 'process' )
    if process and type( process ) != list:
        process = process.split( ',' )
    
    # get onlyWarnings parameter and convert to bool if not already converted
    onlyWarnings = params.get( 'onlyWarnings', False )
    if onlyWarnings and type( onlyWarnings ) != bool:
        conversion = { 'true': True, 'false': False }
        try:
            onlyWarnings = conversion[onlyWarnings]
            
        except KeyError:
            raise falcon.HTTPBadRequest( title = 'Invalid value for onlyWarnings.', description = f'Value should be true or false but it was {onlyWarnings}.' )
        
    # get topic parameter
    topic = params.get( 'topic' )
    
    # get the messages
    result = messageStore.getMessages( simId, epoch = epoch, startEpoch = startEpoch, endEpoch = endEpoch, process = process, onlyWarnings = onlyWarnings, fromSimDate = fromSimDate, toSimDate = toSimDate, topic = topic )
    return result
