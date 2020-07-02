# -*- coding: utf-8 -*-
'''
Initialises logging for the application.
'''

import logging
import os

level = logging.INFO
if os.environ.get( 'LOGREADER_DEBUG' ) == 'true':
    level = logging.DEBUG
    
logging.basicConfig( level = level )
# pakcage logger for possible package level logging configuration
log = logging.getLogger( __name__ )
log.debug( 'Debug logging is on.' )