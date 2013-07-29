$(document).ready(function(){
	
	// fade in body
	$('body').css('display', 'none');
	$('body').fadeIn(1000);
	
	if(typeof(Storage)!=="undefined") { // the browser supports sessionStorage (and HTML 5)
	
		// page positions
		var pagePositions = ['index.html', 'step2.html', 'step3.html', 'results.html'];
		
		if ( sessionStorage.currentPosition ) { currentPos = parseInt(sessionStorage.currentPosition); }
		else { currentPos = 0; }
		
		// move current nav position
		var leftPos = -7 + 150 * currentPos;
		$('#currentNav').css('left', leftPos);
	
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
	} else {
		alert('WARNING!\nIt looks like you are running a version of a browser that does not support some the features of this site. Trying running this site in a different browser or a newer version of your current browser.');
	}
	
	// handle fades btwn pages
	$("a.transition").click(function(event){
        event.preventDefault();
        linkLocation = this.href;
        $("body").fadeOut(1000, redirectPage);      
    });
         
    function redirectPage() {
        window.location = linkLocation;
    }
	
	// logo hover slide
	$('#logos').hover(function() {
		$('#logos').animate({'width': 230}, 500);
	}, function() {
		$('#logos').animate({'width': 30}, 500, function() {
			$('#logos').stop(true, true);
		});
	});
	
});