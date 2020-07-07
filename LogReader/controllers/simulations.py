# -*- coding: utf-8 -*-
'''
Processors for requests related to simulations.
'''

import logging

import dateutil.parser
import falcon

import LogReader.utils


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
        
    @falcon.before( LogReader.utils.processDateParams )
    def on_get_simulations( self, req, resp, toDate = None, fromDate = None  ):
        '''
        Process request for getting list of simulations.
        The LogReader.utils.processDateParams is used as a falcon before hook to convert fromDate and toDate query parameters to datetime objects.
        '''
        log.debug( f'Got request for  simulations with parameters: {req.params}.' )
        
        results = self._simulationStore.getSimulations( fromDate, toDate )
        resp.media = results
        
    def on_get_simulation(self, req, resp, simId ):
        '''
        Response handler for get simulation by id.
        simId (str): URI template parameter for simulation id.
        '''
        log.debug( f'Get simulation with id {simId}.' )
        result = self._simulationStore.getSimulationById( simId )
        if result == None:
            raise falcon.HTTPNotFound( title = 'Simulation not found.', description = f'Simulation with id {simId} not found.' )
        
        resp.media = result