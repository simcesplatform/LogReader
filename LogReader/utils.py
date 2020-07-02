# -*- coding: utf-8 -*-
'''
Various utility functions.
'''

import datetime

def jsonSerializeDate(obj):
    '''
    Used as a parameter for json.dumps to serialize datetime objects to JSON
    '''
    if isinstance(obj, (datetime.date, datetime.datetime)):
        # .isoformat marks utc as +00:00 but we want to use Z
        return obj.isoformat().replace( '+00:00', 'Z' )
