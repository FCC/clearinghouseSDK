$(document).ready(function(){

	// fade in body
	$('body').css('display', 'none');
	$('body').fadeIn(1000);
	
	// disability ids
	var disabilityIds = {
		'hearing': 3,
		'deafblind': 4,
		'blind': 5,
		'mobility': 6,
		'cognitive': 7
	};
	
	// page positions
	var pagePositions = ['index.html', 'step2.html', 'step3.html', 'results.html'];
	
	if(typeof(Storage)!=="undefined") {
		alert('storage available');
	} else {
		alert('storage NOT available!');
	}
	
	if ( sessionStorage.currentPosition != null ) { currentPos = parseInt(sessionStorage.currentPosition)}
	else { currentPos = 0 }
	//var currentPos = 0;
	
	var leftPos = -7 + 150 * currentPos;
	$('#currentNav').css('left', leftPos);
	
	// check if on index page
	var pathname = window.location.pathname;
	if ( (pathname.indexOf('index.html') > -1) && (sessionStorage.disabilityId) ) {
		disId = sessionStorage.disabilityId;
		for (disability in disabilityIds) {
			if (disabilityIds[disability] == disId) {
				var tdId = '#' + disability;
				$(tdId).addClass('imgSelected');
				$('#nextBtn').removeClass('invisible');
				break;
			}
		}
	}
	
	// check if on step 3 page
	var pathname = window.location.pathname
	if ( pathname.indexOf('step3.html') > -1 ) {
		if (sessionStorage.mfg) {
			var tdId = '#' + sessionStorage.mfg;
			$(tdId).addClass('carrierSelected');
		} else {
			$('#Samsung').addClass('carrierSelected');
		}
	}
	
	// check if on step2 page
	
	var pathname = window.location.pathname
	if (pathname.indexOf('step2.html') > -1) {
		if (sessionStorage.featureList) { featureList = sessionStorage.featureList.split(','); }
		else { sessionStorage.featureList = ''; featureList = []; }
		
		if (sessionStorage.disabilityId) {
			disId = sessionStorage.disabilityId;
			var disStr = '&disabilityId=' + String(disId);
			//var url = 'js/features.json';
			//var url = 'http://data.fcc.gov/api/accessibilityclearinghouse/featureGroups?api_key=9SETg07EtIkOJtUYC7b1xMsNQlStuf8w5fVvb5AN?jsoncallback=myFunc' + disStr;
			//var url = 'http://api.flickr.com/services/feeds/photos_public.gne?jsoncallback=?';
			var url = 'http://data.fcc.gov/api/accessibilityclearinghouse/featureGroups?api_key=9SETg07EtIkOJtUYC7b1xMsNQlStuf8w5fVvb5AN&format=jsonp&jsonCallback=myFunc' + disStr;
			
			//var url = 'http://www.jquery4u.com/scripts/jquery4u.settings.json';
			console.log('url: ' + url);
			function myFunc (data) {
				console.log('data: ' + data);
			}
			var result = $.ajax({
			   type: 'GET',
				url: url,
				async: false,
				contentType: "application/json",
				dataType: 'jsonp',
				jsonpCallback: 'myFunc',
				success: function(data) {
					// add overflow to contentbody
					$('#contentBody').css('overflow', 'auto');
					
					var table = $('#featuresTable tbody');
					
					var tdFlag = true;
					table.append('<tr>');
					$.each(data.FeatureGroup[0].featureList, function (i, item) {
						tdFlag = true;
						//console.log('id type: ' + $.type(item.id));
						var listVal = featureList.indexOf(String(item.id));
						var isChecked = '';
						//console.log('adding on: ' + checkboxName);
						
						if (listVal > -1) {
							isChecked = 'checked';
							$('#nextBtn').removeClass('invisible');
						}
						
						table.append('<td><input type="checkbox" name="' + item.id + '" ' + isChecked + ' value="' + item.name + '">' + item.name);
						if (i%3 == 2) { // new row
							console.log('new row: ' + i);
							table.append('</tr><tr>');
							tdFlag = false;
						}
						//console.log(i + ': ' + item.name);
					}); // END each
					
					if (tdFlag) {
						console.log('adding row at end');
						table.append('</tr>');
					}
					
					$('#featuresTable input[type="checkbox"]').change( function() {
						var name = this.name;
						var listVal;
						if (sessionStorage.featureList) { 
							featureList = sessionStorage.featureList.split(',');
							listVal = featureList.indexOf(name);
						}
						else { listVal = -1 }
						
						if (this.checked && (listVal == -1)) {
							if (listVal == -1) {
								featureList.push(name);
								sessionStorage.featureList = featureList.toString();
								$('#nextBtn').removeClass('invisible');
							}
						} else {
							// unchecked
							featureList = jQuery.grep(featureList, function(value) {
								return value != name;
							});
							sessionStorage.featureList = featureList.toString();
							console.log('length: ' + featureList.length);
							if (featureList.length < 1) {
								$('#nextBtn').addClass('invisible');
							}
						}
					});
					//console.log(data);
				},
				error: function(e) {
					console.log(e.message);
				}
			});
			
			/*var result = $.ajax({
							type: 'GET',
							async: false,
							url: url,
							jsonpCallback: 'myFunc',
							contentType: 'application/json',
							dataType: 'jsonp',
							success: function(data) {
								console.log(data);
							},
							error: function(e) {
								console.log(e.message);
							}
						});*/
							
			/*var result = $.getJSON(url, {
								tags: "jquery",
								tagmode: "any",
								format: "json"
							}, function(json) {
								$.each(json.items, function (i, items) {
									console.log(i + ': ' + items.title);
								});
								//console.log(json);
							});*/
			/*for (key in result) {
				console.log('key: ' + key + ' ******* result: ' + result[key]);
			}*/
			console.log('result: ' + result);
		} else { // disability id not set, cannot run JSON request
			
		}
	}
	
	// handle checkbox select or deselect
	$('#featuresTable input[type="checkbox"]').hover( function() {
		console.log('td hover');
	});
	
	// handle changes to current position
	$('a').click( function(event) {
		for (var i in pagePositions) {
			if ( this.href.indexOf(pagePositions[i]) > -1 ) {
				newLocale = i;
				break;
			} else {
				newLocale = currentPos;
			}
		}
		sessionStorage.currentPosition = newLocale;
	});
	
	// handle fades btwn pages
	$("#nextBtn a.transition").click(function(event){
        event.preventDefault();
		//sessionStorage.currentPosition = currentPos + 1;
        linkLocation = this.href;
        $("body").fadeOut(1000, redirectPage);      
    });
	
	// handle fades btwn pages
	$("#prevBtn a.transition").click(function(event){
        event.preventDefault();
		//sessionStorage.currentPosition = currentPos - 1;
        linkLocation = this.href;
        $("body").fadeOut(1000, redirectPage);      
    });
         
    function redirectPage() {
        window.location = linkLocation;
    }
	
	$('#disabilityTable td').hover(function() {
		$(this).addClass('imgHover');
	}, function() {
		$(this).removeClass('imgHover');
	});
	
	$('#disabilityTable td').click(function() {
		$(this).parents('table').children().find('.imgSelected').removeClass('imgSelected');
		$(this).addClass('imgSelected');
		
		$('#nextBtn').removeClass('invisible');
		var name = this.id;
		var disId = disabilityIds[name];
		
		sessionStorage.firstNav = true;
		sessionStorage.disabilityId = disId;
	});
	
	$('#carrierTable td').hover(function() {
		$(this).addClass('carrierHover');
	}, function() {
		$(this).removeClass('carrierHover');
	});
	
	$('#carrierTable td').click(function() {
		$(this).parents('table').children().find('.carrierSelected').removeClass('carrierSelected');
		$(this).addClass('carrierSelected');
		
		var name = this.id;
		
		sessionStorage.mfg = name;
	});
	
	$('#logos').hover(function() {
		$('#logos').animate({'width': 230}, 500);
	}, function() {
		$('#logos').animate({'width': 30}, 500);
	});
	
});