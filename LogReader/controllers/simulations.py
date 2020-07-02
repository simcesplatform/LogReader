# -*- coding: utf-8 -*-
'''
Processors for requests related to simulations.
'''

import logging

log = logging.getLogger( __name__ )

class SimController:
    '''
    Process requests about simulations.
    '''
    
    def __init__( self, simulationStore ):
        '''
        Initialize simulation request processor.
        simulationStore: module used to get simulations from database.
        '''
        self._simulationStore = simulationStore
        
    def on_get( self, req, resp ):
        '''
        Process request for getting list of simulations.
        '''
        log.debug( 'Got request for all simulations.' )
        results = self._simulationStore.getSimulations()
        resp.media = results 