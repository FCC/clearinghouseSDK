$(document).ready(function(){
	
	if(typeof(Storage)!=="undefined") { // the browser supports sessionStorage (and HTML 5)
		
		// url created from Clearinghouse Python SDK
		var url = 'http://data.fcc.gov/api/accessibilityclearinghouse/product/products?api_key=9SETg07EtIkOJtUYC7b1xMsNQlStuf8w5fVvb5AN&category=mobile&format=jsonp&jsonCallback=myFunc&rowPerPage=-1&region=North%20America';
		var productArray = [];
		var includedPhones = [];
		var cnetVals;
		
		var featureList;
		if (sessionStorage.featureList) {
			featureList = sessionStorage.featureList.split(',');
		}
		
		var mfg;
		var mfgStr;
		if (sessionStorage.mfg) {
			mfgStr = '&mfg=' + sessionStorage.mfg;
			mfg = sessionStorage.mfg;
			if (mfg == 'Motorola') {
				mfgStr += '%20Mobility';
			} else if (mfg == 'RIM') {
				mfg = 'Blackberry';
			}
		}
		else { mfgStr = ''; mfg = false; }
		
		var features = '';
		
		$.each(featureList, function(i, feature) {
			features += '&feat=' + feature;
		});
		
		// add features and manufacturer to url
		url = url + features + mfgStr;
		
		// run ajax request
		var result = $.ajax({
			type: 'GET',
			url: url,
			async: false,
			contentType: "application/json",
			dataType: 'jsonp',
			jsonpCallback: 'myFunc',
			error: function(e) {
				console.log(e.message);
			}
		});
		
		// wait for ajax request to finish, add phone names to search query
		$.when(result).done(function(data) {
			var query = mfg;
			$.each(data.Product, function(i, item) {
				if (item.maker && item.modelNumber) {
					var searchName = '%20' + item.modelNumber;
					searchName = searchName.replace(/\s+/, '%20');
					query += searchName;
				}
				productArray.push(searchName);
			});
			cnetVals = getRatedPhones(query);
			
			// wait for CNET ajax request to finish
			$.when(cnetVals).done(function(data){
				
				var table = $('#resultsTable tbody');
				
				if (data.CNETResponse.TechProducts.TechProduct) {
					var rowText = '<tr>';
					var itemCount = 0;
					// get tech product from JSON object
					$.each(data.CNETResponse.TechProducts.TechProduct, function(i, item) {
						if (itemCount < 4) {
							var name = item.Name.$;
							if (name.toLowerCase().indexOf(mfg.toLowerCase()) > -1) {
								// create new table column with phone image, name, and link to CNET review
								rowText += '<td><a href="' + item.ReviewURL.$ + '" target="_blank" title="CNET Review"><img src="' + item.ImageURL[1].$ + '" width="120" alt="' + item.Name.$ + '" /><h4>' + item.Name.$ + '</h4></a></td>';
								if (itemCount == 1) { // end this row, start new row
									rowText += '</tr>';
									table.append(rowText);
									rowText = '<tr>';
								}
								itemCount += 1;
							}
						}
					});
					rowText += '</tr>';
					table.append(rowText);
					rowText = '';
				} else { // and error occurred
					table.append('<tr><td class="error"><h3>Oops! Looks like there was an error <br />. Please try reloading the page.</h3></td></tr>');
				}
				
				// remove loading icon after table has been created
				$('#loader').fadeOut(500, function() {
					$('#loader').remove();
					table.css('visibility', 'visible');
				});
			
			});
		});
		
		// runs ajax request for CNET.com APIs
		function getRatedPhones(searchTerm) {
			// search query with all phone names included
			var query = '&query=' + searchTerm;
			var url = 'http://developer.api.cnet.com/rest/v1.0/techProductSearch?viewType=json&callback=myFunc&partKey=5wx3nw8gstqshnvhszufpnrh&partTag=5wx3nw8gstqshnvhszufpnrh&categoryId=6454&iod=none&orderBy=editorsRating&sortDesc=true&start=0&limit=20' + query;

			return $.ajax({
				type: 'GET',
				url: url,
				async: false,
				contentType: "application/json",
				dataType: 'jsonp',
				jsonpCallback: 'myFunc',
				error: function(e) {
					console.log(e.message);
				}
			});
		}
	}
	
});