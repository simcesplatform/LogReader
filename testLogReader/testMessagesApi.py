# -*- coding: utf-8 -*
'''
Tests for get messages API
'''
import unittest


from testLogReader import dataManager, testingUtils

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
        result = self.simulate_get( f'/simulations/{dataManager.testMsgSimId}/messages' )
        self.assertEqual( len( result.json ), len( self._testData ) )
        
    def testGetMessagesSimulationNotFound(self):
        '''
        Check that a 404 response is received when getting messages with simulation id that does not exist.
        ''' 
        result = self.simulate_get( '/simulations/foo/messages' )
        self.assertEqual( result.status_code, 404 )

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetAllMessages']
    unittest.main()