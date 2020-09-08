'''
Created on 21.8.2020

@author: hylli
'''
import dateutil
from io import StringIO
import csv

from LogReader.db import messages
from LogReader import utils

seriesAttr = 'Series'
seriesValueAttr = 'Values'
timeIndexAttr = 'TimeIndex'

class TimeSeriesMessages():
    
    def __init__(self, attrs, msgs ):
        self._attrs = [ attr.split( '.' ) for attr in attrs ]
        self._msgs = msgs
        self._epochIndex = 0
        
    @property
    def attrs(self):
        return self._attrs
    
    @property
    def msgs(self):
        return self._msgs
    
    def getNextEpochNumber(self):
        try:
            return self.msgs[self._epochIndex][messages.epochNumAttr]
        
        except IndexError:
            return None
    
    def getNextEpochMsgs(self):
        if self._epochIndex >= len( self._msgs ):
            return None
        
        result = []
        epoch = self.msgs[self._epochIndex][messages.epochNumAttr]
        for msg in self.msgs[self._epochIndex:]:
            if msg[messages.epochNumAttr] != epoch:
                break
                
            result.append( msg )
            self._epochIndex += 1
            
        return result
            
class TimeSeries(object):
    '''
    classdocs
    '''


    def __init__(self, timeSeriesMessages : list  ):
        '''
        Constructor
        '''
        self._data = timeSeriesMessages
        self._dataRemaining = True
        self._result = { 'TimeIndex': [] }
        
    def createTimeSeries(self):
        while self._findNextEpoch():
            self._getEpochData()
            self._processEpochData()
            
            
        self._cleanResult()
            
    def _findNextEpoch(self):
        nextEpochs = [ tsMsgs.getNextEpochNumber() for tsMsgs in self._data if tsMsgs.getNextEpochNumber() != None ]
        if len( nextEpochs ) == 0:
            self._nextEpoch = None
            return False
        
        self._nextEpoch = min( nextEpochs )
        return True

    def _getEpochData(self):
        epochData = [ tsMsgs for tsMsgs in self._data if self._nextEpoch == tsMsgs.getNextEpochNumber() ]
        self._epochResult = []
        
        for tsMsgs in epochData:
                for msg in tsMsgs.getNextEpochMsgs(): 
                    topic = msg[messages.topicAttr]
                    process = msg[messages.processAttr]
                    processData = self._result.setdefault( topic, {} ).setdefault( process, {} )
                    for attr in tsMsgs.attrs:
                        attrParent = processData
                        prevValue = msg
                        foundTimeSeries = False
                        for i in range( 0, len(attr)):
                            part = attr[i]
                            value = prevValue.get(part)
                            if value == None:
                                break
                            
                            prevValue = value
                            attrParent = attrParent.setdefault( part, {} )
                            
                            if _isTimeSeries( value ):
                                foundTimeSeries = True
                                break
                            
                        if foundTimeSeries:
                            self._epochResult.append( attrParent )
                            attrParent['index'] = 0
                            #attrParent['timeIndex'] = prevValue[timeIndexAttr]
                            attrParent['timeIndex'] = [ dateutil.parser.isoparse( date ) for date in prevValue[timeIndexAttr] ]
                            series = prevValue[seriesAttr]
                            if i == len( attr ) -1:
                                for key in series:
                                    resultSeries = attrParent.setdefault( key, { 'values': [] })
                                    resultSeries['source'] = series[key][ seriesValueAttr ] 
                            
                            else:
                                resultSeries = attrParent.setdefault( attr[-1], { 'values': [] })
                                resultSeries['source'] = series[attr[-1]][ seriesValueAttr ]
                                
    def _handleMissingDataForEpoch(self):
        for data in self._epochResult:
            for attr in data:
                if attr == 'index' or attr == 'timeIndex':
                    continue
                
                values = data[attr]['values']
                self._addMissingValues( values )
                
    def _addMissingValues(self, values):                
        timeIndex = self._result['TimeIndex']
        numValues = len( timeIndex )
        missing = numValues -len( values )
        if missing > 0:
            values.extend( missing *[ None ] )
        
    def _processEpochData(self):
        self._handleMissingDataForEpoch()
        timeIndex = self._result['TimeIndex']
        while True:
            nextTimes = [ item['timeIndex'][ item['index'] ] for item in self._epochResult if item['index'] != None ]
            if len( nextTimes ) == 0:
                break 
            
            nextTime = min( nextTimes )
            timeIndex.append( { 'epoch': self._nextEpoch, 'timestamp': nextTime })
            for item in self._epochResult:
                index = item['index']
                hasData = nextTime == item['timeIndex'][index]
                
                for key in item:
                    if key in [ 'index', 'timeIndex' ]:
                        continue
                    
                    attrData = item[key]
                    value = None
                    if hasData:
                        value = attrData['source'][index]
                            
                    attrData['values'].append( value )
                
                if hasData:    
                    index += 1
                    if index == len( item['timeIndex'] ):
                        index = None
                    
                    item['index'] = index
                    
    def _cleanResult(self, result = None ):
        if result == None:
            result = self._result
        
        if 'index' in result and 'timeIndex' in result:
            del result['index']
            del result['timeIndex']
            for attr in result:
                values = result[attr]['values']
                self._addMissingValues(values)
                result[attr] = values 
                
            return
        
        for key in result:
            if key != 'TimeIndex':
                self._cleanResult( result[key] )
                
    def getResult(self):
        return self._result

