  tocbot.init({
    headingSelector: 'h1, h2, h3',
	//
    positionFixedSelector: '#js-toc-fixed'
  });
  
$(function() {

    // $('.collapse').collapse('hide');
   // $('.list-group-item.active').parent().parent('.collapse').collapse('show');

    // Markdown plain out to bootstrap style
  //  $('#markdown-content-container table').addClass('table');
  //  $('#markdown-content-container img').addClass('img-responsive');
    $('h1, h2, h3').addClass('anchor');

});

