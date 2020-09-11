# -*- coding: utf-8 -*-
'''
Helper functions used with tests.
'''
import csv
import io

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
    '''
    Check by message id that the list of result simulations matches with the list of expected simulations.
    '''
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

def checkCsv( test, result: str, expected: csv.DictReader, delimiter = ';' ):
    result = io.StringIO( result, newline = '' )
    result = csv.DictReader( result, delimiter = ';' )
    resultHeaders = set( result.fieldnames )
    expectedHeaders = set( expected.fieldnames )
    test.assertEqual( resultHeaders, expectedHeaders, 'Result and expected should have the same headers.' )
    line = 1
    for expectedRow in expected:
        line += 1
        try:
            resultRow = next( result )
            
        except StopIteration:
            test.fail( f'No more rows in result but was expecting a row containing: {expectedRow}.' )
            
        test.assertEqual( resultRow, expectedRow, f'Result and expected rows do not match on line {line}.' )
        
    with( test.assertRaises( StopIteration, msg = 'Result has more rows than expected.' )):
        next( result )
        
def getTestDataResultFileName( testName, scenarioName, actual = False, fileType = 'json' ):
    result = 'result'
    if actual:
        result = 'actual_result'
    scenarioName = scenarioName.replace( ' ', '_' )
    return f'{testName}_{scenarioName}_{result}.{fileType}'
