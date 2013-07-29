'''
Created on May 22, 2013

@author: Aaron.Vimont
'''
from clearinghouse import clearinghouse_handler as hdlr

verbose = False

class ClearinghouseAPI:
    
    HEARING, DEAFBLIND, BLIND, MOBILITY, COGNITIVE = 3, 4, 5, 6, 7

    def __init__(self, apiKey):
        # constructor
        self._handler = hdlr.ClearinghouseHandler(apiKey)
        
    
    '''
    retrieveAPIData(apiName, args)
        - Returns a ClearinghouseStoredValue object with a string containing
          response data in XML, JSON, or JSONP format
        - Required parameter: apiName (from valid list)
    '''
    def retrieveAPIData(self, apiName, **args):
        # call handler retrieve data
        return self._handler.retrieveData(apiName, **args)
    
    
    '''
    searchForFeatures(searchString)
        - Searches through feature names to find those that contain the search string
        - Returns a dictionary of feature IDs and names
        - Required parameter: searchString (any string value)
          NOTE: pass "all features" to return a list of all features
    '''
    def searchForFeatures(self, searchString):
        # call handler feature search
        return self._handler.searchForFeatures(searchString)


    '''
    listOfMobileDevices()
        - Returns a dictionary of device IDs and brand, maker, and model
          OR returns a strings containing raw XML, JSON, or JSONP
        - Optional Parameter: responseFormat ('xml', 'json', jsonp') will return a raw string
    '''
    def listOfMobileDevices(self):
        # call handler mobile devices
        return self._handler.listOfMobileDevices()
    
    
    '''
    deviceDetails(deviceId)
        - Returns a dictionary of device brand, maker, and model along with
          a list of accessibility features for the device
        - Required parameter: deviceId (number) from product list
    '''
    def deviceDetails(self, productId):
        # call handler device details
        return self._handler.deviceDetails(productId)
    
    
    '''
    searchForDevices(searchString)
        - Compares searchString to Brand, Maker, and Model
        - Returns a dictionary of device IDs and brand, maker, model, and regions
        - Required Parameter: searchString (any string value)
    '''
    def searchForDevices(self, searchString):
        # call handler search for devices
        return self._handler.searchForDevices(searchString)
    
    
    '''
    setParams(args)
        - Sets a list of parameters to be used in API calls
        - Does not return any values
        - Optional Parameter: any parameters to update
    '''
    def setParams(self, **args):
        # call handler set params
        self._handler.setParams(**args)
        
    
    '''
    getCurrentParams()
        - Returns a dictionary of current parameters and their values
    '''
    def getCurrentParams(self):
        # call handler get params
        return self._handler.getCurrentParams()
    
    '''
    getParam()
        - Returns the value of the toGet parameter
    '''
    def getParam(self, toGet):
        # call handler get param
        return self._handler.getParam(toGet)
        