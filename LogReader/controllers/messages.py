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
        # process and validate possible fromSimDate and toSimDate date parameters  
        fromSimDate, toSimDate = utils.processDateParams( req.params, 'fromSimDate', 'toSimDate' )
        # Get possible epoch filtering parameters and check that they are integers.
        epoch = utils.paramToInt( 'epoch', req )
        startEpoch = utils.paramToInt( 'startEpoch', req )
        endEpoch = utils.paramToInt( 'endEpoch', req )
        
        # get possible process ids and separate comma separated values into a list.
        process = req.get_param( 'process' )
        if process:
            process = process.split( ',' )
        
        # get onlyWarnings parameter and convert to bool    
        onlyWarnings = req.get_param_as_bool( 'onlyWarnings', default = False )
        # get topic parameter
        topic = req.get_param( 'topic' )
        
        # get the messages
        result = self._messageStore.getMessages( simId, epoch = epoch, startEpoch = startEpoch, endEpoch = endEpoch, process = process, onlyWarnings = onlyWarnings, fromSimDate = fromSimDate, toSimDate = toSimDate, topic = topic )
        # result None means that there is no simulation with the id (no corresponding mongodb collection for the messages)
        if result == None:
            raise falcon.HTTPNotFound( title = 'Simulation not found.', description = f'Simulation with id {simId} not found.' )
        
        resp.media = result