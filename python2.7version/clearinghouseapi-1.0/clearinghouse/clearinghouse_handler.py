'''
Created on Jun 18, 2013

@author: Aaron.Vimont
'''
import time
import warnings
import urllib2, urllib
import xml.etree.ElementTree as et
from clearinghouse import clearinghouse_stored_value as chsv
from itertools import izip
import sys

verbose = False

class _ValueNotFoundException(Exception):
    def _init__(self, message):
        self.message = message
    def _str__(self):
        return self.message

class _UrlRequestException(Exception):
    def _init__(self, message):
        self.message = message
    def _str__(self):
        return self.message

class ClearinghouseHandler(object):
    
    # constructor
    def __init__(self, apiKey):
        # api key used in URL requests
        self._apiKey = apiKey
        
        # beginning of the request URL for all APIs except Video Programming Distributors
        self._requestStr = "http://data.fcc.gov/api/accessibilityclearinghouse"
        
        # set default values for mfg, region, etc. to empty strings
        self._currentParams = dict.fromkeys(['disabilityId', 'mfg', 'region', 'page', 'feat', 'searchString', 'limit', 'tag', 'entityRangeStartWith', 'entityRangeEndWith', 'groupByState', 'stateName', 'date'], '')
    
        # add default values that are not empty strings
        self._currentParams.update(izip(['responseFormat', 'callback', 'rowPerPage', 'category', 'excel', 'filename', 'productID', 'order', 'contentType', 'entityType', 'vpdtype', 'dateFlag'],\
                              ['xml', '?', -1, 'mobile', False, 'clearinghouse.xls', 1, 'asc', 'fact sheet', 'at program', 'broadcaster', 'future']))
    
        # dictionary of formatted values for use in request URLs
        self._formattedParams = dict.fromkeys(['disabilityId', 'mfg', 'region', 'page', 'feat', 'searchString', 'limit', 'tag', 'entityRangeStartWith', 'entityRangeEndWith', 'groupByState', 'stateName', 'date'], '')
    
        # add formatted values that are not empty strings
        self._formattedParams.update(izip(['responseFormat', 'callback', 'rowPerPage', 'rows_per_page', 'category', 'productID', 'order', 'contentType', 'entityType', 'vpdtype', 'vpdFormat', 'dateFlag'],\
                              ['&format=xml', '&jsonCallback=?', '&rowPerPage=-1', '&rows_per_page=-1', '&category=mobile', '&productID=1', '&order=asc', '&contentType=Fact%20sheet', '&entityType=at%20program', 'vpdtype=broadcaster.', 'xml?', '&dateFlag=future']))
        
        # dictionary (keys of parameter names) containing the API parameters
        # sub-dictionary with validValues OR conditionals that must be met by the parameter
        self._varList = {'excel':           {'validValues': [True, False]},
                        'category':         {'validValues': ['mobile']},
                        'productID':        {'validValues': ['''created below''']},
                        'entityType':       {'validValues': ['at program', 'equipment manufacturer', 'service provider', 'school', 'international', 'national']},
                        'tag':              {'validValues': ['vet', 'kid', 'sen']},
                        'groupByState':     {'validValues': [True, False]},
                        'dateFlag':         {'validValues': ['past', 'future']},
                        'stateName':        {'validValues': ['alabama', 'alaska', 'arizona', 'arkansas', 'california', 'colorado', 'commonwealth of the northern mariana islands', 'connecticut', 'delaware', 'district of columbia', 'florida', 'georgia', 'guam', 'hawaii', 'idaho', 'illinois', 'indiana', 'iowa', 'kansas', 'kentucky', 'louisiana', 'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota', 'mississippi', 'missouri', 'montana', 'nebraska', 'nevada', 'new hampshire', 'new jersey', 'new mexico', 'new york', 'north carolina', 'north dakota', 'ohio', 'oklahoma', 'oregon', 'pennsylvania', 'pensylvania', 'puerto rico', 'rhode island', 'south carolina', 'south dakota', 'tennessee', 'texas', 'utah', 'vermont', 'virginia', 'washington', 'west virginia', 'wisconsin', 'wyoming']},
                        'disabilityId':     {'validValues': [3, 4, 5, 6, 7]},
                        'order':            {'validValues': ['asc', 'desc']},
                        'feat':             {'validValues': ['''created below''']},
                        'responseFormat':   {'validValues': ['xml', 'json', 'jsonp']},
                        'vpdtype':          {'validValues': ['broadcaster', 'cable', 'lec', 'satellite', 'other']},
                        'mfg':              {'validValues': ['''created below''']},
                        'region':           {'validValues': ['Africa', 'Asia Pacific', 'Europe', 'Latin America', 'Middle East', 'North America']},
                        'rowPerPage':       {'validValues': [-1, 20, 40, 60, 100]},
                        'contentType':      {'validValues': ['Fact sheet', 'UserVoice']},
                        'searchString':     {'conditionals': "(newVal != '')"},
                        'limit':            {'conditionals': "(newVal > 0)"},
                        'date':             {'conditionals': "time.strptime(newVal, '%m/%d/%Y')"},
                        'page':             {'conditionals': "(newVal > 0)"},
                        'callback':         {'conditionals': "(newVal != '')"}
                        }
        
        # dictionary of API names
        # each key contains a dictionary of information about that API
        # - apiURL
        # - excelURL (if it exists)
        # - list of parameters
        # - list of strings of warnings and warning messages (if necessary)
        # - list of strings of errors and error messages (if necessary)
        self._apiCalls = {'disability types':       {'apiURL': '/disabilityTypes?api_key=',
                                                     'excelURL': '/DisabilityTypesService?api_key=',
                                                     'parameters': ['responseFormat']
                                                    },
                          'mobile devices':         {'apiURL': '/product/products?api_key=',
                                                     'parameters': ['category', 'feat', 'responseFormat', 'mfg', 'page', 'region', 'rowPerPage']
                                                    },
                          'device details':         {'apiURL': '/product/productFeatures?api_key=',
                                                     'parameters': ['productID', 'responseFormat']
                                                    },
                          'features':               {'apiURL': '/featureGroups?api_key=',
                                                     'parameters': ['disabilityId', 'responseFormat']
                                                    },
                          'manufacturers':          {'apiURL': '/product/manufacturers?api_key=',
                                                     'parameters': ['category', 'responseFormat']
                                                    },
                          'regions':                {'apiURL': '/product/regions?api_key=',
                                                    'parameters': ['order', 'responseFormat']
                                                    },
                          'search':                 {'apiURL': '/product/searchProducts?api_key=',
                                                     'parameters': ['searchString', 'responseFormat', 'page', 'rowPerPage'],
                                                     'warnings': ["self._currentParams['searchString'] == ''"],
                                                     'warningMsgs': ["\nPassing empty search string to method"]
                                                    },
                          'search autocomplete':    {'apiURL': '/product/makerBrandModel?api_key=',
                                                     'parameters': ['searchString', 'responseFormat', 'limit'],
                                                     'warnings': ["self._currentParams['searchString'] == ''"],
                                                     'warningMsgs': ["\nPassing empty search string to method"]
                                                    },
                          'apps and technologies':  {'apiURL': '/apps?api_key=',
                                                     'excelURL': '/AppsService?api_key=',
                                                     'parameters': ['disabilityId', 'responseFormat', 'page', 'rowPerPage']
                                                    },
                          'content':                {'apiURL': '/content?api_key=',
                                                     'excelURL': '/ContentService?api_key=',
                                                     'parameters': ['contentType', 'disabilityId', 'responseFormat']
                                                    },
                          'convenience contacts':   {'apiURL': '/contacts?api_key=',
                                                     'excelURL': '/ContactService?api_key=',
                                                     'parameters': ['entityType', 'tag', 'disabilityId', 'entityRangeStartWith', 'entityRangeEndWith', 'responseFormat', 'groupByState', 'page', 'rowPerPage', 'stateName'],
                                                     'errors': ["self._currentParams['entityType'] != '' and self._currentParams['tag'] != ''"],
                                                     'errorMsgs': ["entityType and tag cannot be used together! One must be empty"]
                                                    },
                          'states':                 {'apiURL': '/states?api_key=',
                                                     'excelURL': '/StatesService?api_key=',
                                                     'parameters': ['entityType', 'responseFormat']
                                                    },
                          'events':                 {'apiURL': '/events?api_key=',
                                                     'excelURL': '/EventService?api_key=',
                                                     'parameters': ['date', 'dateFlag', 'disabilityId', 'responseFormat', 'page', 'rowPerPage']
                                                    },
                          'federal contacts':       {'apiURL': '/fedContacts?api_key=',
                                                     'excelURL': '/FedContactService?api_key=',
                                                     'parameters': ['disabilityId', 'responseFormat', 'rowPerPage']
                                                    },
                          'vpd contacts':           {'apiURL': '',
                                                     'parameters': ['vpdtype', 'vpdFormat', 'rows_per_page', 'page']
                                                    }
                          }
        
        # update product ids
        self._varList['productID']['validValues'] = self._createProductIdList()
        #print(self._varList['productID']['validValues'])
        
        # update manufacturers
        self._varList['mfg']['validValues'] = self._createManufacturerList()
        
        # dictionary of feature ids and names
        self._dictOfFeatures = self._createFeatureList()
        self._varList['feat']['validValues'] = self._dictOfFeatures.keys()
        
        # END INIT
        
    def retrieveData(self, apiName, **args):
        if args: self.setParams(**args)
        
        if apiName.lower() in self._apiCalls:
            retval = self._callApi(apiName.lower())
        else:
            raise _ValueNotFoundException("api name '" + str(apiName) + "' is not a valid name")
            
        return retval
    
    def getFormattedParam(self, toget):
        if toget in self._formattedParams:
            return self._formattedParams[toget]
        else:
            raise _ValueNotFoundException("Parameter '" + str(toget) + "' is not an available parameter")
    
    def getParam(self, toget):
        if toget in self._currentParams:
            return self._currentParams[toget]
        else:
            raise _ValueNotFoundException("Parameter '" + str(toget) + "' is not an available parameter")
    
    # default values getter method
    def getCurrentParams(self, **args):
        return self._currentParams
    
    # default values setter method
    def setParams(self, **args):
        
        # check for existence of variable name and set default value if present
        for k in args:
            if k not in self._currentParams: # parameter name not found
                warnings.warn("\nParameter '" + k + "' is not an available parameter. No parameter was set")
            elif (k in self._currentParams) and (k not in self._varList): # only applies to filename
                self._currentParams[k] = args[k]
            else:
                # methods for conditionals...
                def runConditional(newVal, param, paramName):
                    conditions = param['conditionals']
                    if eval(conditions) and paramName in self._formattedParams:
                        self._formatVar(paramName, newVal)
                    else:
                        raise ValueError("Invalid value for " + paramName)
                # ... and valid values
                def checkValidValues(newVal, param):
                    if type(newVal) == str: newVal = newVal.lower()
                    for value in param['validValues']:
                        if ((type(value) == str) and (newVal == value.lower())):
                            return value
                        elif (newVal == value):
                            return value
                    else:
                        return False
                        
                param = self._varList[k]
                newVal = args[k]
                try:
                    # test for list of values and not a string
                    iterator = iter(newVal)
                    assert not isinstance(newVal, str)
                    # check if parameter supports multiple values
                    if not ((k == 'feat') or (k == 'mfg') or (k == 'region')):
                        raise _ValueNotFoundException("Parameter '" + k + "' does not support multiple values")
                    
                    for val in iterator:
                        if 'conditionals' in param:
                            runConditional(val, param, k)
                        elif 'validValues' in param:
                            valWithCaps = checkValidValues(val, param)
                            if not valWithCaps:
                                raise _ValueNotFoundException('Invalid value ' + str(val) + ' for ' + k)
                            if k in self._formattedParams:
                                self._formatVar(k, valWithCaps)
                    # all tests have passed, set current param
                    self._currentParams[k] = newVal
                    
                except (TypeError, AssertionError):
                    # parameter value is a number or a single string, not a list
                    if 'conditionals' in param:
                        runConditional(newVal, param, k)
                    elif 'validValues' in param:
                        valWithCaps = checkValidValues(newVal, param)
                        if not valWithCaps:
                            raise _ValueNotFoundException('Invalid value ' + str(val) + ' for ' + k)
                        if k in self._formattedParams:
                            self._formatVar(k, valWithCaps)
                    # all tests have passed, set current param
                    self._currentParams[k] = newVal
        
    def searchForFeatures(self, searchString):
        searchString = searchString.lower()
        searchList = searchString.split()
        
        # check for all features key words
        if (searchString == 'all features'):
            return self._dictOfFeatures
        
        # return item
        featureList = dict()
        
        # loop through all disability IDs and get feature ID and names that contain search string
        listOfDisabilityIds = self._varList['disabilityId']['validValues']
        for disId in listOfDisabilityIds:
            storedValue = self.retrieveData('features', disabilityId=disId)
            content = et.fromstring(storedValue.getResponseData())
            for product in content.findall('FeatureGroup/featureList'):
                productID = int(product.find("id").text)
                name = str(product.find("name").text)
                if (searchString in name.lower() and productID not in featureList):
                    featureList[productID] = name
                if (all(word in name.lower() for word in searchList) and productID not in featureList):
                    featureList[productID] = name
        
        return featureList
    
    def listOfMobileDevices(self):
        
        storedValue = self.retrieveData('mobile devices', rowPerPage=-1)
        
        content = et.fromstring(storedValue.getResponseData())
        deviceList = dict()

        for product in content.findall('Product'):
            productID = int(product.find("id").text)
            brand = str(product.find("brand").text)
            maker = str(product.find("maker").text)
            model = str(product.find("modelNumber").text)
            if productID not in deviceList:
                deviceList[productID] = (brand, maker, model)
            
        return deviceList
    
    def deviceDetails(self, productID):
        
        storedValue = self.retrieveData('device details', productID=productID)
        content = et.fromstring(storedValue.getResponseData())
        deviceDetails = dict()
        deviceDetails['features'] = dict()
        
        for product in content.findall('Product'):
            pBrand =  str(product.find("brand").text)
            pMaker = str(product.find("maker").text)
            pModel = str(product.find("modelNumber").text)
            deviceDetails['brand'], deviceDetails['maker'], deviceDetails['model'] = pBrand, pMaker, pModel
        
        for features in content.findall('Product/disabilityTypeList/featureList'):
            featId = int(features.find('id').text)
            feature = str(features.find('name').text)
            deviceDetails['features'][featId] = feature
            
        return deviceDetails
    
    def searchForDevices(self, searchString):
        
        self.setParams(searchString=searchString, rowPerPage=-1)
        storedValue = self.retrieveData('search')
        content = et.fromstring(storedValue.getResponseData())
        deviceList = dict()
        
        for product in content.findall('Product'):
            productID = int(product.find("id").text)
            brand = str(product.find("brand").text)
            maker = str(product.find("maker").text)
            model = str(product.find("modelNumber").text)
            regions = str(product.find("regions").text)
            if productID not in deviceList:
                deviceList[productID] = (brand, maker, model, regions)
            
        return deviceList
    
    
    """*********************************************************
    *                   Private Methods                        *
    *********************************************************"""
    
    def _callApi(self, apiName):
        
        api = self._apiCalls[apiName]
        
        # if currentParams['excel'] is True and the excelURL exists, set excel variable to True
        excel = (self._currentParams['excel'] and 'excelURL' in api)
            
        # special case for VPD
        if apiName == 'vpd contacts':
            requestStr = 'http://data.fcc.gov/api/vpd-service/contacts/'
            
            # add parameters to requestString
            for param in api['parameters']:
                requestStr += self._formattedParams[param]
            # ENDIF
        else: # all other APIs
            
            # check for warnings and errors
            if 'warnings' in api:
                warningList = api['warnings']
                for i, checkWarning in enumerate(warningList):
                    if eval(checkWarning): warnings.warn(api['warningMsgs'][i])
            # errors
            if 'errors' in api:
                errList = api['errors']
                for i, checkErr in enumerate(errList):
                    if eval(checkErr): warnings.warn(api['errorMsgs'][i])
            
            requestStr = self._requestStr
            
            # prepare excel api call or regular api call
            if excel: requestStr += api['excelURL'] + self._apiKey
            else: requestStr += api['apiURL'] + self._apiKey
            
            # add parameters to request str
            for param in api['parameters']:
                requestStr += self._formattedParams[param]
            # END ELSE
                
        # call excel api or regular api
        if excel:
            filename = self._currentParams['filename']
            splitName = filename.split('.', 1)
            if len(splitName) > 1:
                filename = splitName[0] + time.strftime('%y-%m-%d_%I-%M-%S.') + splitName[1]
            else:
                filename += time.strftime('%y-%m-%d_%I-%M-%S')
            if not ('.xls' in filename): filename += '.xls'
            urllib.urlretrieve(requestStr, filename)
            storedValue = chsv.ClearinghouseStoredValue('excel', filename, requestStr)
        
        else:
            response = self._runRequest(requestStr)
            
            try: content = response.read().decode('utf-8').encode('ascii', 'ignore').decode('utf-8')
            except strDecodeError:
                print "Error decoding and encoding content"
                content=''
            
            storedValue = chsv.ClearinghouseStoredValue(self._currentParams['responseFormat'], content, requestStr)
            
        return storedValue
        
    def _formatVar(self, name, value):
                
        # special cases
        if name == 'responseFormat':
            self._formattedParams['responseFormat'] = '&format=' + value
            self._formattedParams['vpdFormat'] = value + '?'
            if value == 'jsonp':
                self._formattedParams['responseFormat'] += '&jsonCallback=' + self._currentParams['callback']
                self._formattedParams['vpdFormat'] = 'json?jsonpCallback=' + self._currentParams['callback']
            
        elif name == 'callback' and self._currentParams['responseFormat'] == 'jsonp':
            self._formattedParams['responseFormat'] = '&format=' + self._currentParams['responseFormat'] + '&jsonCallback=' + str(value)
            self._formattedParams['vpdFormat'] = 'json?jsonpCallback=' + str(value)
        
        elif name == 'vpdtype':
            self._formattedParams['vpdtype'] = 'vpdtype=' + value + '.'
        
        elif name == 'rowPerPage':
            self._formattedParams['rowPerPage'] = '&rowPerPage=' + str(value)
            self._formattedParams['rows_per_page'] = '&rows_per_page=' + str(value)
        
        else: # all other parameters
            def addSpecialChars(name, value):
                value = value.replace(' ', '%20')
                return '&' + name + '=' + value
            try:
                iterator = iter(value) # we have a list
                assert not isinstance(value, str)
                for val in iterator:
                    self._formattedParams[name] += addSpecialChars(str(name), str(val))
            except TypeError:
                self._formattedParams[name] = addSpecialChars(str(name), str(value))
            except AssertionError:
                self._formattedParams[name] += addSpecialChars(str(name), str(value))
        
    
    '''
    runRequest()
        - Return response string from API call
        - Required parameter: urlStr (full URL for API call)
    '''
    def _runRequest(self, urlStr):
        try:
            response = urllib2.urlopen(urlStr, timeout=60)
            return response
        except urllib2.URLError, err:
            raise _UrlRequestException("Error processing request: " + err.read().decode("UTF8"))
            return None
        
    def _createFeatureList(self):
        global verbose
        if verbose: print 'Creating dictionary of features... ',; sys.stdout.write('')
        
        # return item
        featureIdsAndName = dict()
        
        # loop through all disability IDs and get feature ID and names that contain search string
        listOfDisabilityIds = self._varList['disabilityId']['validValues']
        for disId in listOfDisabilityIds:
            storedValue = self.retrieveData('features', disabilityId=disId)
            content = et.fromstring(storedValue.getResponseData())
            for product in content.findall('FeatureGroup/featureList'):
                productID = int(product.find("id").text)
                name = str(product.find("name").text)
                if (productID not in featureIdsAndName):
                    featureIdsAndName[productID] = name
        
        if verbose and len(featureIdsAndName): print 'Success!'
        elif verbose: print 'Failed'
        return featureIdsAndName
    
    def _createProductIdList(self):
        global verbose
        if verbose: print 'Creating list of product IDs... ',; sys.stdout.write('')
        
        productIdList = []
        
        storedValue = self.retrieveData('mobile devices')
        # check for invalid api key
        if 'Incorrect API Key' in str(storedValue.getResponseData()):
            raise ValueError("Invalid API Key")
        
        content = et.fromstring(storedValue.getResponseData())
        
        for product in content.findall('Product'):
            productId = int(product.find("id").text)
            if not productId in productIdList: productIdList.append(productId)
            
        if verbose and len(productIdList): print 'Success!'
        elif verbose: print 'Failed'
        return productIdList
    
    def _createManufacturerList(self):
        global verbose
        if verbose: print 'Creating list of manufacturers... ',; sys.stdout.write('')
        
        mfgList = []
        
        storedValue = self.retrieveData('manufacturers')
        content = et.fromstring(storedValue.getResponseData())
        
        for name in content.findall('Manufacturer'):
            mfg = name.text
            if not mfg in mfgList:
                mfgList.append(mfg)
        
        if verbose and len(mfgList): print 'Success!'
        elif verbose: print 'Failed'
        return mfgList
    
