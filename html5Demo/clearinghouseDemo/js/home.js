$(document).ready(function(){
	
	if(typeof(Storage)!=="undefined") { // the browser supports sessionStorage (and HTML 5)
		// disability ids
		var disabilityIds = {
			'hearing': 3,
			'deafblind': 4,
			'blind': 5,
			'mobility': 6,
			'cognitive': 7
		};
		
		/* 	check for disability id. If it exists, add the imgSelected
			class to the item in the list of disabilities */
		if ( sessionStorage.disabilityId ) {
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
			
			sessionStorage.disabilityId = disId;
		});
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
	});
	
});