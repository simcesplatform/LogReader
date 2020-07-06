# -*- coding: utf-8 -*-
'''
Various utility functions.
'''

import datetime

import falcon
import dateutil.parser

def jsonSerializeDate(obj):
    '''
    Used as a parameter for json.dumps to serialize datetime objects to JSON
    '''
    if isinstance(obj, (datetime.date, datetime.datetime)):
        # .isoformat marks utc as +00:00 but we want to use Z
        return obj.isoformat().replace( '+00:00', 'Z' )

def processDateParams( req, resp, resource, params ):
    '''
    To be used as a falcon before hook for converting fromDate and toDate query parameters into datetime objects.
    If there is an invalid value raises falcon.HTTPBadRequest.
    '''
    fromDate = req.get_param( 'fromDate' )
    if fromDate:
        try:
            fromDate = dateutil.parser.isoparse( fromDate  )
            params['fromDate'] = fromDate
            
        except ValueError:
            raise falcon.HTTPBadRequest( title = "Invalid datetime value", description = f"Invalid datetime value for fromDate: {fromDate}" )
    
    toDate = req.get_param( 'toDate' )
    if toDate:
        try:
            toDate = dateutil.parser.isoparse( toDate )
            params['toDate'] = toDate
            
        except ValueError:
            raise falcon.HTTPBadRequest( description = f"Invalid datetime value for toDate: {toDate}" )
        