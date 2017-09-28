var debug = false;
jQuery(function() {
  window.data = $.getJSON('/search_data.json', function() {
    if (debug) { console.log('Okay'); }
  })
  .done(function(searchData) {
    if (debug) { console.log('Got JSON data'); }
    window.idx = new JsSearch.Search('id');
    window.idx.addIndex('id');  
    window.idx.addIndex('title');  
    window.idx.addIndex('content');  
    window.idx.addIndex('categories');  
    if (debug) { console.log('Processing'); }
    if (debug) { console.time('Build index'); }
    window.idx.addDocuments(searchData);
    if (debug) { console.timeEnd('Build index'); }
    var idxCount = searchData.length;
    if (debug) { console.log('Ready: idx: ' + idxCount); }
    JsSearch.StopWordsMap.issue = false;
    JsSearch.StopWordsMap.environment = false;
  })
  .fail(function() {
    console.log('Error with getting search data');
  })
  .always(function() {
    if (debug) { console.log('Complete'); }
  });
 
  $('#searchDev').submit(function(event) {
    event.preventDefault();
    var query = $('#searchInput').val();
    if (debug) { console.log('Query: ' + query); }
    var results = window.idx.search(query);
    displayResults(results);
  });

  function displayResults(results) {
    var $searchResults = $('#searchResults');
    if (debug) { console.log('Hits: ' + results.length); }
    if (results.length) {
      $searchResults.empty();
      results.forEach(function(result) {
        if (debug) { console.log('Result: ' + result.url); }
        var appendString = '<li><a href="' + result.url + '">' + result.title + '</a></li>';
        $searchResults.append(appendString);
      });
    } else {
      $searchResults.html('<li>No results found.</li>');
    }
  }
});
