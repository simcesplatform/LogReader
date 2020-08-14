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
        
    @falcon.before( utils.processDateParams, 'fromSimDate', 'toSimDate' )
    def on_get(self, req, resp, simId, fromSimDate = None, toSimDate = None ):
        '''
        Get messages for simulation:
        simId: Simulation id from the URL path.
        '''
        log.debug( f'Get messages for simulation with id {simId} with parameters {req.params}.' )
        # Get possible epoch filtering parameters and check that they are integers.
        epoch = utils.paramToInt( 'epoch', req )
        startEpoch = utils.paramToInt( 'startEpoch', req )
        endEpoch = utils.paramToInt( 'endEpoch', req )
        
        # get possible process ids and separate comma separated values into a list.
        process = req.get_param( 'process' )
        if process:
            process = process.split( ',' )
            
        onlyWarnings = req.get_param_as_bool( 'onlyWarnings', default = False )
        topic = req.get_param( 'topic' )
        
        result = self._messageStore.getMessages( simId, epoch = epoch, startEpoch = startEpoch, endEpoch = endEpoch, process = process, onlyWarnings = onlyWarnings, fromSimDate = fromSimDate, toSimDate = toSimDate, topic = topic )
        if result == None:
            raise falcon.HTTPNotFound( title = 'Simulation not found.', description = f'Simulation with id {simId} not found.' )
        
        resp.media = result