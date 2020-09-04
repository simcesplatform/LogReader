'''
Created on 3.9.2020

@author: hylli
'''
import logging

import falcon

from LogReader import utils
from LogReader.services import timeSeries 

log = logging.getLogger( __name__ )

class TimeSeriesController():
    '''
    classdocs
    '''


    def __init__(self, messageStore ):
        '''
        Constructor
        '''
        self._messageStore = messageStore
        
    def on_get(self, req, resp, simId ):
        log.debug( f'Get time series for simulation with id {simId} with parameters {req.params}.' )
        params = utils.validateMessageParams( req.params )
        format = req.get_param( 'format' )
        if format != None:
            if format not in [ 'json', 'csv' ]:
                raise falcon.HTTPBadRequest( title = 'Invalid time series result format.', description = f'Format should be json or csv instead of {format}.' )
            
        else:
            format = 'json'
            
        attrs = req.get_param( 'attrs', required = True ).split( ',' )
        msgFilter = timeSeries.TimeSeriesMessageFilter( attrs, topic = params.get( 'topic' ), process = params.get( 'process' ))
        del params['attrs']
        del params['process']
        del params['topic']
        del params['onlyWarnings']
        del params['format']
        result = timeSeries.getTimeSeries( self._messageStore, simId, [ msgFilter ], csv = format == 'csv', **params )
        if format == 'json':
            resp.media = result
            
        elif format == 'csv':
            resp.content_type = 'text/csv'
            resp.body = result 
        