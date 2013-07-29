$(document).ready(function(){
	
	if(typeof(Storage)!=="undefined") { // the browser supports sessionStorage (and HTML 5)
	
		// Create list of current features, if featureList exists
		if (sessionStorage.featureList) { featureList = sessionStorage.featureList.split(','); }
		else { sessionStorage.featureList = ''; featureList = []; }
		
		// if a disability was selected on the previous screen, make the API call
		if (sessionStorage.disabilityId) {
			disId = sessionStorage.disabilityId;
			var disStr = '&disabilityId=' + String(disId);
			// url created from Clearinghouse Python SDK
			var url = 'http://data.fcc.gov/api/accessibilityclearinghouse/featureGroups?api_key=9SETg07EtIkOJtUYC7b1xMsNQlStuf8w5fVvb5AN&format=jsonp&jsonCallback=myFunc' + disStr;
			
			// run ajax request
			var result = $.ajax({
				type: 'GET',
				url: url,
				async: false,
				contentType: "application/json",
				dataType: 'jsonp',
				jsonpCallback: 'myFunc',
				success: function(data) {
					// the request was successful
					if (data.FeatureGroup) {
						// add overflow to contentBody
						$('#contentBody').css('overflow', 'auto');
						
						var table = $('#featuresTable tbody');
						
						var tdFlag = true;
						var rowText = '<tr>';
						$.each(data.FeatureGroup[0].featureList, function (i, item) {
							tdFlag = true;
							var listVal = featureList.indexOf(String(item.id));
							var isChecked = '';
							
							// one or more features are checked, make next button visible
							if (listVal > -1) {
								isChecked = 'checked';
								$('#nextBtn').removeClass('invisible');
							}
							// create a new column in the table
							rowText += '<td><label><input type="checkbox" name="' + item.id + '" ' + isChecked + ' value="' + item.name + '">' + item.name + '</label></td>';
							if (i%3 == 2) { // end current row, create new row
								rowText += '</tr>';
								table.append(rowText);
								rowText = '<tr>';
								tdFlag = false;
							}
						}); // END each
						
						// if row end with two or one columns, end the row
						if (tdFlag) {
							rowText += '</tr>';
							table.append(rowText);
							rowText = '';
						}
					} else { // there was an error!
						var table = $('#featuresTable tbody');
			
						table.append('<tr><td class="error"><h3>Oops! Looks like we are having trouble <br /> connecting to the server. Please try again.</h3></td></tr>');
					}
					
					// add click handler to every checkbox
					$('#featuresTable input[type="checkbox"]').change( function() {
						var name = this.name;
						var listVal;
						
						// get featureList if it exists
						if (sessionStorage.featureList) { 
							featureList = sessionStorage.featureList.split(',');
							listVal = featureList.indexOf(name);
						}
						else { listVal = -1 }
						
						// the feature is not currently in the featureList so add it
						if (this.checked && (listVal == -1)) {
							if (listVal == -1) {
								featureList.push(name);
								sessionStorage.featureList = featureList.toString();
								$('#nextBtn').removeClass('invisible');
							}
						} else {
							// unchecked, remove feature from featureList
							featureList = jQuery.grep(featureList, function(value) {
								return value != name;
							});
							// re-save featureList to sessionStorage
							sessionStorage.featureList = featureList.toString();
							if (featureList.length < 1) {
								$('#nextBtn').addClass('invisible');
							}
						}
					});
				},
				error: function(e) {
					console.log(e.message);
				}
			});
		} else { // disability id not set, cannot run JSON request. Display an error.
			var table = $('#featuresTable tbody');
			
			table.append('<tr><td class="error"><h3>Oops! Looks like there was an error. Be sure <br /> to select a disability type from the previous page</h3></td></tr>');
		}
	}
	
});