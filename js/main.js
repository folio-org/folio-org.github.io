$(function() {

    // $('.collapse').collapse('hide');
    $('.list-group-item.active').parent().parent('.collapse').collapse('show');

 
    var toc = $("#toc").tocify({
      selectors: 'h1, h2',
      extendPage: false,
      theme: 'none',
      smoothScroll: false,
      showEffectSpeed: 0,
      hideEffectSpeed: 180,
      ignoreSelector: '.toc-ignore',
      highlightOffset: 60,
      scrollTo: 50,
      scrollHistory: true,
      hashGenerator: function (text, element) {
        return element.prop('id');
      }
    }).data('toc-tocify');
	
 //   var pages = new Bloodhound({
 //       datumTokenizer: Bloodhound.tokenizers.obj.whitespace('title'),
        // datumTokenizer: Bloodhound.tokenizers.whitespace,
 //       queryTokenizer: Bloodhound.tokenizers.whitespace,

 //       prefetch: baseurl + '/search.json'
 //   });

//    $('#search-box').typeahead({
//        minLength: 0,
//        highlight: true
//    }, {
//        name: 'pages',
//        display: 'title',
//        source: pages
//    });

//    $('#search-box').bind('typeahead:select', function(ev, suggestion) {
//        window.location.href = suggestion.url;
//    });


    // Markdown plain out to bootstrap style
    $('#markdown-content-container table').addClass('table');
    $('#markdown-content-container img').addClass('img-responsive');


});
