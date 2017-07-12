$.fn.scrollView = function() {
  return this.each(function() {
    $('html, body').animate({
      scrollTop: $(this).offset().top - 64
    }, 1000);
  });
}


// Run on Document Ready
$(document).ready(function() {
  // Colorbox
  $('a.embed').each(function() {
    vidTitle = $(this).attr('data-title');
    vidSubtitle = $(this).attr('data-subtitle');
    if (vidSubtitle) {
      vidTitle = vidTitle + ' <span class="subtitle">' + vidSubtitle + '</span>';
    }
    $(this).colorbox({
      iframe: true,
      transition: 'fade',
      innerWidth: 1920,
      innerHeight: 1080,
      maxWidth: '100%',
      maxHeight: '100%',
      title: vidTitle,
      opacity: 1
    });
  });

  $('a[href^="#"]').click(function(event) {
    event.preventDefault();
    targetDiv = $(this).attr('href');
    $(targetDiv).scrollView();
  });
});
