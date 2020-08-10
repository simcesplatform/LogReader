# -*- coding: utf-8 -*-
'''
Helper functions used with tests.
'''

from falcon import testing

from LogReader.app import api
from LogReader.db.simulations import simIdAttr

class ApiTest(testing.TestCase):
    '''
    Super class for api tests which gets the falcon api instance.
    '''

    def setUp(self):
        super(ApiTest, self).setUp()
        self.app = api

def checkSimulations( test, resultSims, expectedSims ):
    '''
    Check by simulation id that results and expected simulations are the same.
    test (unittest.TestCase) Test case which uses this so we can use its assert methods.
    resultSims (list): List of simulations.
    expectedSims (list): List of simulations.
    '''
    checkItemsById( test, simIdAttr, resultSims, expectedSims )
    
def checkMessages( test, resultMsgs, expectedMsgs ):
    checkItemsById( test, 'MessageId', resultMsgs, expectedMsgs )
    
def checkItemsById( test, idAttr, result, expected ):
    '''
    Check by id that results and expected are the same.
    test (unittest.TestCase) Test case which uses this so we can use its assert methods.
    idAttr (str): Name of attribute containing the id of the items.
    result (list): List of items.
    expected (list): List of expected items.
    '''
    # get ids of results and expected and check they contain the same.
    ids = [ item[ idAttr ] for item in result ]
    expectedIds = [ item[ idAttr ] for item in expected ]
    test.assertCountEqual( ids, expectedIds, 'Did not get the expected items.' )
