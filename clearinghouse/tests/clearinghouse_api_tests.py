'''
Created on Jun 3, 2013

@author: Aaron.Vimont
'''
import unittest
import os
from clearinghouse import clearinghouse_api as chapi

class ClearinghouseAPIXmlTest(unittest.TestCase):


    def setUp(self):
        self.apiObj = chapi.ClearinghouseAPI('9SETg07EtIkOJtUYC7b1xMsNQlStuf8w5fVvb5AN')
        self.apiList = ['device details', 'search autocomplete', 'mobile devices', 'content', 'states', 'search', 'federal contacts', 'manufacturers', 'convenience contacts', 'regions', 'events', 'vpd contacts', 'features', 'apps and technologies', 'disability types']


    def tearDown(self):
        self.apiObj = None


    def testXmlCalls(self):
        self.apiObj.setParams(searchString='vol')
        print('----- XML -----')
        for apiName in self.apiList:
            print('Testing ' + apiName.ljust(25, '.'), end='')
            self.storedValue = self.apiObj.retrieveAPIData(apiName)
            self.assertTrue(len(self.storedValue.getResponseData()) > 0, "No data returned from " + apiName + " API call")
            print(' Done')


class ClearinghouseAPIJsonTest(unittest.TestCase):


    def setUp(self):
        self.apiObj = chapi.ClearinghouseAPI('9SETg07EtIkOJtUYC7b1xMsNQlStuf8w5fVvb5AN')
        self.apiList = ['device details', 'search autocomplete', 'mobile devices', 'content', 'states', 'search', 'federal contacts', 'manufacturers', 'convenience contacts', 'regions', 'events', 'vpd contacts', 'features', 'apps and technologies', 'disability types']


    def tearDown(self):
        self.apiObj = None


    def testJsonCalls(self):
        self.apiObj.setParams(searchString='vol', responseFormat='json')
        print('----- JSON -----')
        for apiName in self.apiList:
            print('Testing ' + apiName.ljust(25, '.'), end='')
            self.storedValue = self.apiObj.retrieveAPIData(apiName)
            self.assertTrue(len(self.storedValue.getResponseData()) > 0, "No data returned from " + apiName + " API call")
            print(' Done')
            
        
class ClearinghouseAPIJsonpTest(unittest.TestCase):


    def setUp(self):
        self.apiObj = chapi.ClearinghouseAPI('9SETg07EtIkOJtUYC7b1xMsNQlStuf8w5fVvb5AN')
        self.apiList = ['device details', 'search autocomplete', 'mobile devices', 'content', 'states', 'search', 'federal contacts', 'manufacturers', 'convenience contacts', 'regions', 'events', 'vpd contacts', 'features', 'apps and technologies', 'disability types']


    def tearDown(self):
        self.apiObj = None


    def testJsonpCalls(self):
        self.apiObj.setParams(searchString='vol', responseFormat='jsonp')
        print('----- JSONP -----')
        for apiName in self.apiList:
            print('Testing ' + apiName.ljust(25, '.'), end='')
            self.storedValue = self.apiObj.retrieveAPIData(apiName)
            self.assertTrue(len(self.storedValue.getResponseData()) > 0, "No data returned from " + apiName + " API call")
            print(' Done')

       
class ClearinghouseAPIExcelTest(unittest.TestCase):


    def setUp(self):
        self.apiObj = chapi.ClearinghouseAPI('9SETg07EtIkOJtUYC7b1xMsNQlStuf8w5fVvb5AN')
        self.apiList = ['content', 'states', 'federal contacts', 'convenience contacts', 'events', 'apps and technologies', 'disability types']


    def tearDown(self):
        self.apiObj = None
        
        
    def testExcelCalls(self):
        self.apiObj.setParams(searchString='vol', excel=True, filename='download.xls')
        print('----- EXCEL -----')
        for apiName in self.apiList:
            print('Testing ' + apiName.ljust(25, '.'), end='')
            self.storedValue = self.apiObj.retrieveAPIData(apiName)
            name = self.storedValue.getResponseData()
            self.assertTrue(os.path.exists(name), "No data returned from " + apiName + " API call")
            print(' Done')
            try:
                os.remove(name)
            except OSError:
                pass
            

class ClearinghouseAPIParameterTest(unittest.TestCase):
    
    def setUp(self):
        self.apiObj = chapi.ClearinghouseAPI('9SETg07EtIkOJtUYC7b1xMsNQlStuf8w5fVvb5AN')
        self.paramList = {'excel':          True,
                        'category':         'mobile',
                        'productID':        713,
                        'entityType':       'equipment manufacturer',
                        'tag':              'kid',
                        'groupByState':     True,
                        'dateFlag':         'future',
                        'stateName':        'arizona',
                        'disabilityId':     4,
                        'order':            'desc',
                        'feat':             3,
                        'responseFormat':   'json',
                        'vpdtype':          'cable',
                        'mfg':              'Nokia',
                        'region':           'Europe',
                        'rowPerPage':       20,
                        'contentType':      'UserVoice',
                        'searchString':     'sam',
                        'limit':            5,
                        'date':             '07/25/2013',
                        'page':             2,
                        'callback':         'myFunc'
                        }
    
    def tearDown(self):
        self.apiObj = None
        
    def testSetParams(self):
        print('--- CHECKING PARAMETERS ---')
        self.apiObj.setParams(excel=self.paramList['excel'], productID=self.paramList['productID'], 
                              entityType=self.paramList['entityType'], tag=self.paramList['tag'], 
                              groupByState=self.paramList['groupByState'], dateFlag=self.paramList['dateFlag'], 
                              stateName=self.paramList['stateName'], disabilityId=self.paramList['disabilityId'], 
                              order=self.paramList['order'], feat=self.paramList['feat'], 
                              responseFormat=self.paramList['responseFormat'], vpdtype=self.paramList['vpdtype'], 
                              mfg=self.paramList['mfg'], region=self.paramList['region'], 
                              rowPerPage=self.paramList['rowPerPage'], contentType=self.paramList['contentType'], 
                              searchString=self.paramList['searchString'], limit=self.paramList['limit'], 
                              date=self.paramList['date'], page=self.paramList['page'], 
                              callback=self.paramList['callback'])
        for key, val in self.paramList.items():
            print('Testing ' + key.ljust(25, '.'), end='')
            self.assertEqual(self.apiObj.getParam(key), val, "Mismatched values for '" + key + "'")
            print(' Done')
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()