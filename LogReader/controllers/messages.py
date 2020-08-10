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
        
    def on_get(self, req, resp, simId):
        '''
        Get messages for simulation:
        simId: Simulation id from the URL path.
        '''
        log.debug( f'Get messages for simulation with id {simId} with parameters {req.params}.' )
        epoch = utils.paramToInt( 'epoch', req )
            
        result = self._messageStore.getMessages( simId, epoch = epoch )
        if result == None:
            raise falcon.HTTPNotFound( title = 'Simulation not found.', description = f'Simulation with id {simId} not found.' )
        
        resp.media = result