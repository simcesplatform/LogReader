# -*- coding: utf-8 -*-
'''
Some tests for the application when it is run with a real WSGI server.
'''
import os
import unittest
import threading
import time

import waitress
import requests

from testLogReader import dataManager
from LogReader.app import api

class ServerThread(threading.Thread):
    '''
    A Thread subclass for launching the application with waitress.
    Inspired by https://gist.githubusercontent.com/miohtama/1f716f0d6aa2a9d05406/raw/65ef485d134ae1c3f320675ab485c51c2c4e1843/webserver.py
    '''
    
    def __init__(self, app, port ):
        '''
        Initialise with the WSGI app to be run with waitress and the TCP port number to be used.
        '''
        threading.Thread.__init__(self)
        self._app = app
        self._port = port
        # mark as daemon so that when the tests are done in main thread this thread is terminated
        # there is no other way to tell waitress to stop.
        self.daemon = True
        
    def run(self):
        '''
        Launch the app with waitress.
        '''
        try:
            waitress.serve(self._app, host='127.0.0.1', port=self._port, log_socket_errors=False, clear_untrusted_proxy_headers = True, _quiet=True)
            
        except Exception as e:
            # We are a background thread so we have problems to interrupt tests in the case of error. Try spit out something to the console.
            import traceback
            traceback.print_exc()
            
class TestWebServer(unittest.TestCase):
    '''
    Tests for the running server.
    '''
    
    @classmethod
    def setUpClass(cls):
        '''
        Launch the server and insert test data.
        '''
        cls._port = os.environ.get( 'LOGREADER_PORT', 8080 ) 
        cls._server = ServerThread( api, cls._port )
        cls._server.start() 
        cls._testData = dataManager.insertTestSimData()
        # try to make sure that server is up by sleeping
        # could also try to just make http requests until the server responds.
        time.sleep( 1 )

    @classmethod
    def tearDownClass(cls):
        '''
        Remove test data when tests done.
        '''
        dataManager.deleteTestSimData() 
        
    def testGetSimulations(self):
        result = requests.get( f'http://localhost:{self._port}/simulations' )
        self.assertEqual( result.status_code, 200, 'Incorrect response status.' )
        self.assertEqual( len( result.json() ), len( self._testData ), 'Should get all simulations.' )


if __name__ == "__main__":
    # execute tests
    unittest.main()