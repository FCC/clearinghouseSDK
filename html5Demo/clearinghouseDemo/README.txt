FCC Clearinghouse API Web Demo
=======
An HTML5 demo to illustrate using API calls from the FCC Clearinghouse in conjunction with data from CNET.com.

API Information
-------
[FCC API Developer Guide](http://apps.fcc.gov/accessibilityclearinghouse/developers.html?pgID=5 "FCC Clearinghouse API")

[CNET.com API Developer Guide](http://developer.cnet.com/ "CNET.com API Developers")

About this Demo
-------
The files included in this package provide a simple web interface using HTML5 and Javascript to demonstrate how to create calls to the FCC Clearinghouse APIs and manipulate the data received from those calls.  The data is combined with calls to CNET.com's product review APIs.  The demo illustrates one way to create a mashup of different data on the Internet.  The demo is entirely self-contained and does not require any additional files or software besides a web browser with Javascript enabled.  The use of HTML5 requires using an updated browser.  A warning will appear upon opening index.html if features of this demo are not supported in that browser.  The features of this demo should be supported in Internet Explorer 8 and 9.  

The demo is not up on a live site.  The files used in this demo are meant to be illustrative and provide guidance for others using the FCC Clearinghouse APIs.

The API URLs used in this demo were created using the Clearinghouse API Python SDK, which is available on the FCC's GitHub page.

Usage
-------
To use the demo, download clearinghouseDemo.zip, open the clearinghouseDemo folder, and open index.html in a web browser.  If a warning appears declaring that your web browser does support of the features of the site, open index.html in a different browser or install a newer version of the current browser.  

The demo takes the user through four steps to select a smartphone that contains features related to a user-selected disability.  The four  highest rated smartphones are displayed to the user as well as links to the CNET.com review of each phone.  

To use the demo, open index.html and continue through the steps on each page to see the results.

####Step 1
+ Select one of the disabilities from the 5 choices on the screen
+ Click the next button to continue

#### Step 2
+ Select one or more of the smartphone features associated with the disability chosen on the previous page
+ Click the next button to continue

#### Step 3
+ Select one of the smartphone manufacturers from the 6 choices on the screen
+ Click the next button to continue

#### Step 4
+ The user is presented with a list of four phones that contain the features selected in the second step
+ Click on one of the smartphones to see the CNET.com review of that phone

