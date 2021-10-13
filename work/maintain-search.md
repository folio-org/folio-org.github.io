# Maintenance of search facilities

An ongoing maintenance task is to verify the generated search index. Sometimes strange characters in content are not escaped or handled properly, and that causes invalid JSON. Also some pages should not be indexed.

The data file is generated using Liquid processing in `./search_data.json` into the `_site/search_data.json` file.

It can exclude specific pages, and transform content.

Use 'jq' to display and validate the output JSON:

```
cat _site/search_data.json | jq
cat _site/search_data.json | jq '.[].id'
cat _site/search_data.json | jq '.[].title'
du -sh _site/search_data.json
```

Also ensure when adding new Liquid-based content, that there is no raw Liquid program content (`{%`) in the data file.
This is a sign that something is amiss, and the real content could be missing from the search system.

See FOLIO-860, FOLIO-859, FOLIO-871
