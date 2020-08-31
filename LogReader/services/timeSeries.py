'''
Created on 21.8.2020

@author: hylli
'''
import dateutil

from LogReader.db import messages

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
                                
    def _processEpochData(self):
        timeIndex = self._result['TimeIndex']
        numValues = len( timeIndex )
        for data in self._epochResult:
            for attr in data:
                if attr == 'index' or attr == 'timeIndex':
                    continue
                
                values = data[attr]['values']
                missing = numValues -len( values )
                if missing > 0:
                    values.extend( missing *[ None ] )
        
        #nextTime = min( dateutil.)
    
    def _cleanResult(self, result = None ):
        if result == None:
            result = self._result
        
        if 'index' in result and 'timeIndex' in result:
            del result['index']
            del result['timeIndex']
            for attr in result:
                result[attr] = result[attr]['values']
                
            return
        
        for key in result:
            self._cleanResult( result[key] )

def _isTimeSeries(value):
    return seriesAttr in value and timeIndexAttr in value