# -*- coding: utf-8 -*-
'''
The main file which sets up the falcon framework based web application.
If this file  is executed as a main file, the application is started with the waitress WSGI server.
The WSGI application is available in LogReader.app.api
'''

import os
from functools import partial
import json
import logging

import falcon
from paste.translogger import TransLogger
import waitress

from LogReader.controllers.simulations import SimController
from LogReader.controllers.messages import MsgController
from LogReader.controllers.timeSeries import TimeSeriesController
from LogReader.controllers.static import StaticSite
from LogReader.db import simulations, messages
from LogReader import utils
import LogReader

# log for this module
log = logging.getLogger( __name__ )

# configure falcon to automatically convert datetime objects in to JSON when they are a part of the response
# falcon uses the default python json.dumps method which we will still use but with some parameters preset
# namely we give our own function for processing objects (datetime) that the default implementation cannot process
jsonHandler = falcon.media.JSONHandler(
    dumps = partial(
        json.dumps, default = utils.jsonSerializeDate,
        ensure_ascii=False, sort_keys=True
        )
    )

extra_handlers = {
    'application/json': jsonHandler,
}

api = falcon.API()
api.resp_options.media_handlers.update(extra_handlers)

# Add route for getting simulations
# simController is given the module used to get simulations from the db
simController = SimController( simulations )
api.add_route( '/simulations', simController, suffix = 'simulations' )
# add route for getting simulation by id.
api.add_route( '/simulations/{simId}', simController, suffix = 'simulation' )
# Add route for getting messages for simulation
# Give the messages controller the messages db module as the source for messages.
msgController = MsgController( messages )
api.add_route( '/simulations/{simId}/messages', msgController, suffix = 'messages' )
api.add_route( '/simulations/{simId}/messages/invalid', msgController, suffix = 'invalid_messages' )
timeSeriesController = TimeSeriesController( messages )
api.add_route( '/simulations/{simId}/timeseries', timeSeriesController )
# add route for the user interface consisting of static files
staticPrefix = '/' # ui available from the root path
static = StaticSite( staticPrefix ) # use the static controller for delivering the files.
# note works only on one level e.g. /foo/bar.html does not work.
api.add_route( staticPrefix +'{file}', static )

if __name__ == '__main__':
    # this is main file launch the application
    # get listen ip and port from environment variables or use defaults
    host = os.environ.get( 'LOGREADER_HOST', '*' )
    port = os.environ.get( 'LOGREADER_PORT', 8080 )
    log.info( f'Starting LogReader. Listening on {host}:{port}.' )

    # start the waitress server using Translogger to get logging information about each connection attempt
    waitress.serve(
        app=TransLogger(api),
        host=host,
        port=port
    )
