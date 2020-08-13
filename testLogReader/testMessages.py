# -*- coding: utf-8 -*-
'''
Tests for getting messages from the database.
'''

import unittest
from builtins import classmethod

import dateutil

from testLogReader import dataManager, testingUtils
from LogReader.db import messages

class TestMessages(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls._testData = dataManager.insertTestMsgData()
    
    @classmethod
    def tearDownClass(cls):
        dataManager.deleteTestMsgData()

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testGetAllMessages(self):
        '''
        Test that we can get all messages.
        '''
        result = messages.getMessages( dataManager.testMsgSimId )
        testingUtils.checkMessages( self, result, self._testData )
        
    def testGetMessagesSimulationNotFound(self):
        '''
        Test that we get None with id of a simulation that does not exist.
        '''
        result = messages.getMessages( 'foo' )
        self.assertIsNone( result )
        
    def testGetMessagesByEpoch(self):
        '''
        Test get messages by epoch number.
        '''
        epoch = 1
        result = messages.getMessages( dataManager.testMsgSimId, epoch = epoch )
        expected = [ msg for msg in self._testData if msg.get( messages.epochNumAttr ) == epoch ]
        testingUtils.checkMessages( self, result, expected )
        
    def testGetMessagesByStartEpoch(self):
        '''
        test get messages starting from given epoch.
        '''
        startEpoch = 2
        result = messages.getMessages( dataManager.testMsgSimId, startEpoch = startEpoch )
        expected = [ msg for msg in self._testData if messages.epochNumAttr in msg and msg[messages.epochNumAttr] >= startEpoch ]
        testingUtils.checkMessages( self, result, expected )
        
    def testGetMessagesByEndEpoch(self):
        '''
        test get messages ending at given epoch.
        '''
        endEpoch = 2
        result = messages.getMessages( dataManager.testMsgSimId, endEpoch = endEpoch )
        expected = [ msg for msg in self._testData if messages.epochNumAttr in msg and msg[messages.epochNumAttr] <= endEpoch ]
        testingUtils.checkMessages( self, result, expected )
        
    def testGetMessagesBetweenEpochs(self):
        '''
        test get messages between given epochs
        '''
        startEpoch = 2
        endEpoch = 3
        result = messages.getMessages( dataManager.testMsgSimId, startEpoch = startEpoch, endEpoch = endEpoch )
        expected = [ msg for msg in self._testData if messages.epochNumAttr in msg and msg[messages.epochNumAttr] >= startEpoch and msg[messages.epochNumAttr] <= endEpoch ]
        testingUtils.checkMessages( self, result, expected )
    
    def testGetMessagesByProcess(self):
        '''
        Test get messages by source process id.
        '''
        process = [ 'solarPlant1' ]
        result = messages.getMessages( dataManager.testMsgSimId, process = process )
        expected = [ msg for msg in self._testData if msg[ messages.processAttr ] in process ]
        testingUtils.checkMessages( self, result, expected )
        
    def testGetMessagesByProcesses(self):
        '''
        Test get messages by multiple source process ids.
        '''
        process = [ 'solarPlant1', 'weatherDivinity' ]
        result = messages.getMessages( dataManager.testMsgSimId, process = process )
        expected = [ msg for msg in self._testData if msg[ messages.processAttr ] in process ]
        testingUtils.checkMessages( self, result, expected )
        
    def testGetOnlyWarningMessages(self):
        '''
        Test get only messages that contain warnings.
        '''
        result = messages.getMessages( dataManager.testMsgSimId, onlyWarnings = True )
        expected = [ msg for msg in self._testData if messages.warningsAttr in msg ]
        testingUtils.checkMessages( self, result, expected )        
        
    def testGetEpochsForSimDates(self):
        '''
        Test the _getEpochForsimDates helper method used when getting messages by simulation dates.
        '''
        fromSimDate = dateutil.parser.isoparse( "2020-06-03T14:00:00Z" ) # start of epoch 2
        toSimDate = dateutil.parser.isoparse( "2020-06-03T16:00:00Z" ) # end of epoch 3
        result = messages._getEpochsForSimDates( dataManager.testMsgSimId, fromSimDate = fromSimDate )
        self.assertEqual( result, ( 2, None ))
        result = messages._getEpochsForSimDates( dataManager.testMsgSimId, toSimDate = toSimDate )
        self.assertEqual( result, ( None, 3 ))
        result = messages._getEpochsForSimDates( dataManager.testMsgSimId, fromSimDate = fromSimDate, toSimDate = toSimDate )
        self.assertEqual( result, ( 2, 3 ))
        fromSimDate = dateutil.parser.isoparse( "2020-06-03T17:00:00Z" ) #  end of last epoch, no epochs
        toSimDate = dateutil.parser.isoparse( "2020-06-03T13:00:00Z" ) # Start of first epoch, should not get any epochs 
        result = messages._getEpochsForSimDates( dataManager.testMsgSimId, fromSimDate = fromSimDate )
        self.assertEqual( result, ( None, None ))
        result = messages._getEpochsForSimDates( dataManager.testMsgSimId, toSimDate = toSimDate )
        self.assertEqual( result, ( None, None ))
        
    def testGetMessagesByFromSimDate( self ):
        '''
        Get messages on and after epoch which includes the given simulation date.
        '''
        fromSimDate = dateutil.parser.isoparse( "2020-06-03T14:00:00Z" )
        result = messages.getMessages( dataManager.testMsgSimId, fromSimDate = fromSimDate )
        # we expect messages starting from epoch 2
        startEpoch = 2
        expected = [ msg for msg in self._testData if messages.epochNumAttr in msg and msg[messages.epochNumAttr] >= startEpoch ]
        testingUtils.checkMessages( self, result, expected )
        
    def testGetMessagesByToSimDate( self ):
        '''
        Get messages on and before epoch which includes the given simulation date.
        '''
        toSimDate = dateutil.parser.isoparse( "2020-06-03T15:00:00Z" )
        result = messages.getMessages( dataManager.testMsgSimId, toSimDate = toSimDate )
        # we expect messages ending with   epoch 2
        endEpoch = 2
        expected = [ msg for msg in self._testData if messages.epochNumAttr in msg and msg[messages.epochNumAttr] <= endEpoch ]
        testingUtils.checkMessages( self, result, expected )
        
    def testGetMessagesBetweenSimDate( self ):
        '''
        Get messages between epochs  that contain the given simulation dates.
        '''
        fromSimDate = dateutil.parser.isoparse( "2020-06-03T14:00:00Z" )
        toSimDate = dateutil.parser.isoparse( "2020-06-03T16:00:00Z" )
        result = messages.getMessages( dataManager.testMsgSimId, fromSimDate = fromSimDate, toSimDate = toSimDate )
        # we expect messages starting from epoch 2 and ending with epoch 3
        startEpoch = 2
        endEpoch = 3
        expected = [ msg for msg in self._testData if messages.epochNumAttr in msg and msg[messages.epochNumAttr] >= startEpoch and msg[messages.epochNumAttr] <= endEpoch ]
        testingUtils.checkMessages( self, result, expected )
        
if __name__ == "__main__":
    unittest.main()