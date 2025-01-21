const debug = true;
let idx = [];
$( (searchEndpoints) => {
  window.data = $.getJSON( "/search_endpoints.json", () => {
    if ( debug ) { console.log( "Setup okay." ); }
  } )
    .done( ( searchData ) => {
      if ( debug ) { console.log( "Loaded JSON data." ); }
      idx = new JsSearch.Search( "id" );
      idx.indexStrategy = new JsSearch.AllSubstringsIndexStrategy();
      idx.addIndex( "id" );
      idx.addIndex( "moduleName" );
      idx.addIndex( "path" );
      idx.addIndex( "interface" );
      idx.addIndex( "methods" );
      idx.addIndex( "apiDescription" );
      idx.addIndex( "apiType" );
      if ( debug ) { console.log( "Processing ..." ); }
      if ( debug ) { console.time( "Build index" ); }
      idx.addDocuments( searchData );
      if ( debug ) { console.timeEnd( "Build index" ); }
      const idxCount = searchData.length;
      if ( debug ) { console.log( `Ready: idx: ${ idxCount } items` ); }
      JsSearch.StopWordsMap.issue = false;
      JsSearch.StopWordsMap.environment = false;
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
    const urlRepoBase = "https://github.com/folio-org/";
    const urlS3Base = "https://s3.amazonaws.com/foliodocs/api/";
    if ( debug ) { console.log( `Hits: ${ results.length }` ); }
    if ( results.length ) {
      searchResults.empty();
      hits.html( `Hits: ${ results.length }` );
      const resultsSorted = results.sort(function(a, b) {
        return a.path.localeCompare(b.path);
      });
      resultsSorted.forEach( ( result ) => {
        if ( debug ) { console.log( `Result: ${ result.path }` ); }
        const urlRepo = `${ urlRepoBase }${ result.moduleName }`;
        const urlS3Repo = `${ urlS3Base }${ result.moduleName }`;
        const apath = result.apiDescription;
        const filenameDoc = apath.substring( apath.lastIndexOf( "/" ) + 1 );
        const basenameDoc = filenameDoc.replace( /\.[^/.]+$/, "" );
        const urlApiDesc = `${ urlRepo }/blob/master/${ result.apiDescription }`;
        const methods = result.methods.split( " " );
        let methodsList = "";
        methods.forEach( ( method ) => {
          const opParts = method.split( ":" );
          let nullNote = "";
          if  ( opParts[ 1 ] === "null" ) {
            nullNote = " (missing operationId)"
          }
          let urlS3 = `${ urlS3Repo }/`;
          if ( result.apiType === "RAML" ) {
            urlS3 += "p/";
          }
          urlS3 += `${ basenameDoc }.html#${ opParts[ 1 ] }`;
          methodsList += `<li><a href="${ urlS3 }">${ opParts[ 0 ] }</a> ${nullNote}</li>`;
        } );
        const appendString = `
          <li> ${ result.path }
            <ul>
              <li>module: <a href="${ urlRepo }">${ result.moduleName }</a></li>
              <li>interface: ${ result.interface } </li>
              <li>path: ${ result.path } </li>
              <li>methods:
                <ul>${ methodsList }</ul>
              </li>
              <li>api description: <a href="${ urlApiDesc }">${ result.apiDescription }</a></li>
              <li>api type: ${ result.apiType } </li>
            </ul>
          </li>
        `;
        searchResults.append( appendString );
      } );
    } else {
      hits.html( `Hits: 0` );
      searchResults.html( "<li>No results found.</li>" );
    }
  }

  $( "#searchEndpoints" ).submit( ( event ) => {
    event.preventDefault();
    const query = $( "#searchInput" ).val();
    if ( debug ) { console.log( `Query: ${ query }` ); }
    const results = idx.search( query );
    displayResults( results );
  } );
} );
