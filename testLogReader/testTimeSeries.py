'''
Created on 25.8.2020

@author: hylli
'''
import unittest
import pprint
import functools
import copy

from LogReader.db import messages
from LogReader.services import timeSeries
from testLogReader import dataManager, testingUtils

batteryMsgIds = [ 'battery1-1', 'battery2-1', 'battery1-2', 'battery2-2' ]
solarPlantOkMsgIds = [ 'solarPlant1-1', 'solarPlant1-2' ]
solarPlantMsgIds = solarPlantOkMsgIds +[ 'solarPlant1-3' ]
battery3MsgIds = [ 'battery3-1', 'battery3-2' ]
battery_1_3MsgIds = [ 'battery1-1', 'battery3-1', 'battery1-2', 'battery3-2' ]
batteryMsgIdsMissing = [ 'battery1-1', 'battery1-2', 'battery2-2' ]
batteryMsgIdsMissing2 = [ 'battery1-1', 'battery2-1', 'battery2-2' ]
chargePercentageAttr = 'batteryState.chargePercentage'
capacityAttr = 'batteryState.capacity'
batteryStateAttr = 'batteryState'
realPowerAttr = 'RealPower'
reactivePowerAttr = 'ReactivePower'
 
testScenarios = [ 
    { 'name': 'battery state from battery 1 and 2',
     'timeSeriesParams': [ 
         {'msgIds': batteryMsgIds,
         'attrs': [ batteryStateAttr ]}
     ],
     'testGetMessagesForNextEpoch': [[ 1, 2 ]],
     'testGetEpochData': { 'fileType': 'json' },
     'testCreateTimeSeries': { 'fileType': 'json' },
     'testCreateCsvHeaders': { 'fileType': 'csv' },
     'testCreateCsv': { 'fileType': 'csv' } },
    { 'name': 'real power from solar plant 1',
     'timeSeriesParams': [ 
         {'msgIds': solarPlantOkMsgIds,
         'attrs': [ realPowerAttr ]}
     ],
     'testGetMessagesForNextEpoch': [[ 1, 2 ]],
     'testGetEpochData': { 'fileType': 'json' },
     'testCreateTimeSeries': { 'fileType': 'json'  },
     'testCreateCsvHeaders': { 'fileType': 'csv' },
     'testCreateCsv': { 'fileType': 'csv' } },
    { 'name': 'real and reactive power from solar plant 1',
     'timeSeriesParams': [ 
         {'msgIds': solarPlantOkMsgIds,
         'attrs': [ realPowerAttr, reactivePowerAttr ]}
     ],
     'testGetMessagesForNextEpoch': [[ 1, 2 ]],
     'testGetEpochData': { 'fileType': 'json' },
     'testCreateTimeSeries': { 'fileType': 'json' },
     'testCreateCsvHeaders': { 'fileType': 'csv' },
     'testCreateCsv': { 'fileType': 'csv' }},
    { 'name': 'charge percentage from battery 1 and 2',
     'timeSeriesParams': [ 
         {'msgIds': batteryMsgIds,
         'attrs': [ chargePercentageAttr ],}
     ],
     'testGetMessagesForNextEpoch': [[ 1, 2 ]],
     'testGetEpochData': { 'fileType': 'json' },
    'testCreateTimeSeries': { 'fileType': 'json' },
     'testCreateCsvHeaders': { 'fileType': 'csv' },
     'testCreateCsv': { 'fileType': 'csv' } },
    { 'name': 'missing attributes from battery 3',
     'timeSeriesParams': [ 
         {'msgIds': battery3MsgIds,
         'attrs': [ chargePercentageAttr, capacityAttr ],}
     ],
     'testGetMessagesForNextEpoch': [[ 1, 2 ]],
     'testGetEpochData': { 'fileType': 'json' },
    'testCreateTimeSeries': { 'fileType': 'json' },
     'testCreateCsvHeaders': { 'fileType': 'csv' },
     'testCreateCsv': { 'fileType': 'csv' } },
    { 'name': 'battery state from battery 1 and 2 with missing data',
     'timeSeriesParams': [ 
         {'msgIds': batteryMsgIdsMissing,
         'attrs': [ batteryStateAttr ]}
     ],
     'testGetMessagesForNextEpoch': [[ 1, 2 ]],
     'testGetEpochData': { 'fileType': 'json' },
     'testCreateTimeSeries': { 'fileType': 'json' },
     'testCreateCsvHeaders': { 'fileType': 'csv' },
     'testCreateCsv': { 'fileType': 'csv', } },
    { 'name': 'battery state from battery 1 and 2 with missing data 2',
     'timeSeriesParams': [ 
         {'msgIds': batteryMsgIdsMissing2,
         'attrs': [ batteryStateAttr ]}
     ],
     'testGetMessagesForNextEpoch': [[ 1, 2 ]],
     'testGetEpochData': { 'fileType': 'json' },
     'testCreateTimeSeries': { 'fileType': 'json' },
     'testCreateCsvHeaders': { 'fileType': 'csv' },
     'testCreateCsv': { 'fileType': 'csv', } },
    { 'name': 'different time indexes',
     'timeSeriesParams': [ 
         {'msgIds': battery_1_3MsgIds,
         'attrs': [ chargePercentageAttr ],}
     ],
     'testGetMessagesForNextEpoch': [[ 1, 2 ]],
     'testGetEpochData': { 'fileType': 'json' },
    'testCreateTimeSeries': { 'fileType': 'json' },
     'testCreateCsvHeaders': { 'fileType': 'csv' },
     'testCreateCsv': { 'fileType': 'csv' } }
]

