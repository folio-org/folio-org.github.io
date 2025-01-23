var debug = false;
let idx = [];
$( (searchDev) => {
  window.data = $.getJSON( "/search_data.json", () => {
    if ( debug ) { console.log( "Setup okay." ); }
  } )
    .done( ( searchData ) => {
      if ( debug ) { console.log( "Loaded JSON data." ); }
      const indexCount = $( "#indexCount" );
      idx = new JsSearch.Search( "id" );
      idx.indexStrategy = new JsSearch.PrefixIndexStrategy();
      idx.addIndex( "title" );
      idx.addIndex( "content" );
      idx.addIndex( "categories" );
      if ( debug ) { console.log( "Processing ..." ); }
      if ( debug ) { console.time( "Build index" ); }
      idx.addDocuments( searchData );
      if ( debug ) { console.timeEnd( "Build index" ); }
      const idxCount = searchData.length;
      if ( debug ) { console.log( `Ready: idx: ${ idxCount } items` ); }
      indexCount.html( `Number of items in search index: ${ idxCount }` );
    } )
    .fail( () => {
      console.log( "Error with getting search data." );
    } )
    .always( () => {
      if ( debug ) { console.log( "Complete." ); }
    } );

  function displayResults( results ) {
    const searchResults = $( "#searchResults" );
    const hits = $( "#hits" );
    if ( debug ) { console.log( `Hits: ${ results.length }` ); }
    if ( results.length ) {
      searchResults.empty();
      hits.html( `Hits: ${ results.length }` );
      results.forEach( ( result ) => {
        if ( debug ) { console.log( `Result: ${ result.url }` ); }
        const appendString = `<li><a href="${ result.url }">${ result.title }</a></li>`;
        searchResults.append(appendString);
      } );
    } else {
      hits.html( `Hits: 0` );
      searchResults.html( "<li>No results found.</li>" );
    }
  }

  $( "#searchDev" ).submit( ( event ) => {
    event.preventDefault();
    const query = $( "#searchInput" ).val();
    if ( debug ) { console.log( `Query: ${ query }` ); }
    const results = idx.search( query );
    displayResults( results );
  } );
} );
