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
from functools import partial
import csv
import io

from LogReader.db import db, simulations, messages

# the mongodb collection where simulations are stored.
simCollection = db[simulations.simCollection]
# location of json files containing test data.
testDataDir = pathlib.Path(__file__).parent.absolute() / 'data'

# id of simulation for which there are test messages.
testMsgSimId = '2020-06-03T04:01:52.345Z'

def writeFile( fileName, data ):
    filePath = testDataDir / fileName
    fileType = filePath.suffix[1:]
    with open( filePath, 'w' ) as file:
        if fileType == 'json':
            opt = json_util.JSONOptions(strict_number_long=False, datetime_representation=json_util.DatetimeRepresentation.ISO8601, strict_uuid=False, json_mode=0, document_class=dict, tz_aware=True,  unicode_decode_error_handler='strict'  )
            default = partial( json_util.default, json_options = opt ) 
            json.dump( data, file, default = default, indent = 3 )
            
        elif fileType == 'csv':
            file.write( data )

def readFile( fileName, csvDelimiter = ';' ):
    '''
    Read the given file from test data directory.
    '''
    filePath = testDataDir / fileName
    fileType = filePath.suffix[1:]
    fileParams = {} 
    if fileType == 'csv':
        fileParams[ 'newline' ] = ''
         
    with( open( filePath, 'r', **fileParams )) as data:
        if fileType == 'json':
            # json_util is used to parse the mongodb extended JSON data correctly mainly  dates to python datetime objects
            data = json.load(data, object_hook=json_util.object_hook)
            
        elif fileType == 'csv':
            data = io.StringIO( data.read(), newline = '' ) 
            data = csv.DictReader( data, delimiter = csvDelimiter )
        
    return data
    
def insertDataFromFile( fileName, collectionName ):
    '''
    Inserts data from a file from the test data directory whose name is given to the given collection.
    Returns a dict containing the test data.
    '''
    testItems = readFile( fileName )
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
    return insertDataFromFile( 'messages1.json', messages._getMessageCollectionName( testMsgSimId ))

def deleteTestMsgData():
    db[messages._getMessageCollectionName( testMsgSimId ) ].drop()

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