def testWithAllScenarios( testName ):
    def decorator(test):
        @functools.wraps(test)
        def wrapper(testInstance):
            testInstance._testName = testName
            testInstance._results = {}
            for scenario in testScenarios:
                testInstance._skipAsserts = False
                timeSeries, expected = testInstance.getTestData( scenario )
                if expected == None:
                    continue
                    
                testInstance._scenarioName = scenario['name']
                with testInstance.subTest( scenario = scenario['name'] ):
                    test( testInstance, timeSeries, expected )
                        
        return wrapper
    return decorator

class TestTimeSeries(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls._testData = dataManager.readFile( 'messages1.json' )


    def setUp(self):
        pass


    def tearDown(self):
        for scenarioName in self._results:
            fileName = testingUtils.getTestDataResultFileName( self._testName, scenarioName, True, self._fileType )
            dataManager.writeFile( fileName, self._results[scenarioName] )

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
        results = { 'result': [], 'epochResult': [] }
        self._results[self._scenarioName] = results
        index = 0
        while timeSeries._findNextEpoch(): 
            timeSeries._getEpochData()
            #pprint.pprint( timeSeries._result )
            #pprint.pprint( timeSeries._epochResult )
            results['result'].append( copy.deepcopy(timeSeries._result) )
            results['epochResult'].append( copy.deepcopy(timeSeries._epochResult) )
            if not self._skipAsserts:
                self.assertEqual( timeSeries._result, expected['result'][index] )
                self.assertEqual( timeSeries._epochResult, expected['epochResult'][index] )
            index += 1
             
    
    @testWithAllScenarios( 'testCreateTimeSeries' )        
    def testCreateTimeSeries(self, timeSeries, expected ):
        timeSeries.createTimeSeries()
        self._results[self._scenarioName] = timeSeries._result
        if not self._skipAsserts:
            self.assertEqual( timeSeries._result, expected )
    
    @testWithAllScenarios( 'testCreateCsvHeaders' )        
    def testCreateCsvHeaders(self, timeSeriesObj, expected ):
        timeSeriesObj.createTimeSeries()
        csv = timeSeries.TimeSeriesCsvConverter( timeSeriesObj.getResult() )
        csv._createHeaders()
        result = csv.getTarget().getvalue()
        self._results[self._scenarioName] = result
        if not self._skipAsserts:
            testingUtils.checkCsv( self, result, expected )
        
    @testWithAllScenarios( 'testCreateCsv' )        
    def testCreateCsv(self, timeSeriesObj, expected ):
        timeSeriesObj.createTimeSeries()
        csv = timeSeries.TimeSeriesCsvConverter( timeSeriesObj.getResult() )
        csv.createCsv()
        result = csv.getTarget().getvalue()
        self._results[self._scenarioName] = result
        if not self._skipAsserts:
            testingUtils.checkCsv( self, result, expected )

    def _getTestData1(self):
        msgs = self._getMessagesForIds( batteryMsgIds )
        tsMsgs = timeSeries.TimeSeriesMessages( [ chargePercentageAttr ], msgs )
        return msgs, tsMsgs
    
    def getTestData(self, scenario):
        tsMsgsLst = [ timeSeries.TimeSeriesMessages( params['attrs'],  self._getMessagesForIds( params['msgIds'] ) ) for params in scenario['timeSeriesParams'] ]
        epochs = set()
        for tsMsgs in tsMsgsLst:
            epochs.update( [ msg[messages.epochNumAttr] for msg in tsMsgs.msgs ] )
            
        epochStartTimes = { msg[ messages.epochNumAttr ]: msg[ messages.epochStartAttr ] for msg in self._testData if msg[ messages.topicAttr ] == 'Epoch' and msg[ messages.epochNumAttr ] in epochs }
                
        expected = scenario.get(self._testName)
        if expected != None and type( expected ) == dict and 'fileType' in expected:
            fileType = expected['fileType']
            self._fileType = fileType
            if not expected.get( 'noResult' ):
                fileName = testingUtils.getTestDataResultFileName( self._testName, scenario['name'], False, fileType )
                expected = dataManager.readFile( fileName )
                
            else:
                self._skipAsserts = True
                
        return timeSeries.TimeSeries( tsMsgsLst, epochStartTimes ), expected
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetMessagesForNextEpoch']
    unittest.main()