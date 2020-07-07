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

from LogReader.db import db, simulations

# the mongodb collection where simulations are stored.
simCollection = db[simulations.simCollection]
# location of json files containing test data.
testDataDir = pathlib.Path(__file__).parent.absolute() / 'data'

def insertTestSimData():
    '''
    Inserts the test simulation data.
    Returns a dict containing the test data.
    '''
    with( open( testDataDir / 'simulations.json', 'r' )) as simData:
        # json_util is used to parse the mongodb extended JSON data correctly mainly  dates to python datetime objects
        testSimulations = json.load(simData, object_hook=json_util.object_hook)
            
    # ensure simulations collection is empty before adding data.
    deleteTestSimData()
    simCollection.insert_many( testSimulations )
    return testSimulations

def deleteTestSimData():
    '''
    Removes the test simulations from the db by dropping the simulations collection.
    '''
    simCollection.drop()
    
if __name__ == '__main__':
    # insert or delete the test data
    if len( sys.argv ) < 2:
        insertTestSimData()
        print( 'Inserted test simulation data.' )
        
    elif sys.argv[1] == '-d':
        deleteTestSimData()
        print( 'Deleted test simulations from database.' )
        
    else:
        print( 'Usage: without parameters adds test data. With parameter -d removes inserted test data.' )