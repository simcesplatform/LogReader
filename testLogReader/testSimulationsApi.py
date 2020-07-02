# -*- coding: utf-8 -*-
'''
Tests for simulation api endpoints.
Uses falcons testing tools which simulate HTTP requests. 
'''
import unittest

from falcon import testing

from LogReader.app import api

from testLogReader import dataManager

class ApiTest(testing.TestCase):
    '''
    Super class for api tests which gets the falcon api instance.
    '''

    def setUp(self):
        super(ApiTest, self).setUp()
        self.app = api

class TestSimApi( ApiTest ):
    '''
    The actual simulation API tests.
    '''
    
    @classmethod
    def setUpClass(cls):
        '''
        Insert simulation test data before the tests are executed.
        '''
        # store test data for use in tests
        cls._testData = dataManager.insertTestSimData()
        
    @classmethod
    def tearDownClass(cls):
        '''
        Remove test data after tests are complete.
        '''
        dataManager.deleteTestSimData()
    
    def testGetAll(self):
        '''
        Test get all simulations.
        '''
        result = self.simulate_get( '/simulations' )
        self.assertEqual( len( result.json ), len( self._testData ) )
        


if __name__ == "__main__":
    # execute tests if main file.
    unittest.main()