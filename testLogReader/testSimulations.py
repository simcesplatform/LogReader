# -*- coding: utf-8 -*-
'''
Tests for the simulations db module.
'''
import unittest

from LogReader.db import simulations
from testLogReader import dataManager

class SimTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        '''
        Insert test data before the test methods are executed.
        '''
        # save test data for use in the tests.
        cls._testData = dataManager.insertTestSimData()
    
    @classmethod
    def tearDownClass(cls):
        '''
        Removes test data after tests have been executed.
        '''
        dataManager.deleteTestSimData()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGetAllSimulations(self):
        '''
        Test that all simulations can be fetched correctly.
        '''
        results = simulations.getSimulations()
        self.assertEqual( len( results ), len( self._testData ), 'should have received all simulations.' )
    
    def testGetSimulationsByDate(self):
        pass 

if __name__ == "__main__":
    # if main file execute tests
    unittest.main()