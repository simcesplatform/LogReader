'''
Created on 21.8.2020

@author: hylli
'''

from LogReader.db import messages

seriesAttr = 'Series'
seriesValueAttr = 'Values'
seriesTimeAttr = 'StartTime'
seriesIntervalAttr = 'Interval'

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
        while self._dataRemaining:
            self._getEpochData()
            
    def _getEpochData(self):
        nextEpoch = min( [ tsMsgs.getNextEpochNumber() for tsMsgs in self._data ])
        epochData = [ tsMsgs for tsMsgs in self._data if nextEpoch == tsMsgs.getNextEpochNumber() ]
        
        for tsMsgs in epochData:
                for msg in tsMsgs.getNextEpochMsgs(): 
                    topic = msg[messages.topicAttr]
                    process = msg[messages.processAttr]
                    processData = self._result.setdefault( topic, {} ).setdefault( process, {} )
                    for attr in tsMsgs.attrs:
                        attrParent = processData
                        prevValue = msg
                        foundTimeSeries = False
                        for i in range( 0, len(attr) -1):
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
                            series = prevValue[seriesAttr]
                            if i == len( attr ) -1:
                                for key in series:
                                    resultSeries = attrParent.setdefault( key, { 'values': [] })
                                    resultSeries['index'] = 0
                                    resultSeries['source'] = series[key][ seriesValueAttr ] 
                            
                            else:
                                resultSeries = attrParent.setdefault( attr[-1], { 'values': [] })
                                resultSeries['index'] = 0
                                resultSeries['source'] = series[attr[-1]][ seriesValueAttr ] 

def _isTimeSeries(value):
    return seriesAttr in value