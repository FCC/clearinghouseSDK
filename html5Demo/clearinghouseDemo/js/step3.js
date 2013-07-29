$(document).ready(function(){
	
	if(typeof(Storage)!=="undefined") { // the browser supports sessionStorage (and HTML 5)
		if (sessionStorage.mfg) {
			var tdId = '#' + sessionStorage.mfg;
			$(tdId).addClass('mfgSelected');
		} else {
			$('#Samsung').addClass('mfgSelected');
		}
		
		$('#mfgTable td').hover(function() {
			$(this).addClass('mfgHover');
		}, function() {
			$(this).removeClass('mfgHover');
		});
		
		$('#mfgTable td').click(function() {
			$(this).parents('table').children().find('.mfgSelected').removeClass('mfgSelected');
			$(this).addClass('mfgSelected');
			
			var name = this.id;
			
			sessionStorage.mfg = name;
		});
	}
	
});