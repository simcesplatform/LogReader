# -*- coding: utf-8 -*-
'''
Tests for getting messages from the database.
'''

import unittest
from builtins import classmethod

from testLogReader import dataManager, testingUtils
from LogReader.db import messages

class TestMessages(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls._testData = dataManager.insertTestMsgData()
    
    @classmethod
    def tearDownClass(cls):
        dataManager.deleteTestMsgData()

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testGetAllMessages(self):
        '''
        Test that we can get all messages.
        '''
        result = messages.getMessages( dataManager.testMsgSimId )
        testingUtils.checkMessages( self, result, self._testData )
        
    def testGetMessagesSimulationNotFound(self):
        '''
        Test that we get None with id of a simulation that does not exist.
        '''
        result = messages.getMessages( 'foo' )
        self.assertIsNone( result )
        
    def testGetMessagesByEpoch(self):
        '''
        Test get messages by epoch number.
        '''
        epoch = 1
        result = messages.getMessages( dataManager.testMsgSimId, epoch = epoch )
        expected = [ msg for msg in self._testData if msg.get( messages.epochNumAttr ) == epoch ]
        testingUtils.checkMessages( self, result, expected )
        

if __name__ == "__main__":
    unittest.main()