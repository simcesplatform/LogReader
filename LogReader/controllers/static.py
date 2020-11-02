# -*- coding: utf-8 -*-
'''
Contains controller for delivering static files.
'''
import pathlib
from falcon.routing import StaticRoute

class StaticSite(object):
    '''
    Used to deliver static files for the user interface.
    '''

    def __init__(self, prefix ):
        '''
        Create static controller for the given url path.
        '''
        self._prefix = prefix
        # path to the directory were the ui files are located
        uiDir = str( pathlib.Path(__file__).parent.parent.parent.absolute() / 'ui' )
        # falcon's static route is used mainly to deliver the files.
        # it needs the url path prefix and the file directory
        self._route = StaticRoute( prefix, uiDir )
        
    def on_get(self, req, resp, file ):
        '''
        Return the given file.
        If file is empty string returns index.html.
        '''
        # otherwise just use falcon's static route except with empty file change request path to index.html
        if file == '':
            req.path = req.path +'index.html'
            
        self._route( req, resp )        