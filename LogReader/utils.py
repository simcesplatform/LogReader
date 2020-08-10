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

def processDateParams( req, resp, resource, params, fromDateParam, toDateParam  ):
    '''
    To be used as a falcon before hook for converting fromDate and toDate query parameters into datetime objects.
    If there is an invalid value raises falcon.HTTPBadRequest.
    fromDateParam and toDateParam are the names of query parameters containing start and end dates.
    '''
    fromDate = req.get_param( fromDateParam )
    if fromDate:
        try:
            fromDate = dateutil.parser.isoparse( fromDate  )
            params[fromDateParam] = fromDate
            
        except ValueError:
            raise falcon.HTTPBadRequest( title = "Invalid datetime value", description = f"Invalid datetime value for {fromDateParam}: {fromDate}" )
    
    toDate = req.get_param( toDateParam )
    if toDate:
        try:
            toDate = dateutil.parser.isoparse( toDate )
            params[toDateParam] = toDate
            
        except ValueError:
            raise falcon.HTTPBadRequest( title = "Invalid datetime value", description = f"Invalid datetime value for {toDateParam}: {toDate}" )
        
def paramToInt( paramName, req ):
    '''
    Convert a query parameter from given request to integer. Raises BadRequest if the value cannot be converted into an integer.
    paramName (str): Name of a query parameter whose value should be an integer.
    req: A falcon HTTP request that has the query parameter.
    Returns the parameter value as an integer or None if the request does not have a value for the parameter.
    '''
    param = req.get_param( paramName )
    if param:
        try:
            param = int( param )
            
        except ValueError:
            raise falcon.HTTPBadRequest( title = "Invalid integer value", description = f"Invalid integer value for {paramName}: {param}." )
        
    return param