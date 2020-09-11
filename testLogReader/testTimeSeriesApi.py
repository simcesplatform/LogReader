'''
Created on 10.9.2020

@author: hylli
'''
import unittest
from testLogReader import dataManager, testingUtils

path = f'/simulations/{dataManager.testMsgSimId}/timeseries'

scenarios = [
    { 'name': 'battery state for battery 1',
     'query': { 'attrs': 'batteryState',
               'process': 'battery1', 
               'topic': 'energy.storage.state' },
     'status': 200 },
    { 'name': 'missing attrs parameter',
     'query': { 
               'process': 'battery1', 
               'topic': 'energy.storage.state' },
     'status': 400 },
    { 'name': 'battery charge for battery 1',
     'query': { 'attrs': 'batteryState.chargePercentage',
               'process': 'battery1', 
               'topic': 'energy.storage.state' },
     'status': 200 },
    { 'name': 'battery state for battery 1 and 2',
     'query': { 'attrs': 'batteryState',
               'process': 'battery1,battery2', 
               'topic': 'energy.storage.state' },
     'status': 200 },
    { 'name': 'battery state for battery 1 with start epoch',
     'query': { 'attrs': 'batteryState',
               'startEpoch': '2',
               'process': 'battery1', 
               'topic': 'energy.storage.state' },
     'status': 200 },
    { 'name': 'battery state for battery 1 with end epoch',
     'query': { 'attrs': 'batteryState',
               'endEpoch': '1',
               'process': 'battery1', 
               'topic': 'energy.storage.state' },
     'status': 200 },
    { 'name': 'battery state for battery 1 with epoch',
     'query': { 'attrs': 'batteryState',
               'epoch': '2',
               'process': 'battery1', 
               'topic': 'energy.storage.state' },
     'status': 200 },
    { 'name': 'battery state for battery 1 with from simdate',
     'query': { 'attrs': 'batteryState',
               'fromSimDate': '2020-06-03T14:00:00Z',
               'process': 'battery1', 
               'topic': 'energy.storage.state' },
     'status': 200 },
    { 'name': 'battery state for battery 1 with to simdate',
     'query': { 'attrs': 'batteryState',
               'toSimDate': '2020-06-03T14:00:00Z',
               'process': 'battery1', 
               'topic': 'energy.storage.state' },
     'status': 200 },
    { 'name': 'no messages',
     'query': { 'attrs': 'batteryState',
               'epoch': '3',
               'process': 'battery1', 
               'topic': 'energy.storage.state' },
     'status': 200 }
    ]

class TestTimeSeriesApi( testingUtils.ApiTest ):
    
    @classmethod
    def setUpClass(cls):
        '''
        Adds the test message data to the db
        '''
        cls._testData = dataManager.insertTestMsgData()
        
    @classmethod
    def tearDownClass(cls):
        '''
        Removes the test message data from the db.
        '''
        dataManager.deleteTestMsgData()
        
    def testApiWithScenarios(self):
        for scenario in scenarios:
            for dataFormat in [ 'json', 'csv' ]:
                with self.subTest( scenario = scenario['name' ], format = dataFormat ):
                    self._checkScenario( scenario, dataFormat )
                    
    def _checkScenario(self, scenario, dataFormat ):
        params = dict( scenario['query'] )
        params['format'] = dataFormat
        result = self.simulate_get( path, params = params )
        self.assertEqual( result.status_code, scenario['status'], 'Did not get the expected HTTP status code.' )
        if result.status_code != 200 or scenario['status'] != 200:
            return
        
        testName = 'testTimeSeriesApi'
        actualResultName = testingUtils.getTestDataResultFileName( testName, scenario['name'], True, dataFormat )
        if dataFormat == 'json':
            resultData = result.json
            
        elif dataFormat == 'csv':
            resultData = result.text
            
        dataManager.writeFile( actualResultName, resultData )
        resultName = testingUtils.getTestDataResultFileName( testName, scenario['name'], False, dataFormat )
        expected = dataManager.readFile( resultName )
        if dataFormat == 'json':
            self.assertEqual( resultData, expected )
            
        elif dataFormat == 'csv':
            testingUtils.checkCsv( self, resultData, expected )
            
    def testSimulationNotFound(self):
        result = self.simulate_get( '/simulations/foo/timeseries', params = { 'attrs': 'batteryState', 'topic': 'energy.storage.state' })
        self.assertEqual( result.status_code, 404, 'Got unexpected status code.' )
        
if __name__ == "__main__":
    unittest.main()