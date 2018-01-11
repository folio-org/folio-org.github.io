# Maintenance of search facilities

An ongoing maintenance task is to verify the generated search index. Sometimes strange characters in content are not escaped or handled properly, and that causes invalid JSON. Also some pages should not be indexed.

The data file is generated using Liquid processing in ./search_data.json into _site/search_data.json
It can exclude specific pages, and transform content.

Use 'jq' to display and validate the JSON:

```
cat _site/search_data.json | jq
cat _site/search_data.json | jq '.[].id'
du -sh _site/search_data.json
```

See FOLIO-860, FOLIO-859, FOLIO-871
