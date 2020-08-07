# -*- coding: utf-8 -*-
'''
Code for managing test data i.e. inserting and removing it from the database.
If run as the main file will insert the test data to the db: python -m testLogReader.dataManager
The parameter -d can be used to remove the test data: python -m testLogReader.dataManager -d
'''

import sys
import json
from bson import json_util
import pathlib

from LogReader.db import db, simulations, messages

# the mongodb collection where simulations are stored.
simCollection = db[simulations.simCollection]
# location of json files containing test data.
testDataDir = pathlib.Path(__file__).parent.absolute() / 'data'

# id of simulation for which there are test messages.
testMsgSimId = '2020-06-03T04:01:52.345Z'

def insertDataFromFile( fileName, collectionName ):
    '''
    Inserts data from a file from the test data directory whose name is given to the given collection.
    Returns a dict containing the test data.
    '''
    with( open( testDataDir / fileName, 'r' )) as data:
        # json_util is used to parse the mongodb extended JSON data correctly mainly  dates to python datetime objects
        testItems = json.load(data, object_hook=json_util.object_hook)
            
    # ensure collection is empty before adding data.
    collection = db[collectionName]
    collection.drop()
    collection.insert_many( testItems )
    return testItems

def insertTestSimData():
    '''
    Inserts the test simulation data.
    Returns a dict containing the test data.
    '''
    return insertDataFromFile( 'simulations.json', simulations.simCollection )

def deleteTestSimData():
    '''
    Removes the test simulations from the db by dropping the simulations collection.
    '''
    simCollection.drop()
    
def insertTestMsgData():
    '''
    Inserts test messages to db.
    '''
    return insertDataFromFile( 'messages1.json', messages.collectionNamePrefix +testMsgSimId )

def deleteTestMsgData():
    db[messages.collectionNamePrefix +testMsgSimId ].drop()

if __name__ == '__main__':
    # insert or delete the test data
    if len( sys.argv ) < 2:
        insertTestSimData()
        insertTestMsgData()
        print( 'Inserted test simulation and message data.' )
        
    elif sys.argv[1] == '-d':
        deleteTestSimData()
        deleteTestMsgData()
        print( 'Deleted test simulations and messages from database.' )
        
    else:
        print( 'Usage: without parameters adds test data. With parameter -d removes inserted test data.' )