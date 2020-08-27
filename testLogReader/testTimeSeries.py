'''
Created on 25.8.2020

@author: hylli
'''
import unittest
import pprint
import functools

from LogReader.db import messages
from LogReader.services import timeSeries
from testLogReader import dataManager, testingUtils

batteryMsgIds = [ 'battery1-1', 'battery2-1', 'battery1-2', 'battery2-2' ]
chargePercentageAttr = 'batteryState.chargePercentage'
batteryStateAttr = 'batteryState'
 
testScenarios = [ 
    { 'name': 'battery state from battery 1 and 2',
     'timeSeriesParams': [ 
         {'msgIds': batteryMsgIds,
         'attrs': [ batteryStateAttr ]}
     ],
     'testGetMessagesForNextEpoch': [[ 1, 2 ]],
     'testGetEpochData': '' },
    { 'name': 'charge percentage from battery 1 and 2',
     'timeSeriesParams': [ 
         {'msgIds': batteryMsgIds,
         'attrs': [ chargePercentageAttr ],}
     ],
     'testGetMessagesForNextEpoch': [[ 1, 2 ]],
     'testGetEpochData': '' }
]

def testWithAllScenarios( testName ):
    def decorator(test):
        @functools.wraps(test)
        def wrapper(testInstance):
            for scenario in testScenarios:
                timeSeries, expected = TestTimeSeries.getTestData( scenario, testName )
                if expected == None:
                    continue
                
                with testInstance.subTest( scenario = scenario['name'] ):
                    test( testInstance, timeSeries, expected )
                
        return wrapper
    return decorator
                
class TestTimeSeries(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls._testData = dataManager.readJsonFile( 'messages1.json' )


    def setUp(self):
        pass


    def tearDown(self):
        pass

    @classmethod
    def _getMessagesForIds(cls, msgIds ):
        return [ msg for msg in cls._testData if msg[messages.idAttr] in msgIds ]

    @testWithAllScenarios( 'testGetMessagesForNextEpoch' )
    def testGetMessagesForNextEpoch(self, timeSeries, expected ):
        for i in range( 0, len(expected)):
            tsMsgs = timeSeries._data[i]
            for epoch in expected[i]:
                expectedMsgs = [ msg for msg in tsMsgs.msgs if msg[messages.epochNumAttr] == epoch ] 
                nextEpoch = tsMsgs.getNextEpochNumber()
                self.assertEqual( nextEpoch, epoch ) 
                epochMsgs = tsMsgs.getNextEpochMsgs()
                testingUtils.checkMessages( self, epochMsgs, expectedMsgs )
        
            self.assertIsNone( tsMsgs.getNextEpochNumber() )    
            self.assertIsNone( tsMsgs.getNextEpochMsgs() )

    @testWithAllScenarios( 'testGetEpochData' )
    def testGetEpochData(self, timeSeries, expected):
        timeSeries._getEpochData()
        pprint.pprint( timeSeries._result )
    
    def _getTestData1(self):
        msgs = self._getMessagesForIds( batteryMsgIds )
        tsMsgs = timeSeries.TimeSeriesMessages( [ chargePercentageAttr ], msgs )
        return msgs, tsMsgs
    
    @classmethod
    def getTestData(cls, scenario, testName ):
        tsMsgsLst = [ timeSeries.TimeSeriesMessages( params['attrs'],  cls._getMessagesForIds( params['msgIds'] ) ) for params in scenario['timeSeriesParams'] ]   
        return timeSeries.TimeSeries( tsMsgsLst ), scenario.get(testName)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetMessagesForNextEpoch']
    unittest.main()