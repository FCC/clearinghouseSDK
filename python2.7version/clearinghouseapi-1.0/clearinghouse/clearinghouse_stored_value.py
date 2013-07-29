'''
Created on May 24, 2013

@author: aaron.vimont
'''
import xml.dom.minidom as minidom
import json

class ClearinghouseStoredValue(object):
    '''
    classdocs
    '''


    def __init__(self, responseFormat, responseData, requestURL):
        # constructor
        self._responseFormat = responseFormat
        self._responseData = responseData
        self._requestURL = requestURL
        
    def printData(self):
        if (self._responseFormat == 'xml'):
            try:
                xml = minidom.parseString(self._responseData)
                prettyXml = xml.toprettyxml()
                print "\nStored XML:\n" + prettyXml
            except:
                print "Could not print XML: '" + self._responseData + "'"
        elif (self._responseFormat == 'json'):
            try:
                data = json.loads(self._responseData)
                print "\nStored JSON:\n" + json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
            except:
                print "Could not print JSON: '" + self._responseData + "'"
        elif (self._responseFormat == 'jsonp'):
            try:
                print "\nStored JSONP:\n" + str(self._responseData)
            except:
                print "Could not print JSONP"
        elif (self._responseFormat == 'excel'):
            print "\nExcel filename: " + self._responseData
        else:
            print "Error while printing"
            
    def printRequest(self):
        print 'URL:\n' + self._requestURL
        
    def getRequestURL(self):
        return self._requestURL
    
    def getReponseFormat(self):
        return self._responseFormat
    
    def getResponseData(self):
        return self._responseData
