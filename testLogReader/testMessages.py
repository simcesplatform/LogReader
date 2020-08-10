# -*- coding: utf-8 -*-
'''
Tests for getting messages from the database.
'''

import unittest
from builtins import classmethod

from testLogReader import dataManager
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
        self.assertEqual( len( result ), len( self._testData ) )
        
    def testGetMessagesSimulationNotFound(self):
        '''
        Test that we get None with id of a simulation that does not exist.
        '''
        result = messages.getMessages( 'foo' )
        self.assertIsNone( result )

if __name__ == "__main__":
    unittest.main()