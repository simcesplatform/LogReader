# -*- coding: utf-8 -*
'''
Tests for get messages API
'''
import unittest

from LogReader.db import messages

from testLogReader import dataManager, testingUtils

# URL path for getting test messages
path = f'/simulations/{dataManager.testMsgSimId}/messages'

class TestMessagesApi( testingUtils.ApiTest ):
    
    @classmethod
    def setUpClass(cls):
        '''
        Adds the test message data to the db
        '''
        cls._testData = dataManager.insertTestMsgData()
        
    @classmethod
    def tearDownClass(cls):
        '''
        Removes the test message data from the db.
        '''
        dataManager.deleteTestMsgData()

    def testGetAllMessages(self):
        '''
        Test we can get all messages.
        '''
        result = self.simulate_get(  path )
        testingUtils.checkMessages( self, result.json, self._testData )
        
    def testGetMessagesSimulationNotFound(self):
        '''
        Check that a 404 response is received when getting messages with simulation id that does not exist.
        ''' 
        result = self.simulate_get( '/simulations/foo/messages' )
        self.assertEqual( result.status_code, 404 )
        
    def testGetMessagesByEpoch(self):
        '''
        Test get messages by epoch number.
        '''
        epoch = 1
        params = { 'epoch':  epoch }
        result = self.simulate_get( path, params  = params )
        self.assertEqual( result.status_code, 200 )
        expected = [ msg for msg in self._testData if msg.get( messages.epochNumAttr ) == epoch ]
        testingUtils.checkMessages( self, result.json, expected )
        
    def testGetMessagesByInvalidEpoch(self):
        '''
        Test get bad request error with epoch number not an integer.
        '''
        params = { 'epoch': 'foo' }
        result = self.simulate_get( path, params = params )
        self.assertEqual( result.status_code, 400 )

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetAllMessages']
    unittest.main()