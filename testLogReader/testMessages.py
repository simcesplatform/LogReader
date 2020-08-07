# -*- coding: utf-8 -*-
'''
Created on 7.8.2020

@author: hylli
'''
import unittest

from testLogReader import dataManager
from builtins import classmethod

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
        pass


if __name__ == "__main__":
    unittest.main()