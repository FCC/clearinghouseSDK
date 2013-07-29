FCC Clearinghouse API Python SDK
=======

A Python SDK for the FCC's Clearinghouse API

FCC API Information
-------
[FCC API Developer Guide](http://apps.fcc.gov/accessibilityclearinghouse/developers.html?pgID=5 "FCC Clearinghouse API")

Installation
-------
Change to clearinghouse-1.0 directory

	$ [sudo] python setup.py install

Usage
-------
### API Key
Before using the SDK, a user must obtain an API key. The API key is free, as is the data, and instructions for obtaining an API key can be found at
<http://apps.fcc.gov/accessibilityclearinghouse/developers.html?pgID=5>

### API Python Classes
The SDK provides two classes for retrieving data from the FCC Clearinghouse APIs and storing the data.

The ClearinghouseAPI class provides several methods that allow the user to search for devices, manufacturers, brands, or device features. The class also provides a method that allows the user to access any of the Clearinghouse APIs. The ClearinghouseStoredValue class stores the URL that was used for the request, the format type of the retrieved data (xml, json, or jsonp), and a string of the data.

Usage Examples
-------
### Search for Features Example
	from clearinghouse.clearinghouse_api import ClearinghouseAPI
	
	# create instance of ClearinghouseAPI, pass in API key (str) as parameter
	myClearinghouse = ClearinghouseAPI('YOUR API KEY HERE')
	
	# call searchForFeatures method with search string parameter
	dictOfFeatures = myClearinghouse.searchForFeatures('adjustable')
	
	print(dictOfFeatures)
### API Call XML Example
	from clearinghouse.clearinghouse_api import ClearinghouseAPI
	import xml.etree.ElementTree as et
	
	# create instance of ClearinghouseAPI, pass in API key (str) as parameter
	myClearinghouse = ClearinghouseAPI('YOUR API KEY HERE')
	
	xmlStoredValue = myClearinghouse.retrieveAPIData('federal contacts')
	
	# print XML if needed
	# xmlStoredValue.printData()

	xmlContent = et.fromstring(xmlStoredValue.getResponseData())

	data = dict()

	for contact in xmlContent.findall('Contact'):
	    contactId = int(contact.find("id").text)
	    name = str(contact.find("entityName").text)
	    
	    # get email if it exists
	    try: email = str(contact.find("generalEmail").text)
	    except: email = ''
	    
	    # get fax if it exists
	    try: fax = str(contact.find("fax").text)
	    except: fax = ''
		
		# add name, email, and fax to dictionary. Use contactId as key
	    if contactId not in data:
	        data[contactId] = (name, email, fax)

	print(data)

Methods
-------
#### retrieveAPIData(apiName, **args)
- Returns a ClearinghouseStoredValue object with a string containing response data in XML, JSON, or JSONP format
- Required parameter: apiName (from valid API name list)
- Optional parameters: any parameter from list of defined parameters. E.g. responseFormat='json'
- Example: `myClearinghouse.retrieveAPIData('search', searchString='apple', responseFormat='json')`
- Review list of API Names below

#### searchForFeatures(searchString)
- Searches through feature names to find those that contain the search string
- Returns a dictionary of feature IDs and names
- Required parameter: searchString (any string value)
- NOTE: pass "all features" to return a list of all features

#### searchForDevices(searchString)
- Compares searchString to Brand, Maker, and Model
- Returns a dictionary of device IDs and brand, maker, model, and regions
- Required Parameter: searchString (any string value)

#### listOfMobileDevices()
- Returns a dictionary of device IDs and brand, maker, and model OR returns a strings containing raw XML, JSON, or JSONP
- Optional Parameter: responseFormat ('xml', 'json', jsonp') will return a raw string

#### deviceDetails(deviceId)
- Returns a dictionary of device brand, maker, and model along with a list of accessibility features for the device
- Required parameter: deviceId (number) from product list

#### setParams(**args)
- Sets a list of parameters to be used in API calls
- Does not return any values
- Optional Parameter: any parameters to update
- Example: `myClearinghouse.setParams(responseFormat='json', disabilityId=5)`

#### getCurrentParams()
- Returns a dictionary of current parameters and their values

#### getParam(toGet)
- Returns the value of the specified parameter
- Required parameter: toGet (parameter name as string value)
- Example: `myClearinghouse.getParam('rowPerPage')`

API Names for retrieveAPIData() method
-------
<table>
<tr><td><b>Name</b></td><td><b>Description</b></td></tr>
<tr><td>'disability types'</td><td>Returns a list of disabilities along with the disability type name, id, short description and long description</td></tr>
<tr><td>'mobile devices'</td><td>Returns a list of mobile devices as well as the original source of the data</td></tr>
<tr><td>'device details'</td><td>Returns a list of accessibility features (with name and description) that are supported by a particular device as well as the source for the original data</td></tr>
<tr><td>'features'</td><td>Returns a list of accessibility features (with name and description) that may be supported by various products</td></tr>
<tr><td>'manufacturers'</td><td>Returns a list of product manufacturers</td></tr>
<tr><td>'regions'</td><td>Returns a list of regions where various products may be available</td></tr>
<tr><td>'search'</td><td>Returns a list of mobile devices based on a search query (manufacturer, brand, or model) as well as the original source of the data</td></tr>
<tr><td>'search autocomplete'</td><td>Returns a list of mobile devices (manufacturer or brand and model number) as the user types a search query</td></tr>
<tr><td>'apps and technologies'</td><td>Returns a list of accessible apps and assistive technologies as well as the original source of the data</td></tr>
<tr><td>'content'</td><td>Returns content for Fact Sheets and User Voice questions as well as the original source of the data</td></tr>
<tr><td>'convenience contacts'</td><td>Returns a variety of convenience contact information as well as the original source of the data for Service Providers, Equipment Manufacturers, Schools and Universities, and National and International Organizations. The list of contacts can be grouped by state</td></tr>
<tr><td>'states'</td><td>Returns a list of states by which the convenience contacts can be grouped</td></tr>
<tr><td>'events'</td><td>Returns a list of upcoming and past Disability Related Events</td></tr>
<tr><td>'federal contacts'</td><td>Returns a list of Federal Agencies that provide accessibility related services or information</td></tr>
<tr><td>'vpd contacts'</td><td>Returns a list of contact information for various Video Programming Distributors</td></tr>
</table>

API Parameters
-------
The following is a list of parameters that can be passed to the setParams() method in order to change the output from the APIs.

__NOTE:__ Parameter names are __case sensitive__

<table>
<tr><td><b>Name</b></td><td><b>Type</b></td><td><b>Values</b></td></tr>
<tr><td>responseFormat</td><td>str</td><td>'xml', 'json', 'jsonp'</td></tr>
<tr><td>callback</td><td>str</td><td>Any string value. Only used for JSONP response format</td></tr>
<tr><td>disabilityId</td><td>int</td><td>3, 4, 5 ,6, 7</td></tr>
<tr><td>productID</td><td>int</td><td>Retrieve productID from ClearinghouseAPI for the full list of product IDs</td></tr>
<tr><td>feat</td><td>int</td><td>Retrieve feat from ClearinghouseAPI for the full list of features</td></tr>
<tr><td>searchString</td><td>str</td><td>Any string value</td></tr>
<tr><td>limit</td><td>int</td><td>Value greater than 0. Used to limit number of results for 'search autocomplete'</td></tr>
<tr><td>rowPerPage</td><td>int</td><td>-1 (for all results), 20, 40, 60, 100</td></tr>
<tr><td>page</td><td>int</td><td>Any value greater than 0</td></tr>
<tr><td>order</td><td>str</td><td>'asc', 'desc'</td></tr>
<tr><td>mfg</td><td>str</td><td>Retrieve mfg from ClearinghouseAPI for the full list of manufacturers</td></tr>
<tr><td>region</td><td>str</td><td>Retrieve region from ClearinghouseAPI for the full list of regions</td></tr>
<tr><td>entityType</td><td>str</td><td>Retrieve entityType from ClearinghouseAPI for the full list</td></tr>
<tr><td>tag</td><td>str</td><td>'vet', 'kid', 'sen'</td></tr>
<tr><td>date</td><td>str</td><td>MM/DD/YYYY format</td></tr>
<tr><td>dateFlag</td><td>str</td><td>'past', 'future'</td></tr>
<tr><td>stateName</td><td>str</td><td>Retrieve stateName from ClearinghouseAPI for the full list of state names</td></tr>
<tr><td>groupByState</td><td>Bool</td><td>True, False</td></tr>
<tr><td>contentType</td><td>str</td><td>'Fact sheet', 'UserVoice'</td></tr>
<tr><td>vpdType</td><td>str</td><td>'broadcaster', 'cable', 'lec', 'satellite', 'other'</td></tr>
<tr><td>excel</td><td>Bool</td><td>True, False. Set to True to receive data in Excel spreadsheet format</td></tr>
</table>
