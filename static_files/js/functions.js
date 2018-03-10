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
    
        
    $('a.toggle').click(function(event) {
        event.preventDefault();
        targetDiv = $(this).attr('href');
        $(targetDiv).toggleClass('active');
    });
    
    
    $('a.accordion').click(function(event) {
            event.preventDefault();
            targetDiv = $(this).attr('href');
            $(targetDiv).siblings().addClass('compressed');
            $(targetDiv).toggleClass('compressed');
            if ( !$(targetDiv).hasClass('compressed') ) {
                setTimeout(function() {
                    $(targetDiv).scrollView();
                }, 500);
            } else {
    
            }
        });
    
    
    $('a.scroll').not('.accordion').click(function(event) {
        event.preventDefault();
        targetDiv = $(this).attr('href');
        $(targetDiv).scrollView();
    });
    
    

    
    
    
    $('td').hover(function() {
        targetTh = $(this).attr('data-header');
        $('#' + targetTh).addClass('current');
    }, function() {
        targetTh = $(this).attr('data-header');
        $('#' + targetTh).removeClass('current');
    });
    
    
    
    // Change things when scrolling begins
//    var waypoints = $(window).waypoint({
//      handler: function(direction) {
//          if (direction == 'down') {
//              $("body").addClass('scrolling');
//          } else {
//              $("body").removeClass('scrolling');
//          }
//      },
//      offset: '-60'
//    })
    
    
    
    // Determine whether or not to show intro animation
//    animation = $.cookie('animation');
//    if ( animation == 'viewed' ) {
//      $('body').removeClass('animation');
//    }
    
    
    
});



// Run on load
$(window).load(function() {
    
    $('#menu .site-menu li ul').each(function() {
        submenuHeight = $(this).height();
        $(this).css('height', submenuHeight);
        $(this).parent('li').addClass('compressed parent-menu');        
    });
    $('.parent-menu > a').click(function(event) {
        event.preventDefault();
        $(this).parent('li').toggleClass('compressed');
    });
    
    $('#page-menu .options').each(function() {
        submenuHeight = $(this).height();
        $(this).css('height', submenuHeight);
        $(this).parent('fieldset').addClass('compressed');      
    });
    $('#page-menu legend a').click(function(event) {
        event.preventDefault();
        $(this).closest('fieldset').toggleClass('compressed');
    });
    
    $('.article-content .read-more').each(function() {
        submenuHeight = $(this).height();
        $(this).css('height', submenuHeight);
        $(this).parent('.article-content').addClass('compressed');      
    });
    $('.article-content a.open').click(function(event) {
        event.preventDefault();
        $(this).closest('.article-content').toggleClass('compressed');
    });
        
    $('body').removeClass('preload');
    
//  $.cookie('animation', 'viewed', { expires: 7, path: '/' }); // Set a cookie to indicate animation has been viewed

    $('.accordion-target .section-content').each(function() {
        divHeight = $(this).height();
        $(this).css('height', divHeight);
        $(this).parent('.accordion-target').addClass('compressed');
    });
    if (window.location.hash) {
        var hash = document.URL.substr(document.URL.indexOf('#')+1);
        $('#' + hash).removeClass('compressed');
        setTimeout(function() {
            $('#' + hash).scrollView();
        }, 500);
    }
    


});



// Run on Ajax Complete
$( document ).ajaxComplete(function( event, request, settings ) {
      
});


// Run layout functions when the window is resized
var resizeTimer;

$(window).on('resize', function(e) {

    $('.accordion-target .section-content').css('height', '');
    
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function() {

        $('.accordion-target .section-content').each(function() {
            var reclose = false;
            if ( $(this).parent('.accordion-target').hasClass('compressed') ) {
                $(this).parent('.accordion-target').removeClass('compressed');
                reclose = true;
            }
            divHeight = $(this).height();
            $(this).css('height', divHeight);
            if ( reclose == true ) {
                $(this).parent('.accordion-target').addClass('compressed');
            }
        });
        
    }, 250);

});


