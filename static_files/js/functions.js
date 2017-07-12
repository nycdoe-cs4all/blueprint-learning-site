// Javascript functions

	
	
//scroll functions
$.fn.scrollView = function () {
    return this.each(function () {
        $('html, body').animate({
            scrollTop: $(this).offset().top - 64
        }, 1000);
    });
}



// Run on Document Ready
$( document ).ready(function() {
    
    
    
    // Colorbox
    $('a.embed').each(function() {
    	vidTitle = $(this).attr('data-title');
    	vidSubtitle = $(this).attr('data-subtitle');
    	if ( vidSubtitle ) {
    		vidTitle = vidTitle + ' <span class="subtitle">' + vidSubtitle + '</span>';
    	}
    	$(this).colorbox({iframe:true, transition:'fade', innerWidth:1920, innerHeight:1080, maxWidth:'100%', maxHeight:'100%', title: vidTitle, opacity: 1 });
    });
    
    
    $('a[href^="#"]').click(function(event) {
    	event.preventDefault();
    	targetDiv = $(this).attr('href');
    	$(targetDiv).scrollView();
    });
    
    
    
    // Change things when scrolling begins
//    var waypoints = $(window).waypoint({
//    	handler: function(direction) {
//    		if (direction == 'down') {
//    			$("body").addClass('scrolling');
//        	} else {
//    			$("body").removeClass('scrolling');
//    		}
//    	},
//    	offset: '-60'
//    })
    
    
    
    // Determine whether or not to show intro animation
    animation = $.cookie('animation');
    if ( animation == 'viewed' ) {
    	$('body').removeClass('animation');
    }
    
    
    
});



// Run on load
$(window).load( function() {
		
	$('body').removeClass('preload');
	
	$.cookie('animation', 'viewed', { expires: 7, path: '/' }); // Set a cookie to indicate animation has been viewed

});



// Run on Ajax Complete
$( document ).ajaxComplete(function( event, request, settings ) {
	  
});

	

// Run layout functions when the window is resized
$( window ).resize(function() {
	
	clearTimeout(resizeTimer);
	resizeTimer = setTimeout(function() {
	

	        
	}, 250);
	
});
	