class TimeSeriesCsvConverter():
    
    def __init__(self, timeSeries, target = None ):
        self._timeSeries = timeSeries
        self._target = target
        if target == None:
            self._target = StringIO( newline = '' )
            
    def createCsv(self):
        self._createHeaders()
        timeIndex = self._timeSeries['TimeIndex']
        for i in range( 0, len( timeIndex )):
            time = timeIndex[i]
            row = dict( time )
            row['timestamp'] = utils.dateToIsoString( row['timestamp'] )
            row.update( { column: values[i] for (column, values) in self._columns.items() })
            self._csv.writerow( row )
        
    def _createHeaders(self):
        self._columns = {}
        for topic in self._timeSeries:
            if topic == 'TimeIndex':
                continue
            
            topicData = self._timeSeries[ topic ] 
            for process in topicData:
                processData = topicData[ process ]
                self._getProcessAttrs( processData, topic +':' +process )
        
        columnNames = [ 'epoch', 'timestamp' ] +list( self._columns.keys() )        
        self._csv = csv.DictWriter( self._target, columnNames, delimiter = ';' )
        self._csv.writeheader()
        
    def _getProcessAttrs(self, data, columnName ):
        for attr in data:
            value = data[attr]
            newColumnName = columnName +'.' +attr
            if type( value ) == list:
                self._columns[newColumnName] = value
                
            else:
                self._getProcessAttrs( value, newColumnName)
        
    def getTarget(self):
        return self._target
    
def _isTimeSeries(value):
    return seriesAttr in value and timeIndexAttr in value

class TimeSeriesMessageFilter():
    
    def __init__(self, attrs, process = None, topic = None ):
        self._attrs = attrs
        self._process = process
        self._topic = topic
        
    @property
    def attrs(self):
        return self._attrs
    
    @property
    def process(self):
        return self._process
    
    @property
    def topic(self):
        return self._topic
    
def getTimeSeries( messageStore, simId, messageFilters, epoch = None, startEpoch = None, endEpoch = None, fromSimDate = None, toSimDate = None, csv = False ):
    timeSeriesMsgsLst = []
    for msgFilter in messageFilters:
        msgs = messageStore.getMessages( simId, epoch = epoch, startEpoch = startEpoch, endEpoch = endEpoch, fromSimDate = fromSimDate, toSimDate = toSimDate, process = msgFilter.process, topic = msgFilter.topic, sortAttr = messages.epochNumAttr )
        msgs = [ message for message in msgs if messages.epochNumAttr in message ]
        timeSeriesMsgsLst.append( TimeSeriesMessages( msgFilter.attrs, msgs ))
        
    timeSeries = TimeSeries( timeSeriesMsgsLst )
    timeSeries.createTimeSeries()
    result = timeSeries.getResult()
    if csv:
        csvConverter = TimeSeriesCsvConverter( result )
        csvConverter.createCsv()
        result = csvConverter.getTarget().getvalue()
        
    return result 