  tocbot.init({
    headingSelector: 'h1, h2, h3',
    positionFixedSelector: '#js-toc-fixed'
  });
  
$(function() {
    // $('.collapse').collapse('hide');
   // $('.list-group-item.active').parent().parent('.collapse').collapse('show');

    // Markdown plain out to bootstrap style
  //  $('#markdown-content-container table').addClass('table');
  //  $('#markdown-content-container img').addClass('img-responsive');
  $('#js-toc-fixed').css({ "margin-top": "10em" });
    if ( $('#js-toc-fixed ol:first li').length > 0 ) {
    $('#js-toc-fixed ol:first').prepend('<li class="toc-list-item"><a class="toc-link" href="">Top</a></li>');
  }
    $('h1, h2, h3').addClass('anchor');
});

