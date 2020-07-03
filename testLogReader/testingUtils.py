# -*- coding: utf-8 -*-
'''
Helper functions used with tests.
'''

from LogReader.db.simulations import simIdAttr

def checkSimulations( test, resultSims, expectedSims ):
    '''
    Check by simulation id that results and expected simulations are the same.
    test (unittest.TestCase) Test case which uses this so we can use its assert methods.
    resultSims (list): List of simulations.
    expectedSims (list): List of simulations.
    '''
    # get simulation ids of results and expected and check they contain the same.
    simIds = [ sim[ simIdAttr ] for sim in resultSims ]
    expectedIds = [ sim[ simIdAttr ] for sim in expectedSims ]
    test.assertCountEqual( simIds, expectedIds, 'Did not get the expected simulations.' )
