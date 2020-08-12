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
        
    def testGetMessagesBetweenEpochs(self):
        '''
        Test get messages between given start and end epochs.
        '''
        start = 2
        end = 3
        params = { 'startEpoch': start, 'endEpoch': end }
        result = self.simulate_get( path, params = params )
        expected = [ msg for msg in self._testData if messages.epochNumAttr in msg and msg[messages.epochNumAttr] >= start and msg[messages.epochNumAttr] <= end ]
        testingUtils.checkMessages( self, result.json, expected )
    
        
        
    def testGetMessagesByInvalidEpoch(self):
        '''
        Test get bad request error with epoch number not an integer.
        '''
        params = { 'epoch': 'foo' }
        result = self.simulate_get( path, params = params )
        self.assertEqual( result.status_code, 400 )
        
    def testGetMessagesByProcesses(self):
        '''
        Test get messages by multiple source process ids.
        '''
        process = [ 'solarPlant1', 'weatherDivinity' ]
        params = { 'process': ','.join( process ) }
        result = self.simulate_get( path, params = params )
        expected = [ msg for msg in self._testData if msg[ messages.processAttr ] in process ]
        testingUtils.checkMessages( self, result.json, expected )
        
    def testGetOnlyWarningMessages(self):
        '''
        Test get only messages that contain warnings.
        '''
        params = { 'onlyWarnings': 'true' }
        result = self.simulate_get( path, params = params )
        expected = [ msg for msg in self._testData if messages.warningsAttr in msg ]
        testingUtils.checkMessages( self, result.json, expected )
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetAllMessages']
    unittest.main()