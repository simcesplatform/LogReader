'''
Created on 25.8.2020

@author: hylli
'''
import unittest
import pprint

from LogReader.db import messages
from LogReader.services import timeSeries
from testLogReader import dataManager, testingUtils

batteryMsgIds = [ 'battery1-1', 'battery2-1', 'battery1-2', 'battery2-2' ]
chargePercentageAttr = 'batteryState.chargePercentage'

class Test(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls._testData = dataManager.readJsonFile( 'messages1.json' )


    def setUp(self):
        pass


    def tearDown(self):
        pass

    def _getMessagesForIds(self, msgIds ):
        return [ msg for msg in self._testData if msg[messages.idAttr] in msgIds ]

    def testGetMessagesForNextEpoch(self):
        msgs, tsMsgs = self._getTestData1()
        expected = [ msgs[:2], msgs[2:] ]
        for item in expected:
            nextEpoch = tsMsgs.getNextEpochNumber()
            expectedEpoch = item[0][messages.epochNumAttr]
            self.assertEqual( nextEpoch, expectedEpoch ) 
            epochMsgs = tsMsgs.getNextEpochMsgs()
            testingUtils.checkMessages( self, epochMsgs, item )
        
        self.assertIsNone( tsMsgs.getNextEpochNumber() )    
        self.assertIsNone( tsMsgs.getNextEpochMsgs() )

    def testGetEpochData(self):
        msgs, tsMsgs = self._getTestData1()
        ts = timeSeries.TimeSeries( [ tsMsgs ] )
        ts._getEpochData()
        #pprint.pprint( ts._result )
    
    def _getTestData1(self):
        msgs = self._getMessagesForIds( batteryMsgIds )
        tsMsgs = timeSeries.TimeSeriesMessages( [ chargePercentageAttr ], msgs )
        return msgs, tsMsgs
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetMessagesForNextEpoch']
    unittest.main()