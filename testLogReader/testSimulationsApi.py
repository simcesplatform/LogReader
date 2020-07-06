# -*- coding: utf-8 -*-
'''
Tests for simulation api endpoints.
Uses falcons testing tools which simulate HTTP requests. 
'''
import unittest

from falcon import testing

from LogReader.app import api

from testLogReader import dataManager, testingUtils

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
        testingUtils.checkSimulations(self, result.json, self._testData )
        
    def testGetSimulationsAfterDate(self):
        '''
        Test get simulations after given date.
        '''
        params = { 'fromDate': '2020-06-03T10:01:52.345Z' }
        result = self.simulate_get( '/simulations', params = params )
        self.assertEqual( result.status_code, 200 )
        # we should haven gotten the latter two simulations.
        testingUtils.checkSimulations(self, result.json, self._testData[1:] )
        
    def testGetSimulationsBeforeDate(self):
        '''
        Test get simulations started on or before given date.
        '''
        params = { 'toDate': '2020-06-03T10:01:52.345Z' }
        result = self.simulate_get( '/simulations', params = params )
        self.assertEqual( result.status_code, 200 )
        # we should get the first two simulations
        testingUtils.checkSimulations(self, result.json, self._testData[:2] )
        
    def testGetSimulationsBetweenDates(self):
        '''
        Test get simulations executed between given dates.
        '''
        params = { 'fromDate': '2020-06-03T09:01:52.345Z',
                  'toDate': '2020-06-03T11:01:52.345Z'
               }
        result = self.simulate_get( '/simulations', params = params )
        self.assertEqual( result.status_code, 200 )
        # we should get only the second simulation.
        testingUtils.checkSimulations(self, result.json, self._testData[1:2] )
        
    def testGetSimulationsWithBadDate(self):
        '''
        Check that we get a HTTP bad request response with an invalid date.
        '''
        params = { 'toDate': '2020-06-0310:01:52.345Z' }
        result = self.simulate_get( '/simulations', params = params )
        self.assertEqual( result.status_code, 400 )
    
if __name__ == "__main__":
    # execute tests if main file.
    unittest.main()