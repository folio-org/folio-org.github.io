---
layout: null
---

## Overview

`mod-search` is based on metadata-driven approach. It means that resource description is specified using JSON file and
all rules, mappings and other thing will be applied by internal mod-search services.

### Supported search field types

Elasticsearch mapping field
types: [field data types](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html)
The field type is used to define what search capabilities the corresponding field can provide. For example,
`keyword` field type is used
for [term queries](https://www.elastic.co/guide/en/elasticsearch/reference/current/term-level-queries.html)
and [aggregations](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations.html)
(providing facets for the record). The text fields are intended to use by
the [full-text queries](https://www.elastic.co/guide/en/elasticsearch/reference/current/full-text-queries.html).

#### Resource description

| Property name        | Description                                                                                                                                                                                                                                                                                     |
|:---------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| name                 | The resource name, it used for searching by resource to determine index name, creating index settings and mappings                                                                                                                                                                              |
| parent               | The parent resource name (currently, it is used for browsing by subjects when the additional index is added to arrange the instance subjects uniquely)                                                                                                                                          |
| eventBodyJavaClass   | The Java class that incoming JSON can be mapped to. Currently, it's used to make processing of search field more convenient                                                                                                                                                                     |
| languageSourcePaths  | Contains a list of json path expressions to extract languages values in ISO-639 format. If the multi-language is supported for the resource, this path must be specified.                                                                                                                       |
| searchFieldModifiers | Contains a list of field modifiers, which pre-processes incoming fields for elasticsearch request.                                                                                                                                                                                              |
| fields               | List of field descriptions to extract values from incoming resource event                                                                                                                                                                                                                       |
| fieldTypes           | List of resource descriptions that can be used with an alias using `$ref` field of `PlainFieldDescription`. It's done to reduce duplication in resource description.                                                                                                                            |
| searchFields         | Contains a list of generated fields for the resource events (for example, It can be contain ISBN normalized values or generating subset of field values).                                                                                                                                       |
| indexMappings        | Object with additional index mappings for resource (It can be helpful for `copy_to` functionality of Elasticsearch                                                                                                                                                                              |
| mappingSource        | It's used to include or exclude some field from storing those values in `_source` object in Elasticsearch. Mainly, it's used to reduce the size per index. See also: [_source field](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-source-field.html#include-exclude) |
| reindexSupported     | Indicates if the resource could be reindexed                                                                                                                                                                                                                                                    |

#### Supported field description types

| Field type | Description                                                                                                                                                                                                   |
|:-----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| plain      | This field type is default and there is no need to explicitly specify the field.<br/> It can be used to define all fields containing the following values: string, number, boolean, or array of plain values. |
| object     | This field type is used to mark that key contains subfield, each of subfield must have its own field description.                                                                                             |
| authority  | This field type is designed to provide special options to divide a single authority record into multiple based on the `distinctType` property value.                                                          |

#### Plain field description

| Property name       | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|:--------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| searchTypes         | List of search types that are supported for the current field. Allowed values: `facet`, `filter`, `sort`                                                                                                                                                                                                                                                                                                                                                   |
| searchAliases       | List of aliases that can be used as a field name in the CQL search query. It can be used to combine several fields together during the search. For example, a query `keyword all title` combines for instance record following fields - `title`, `alternativeTitles.alternativeTitle`,  `indexTitle`, `identifiers.value`, `contributors.name`<br/>Other way of using it - is to rename field keeping the backward compatibility without required reindex. |
| index               | Reference to the Elasticsearch mappings that are specified in [index-field-types](src/main/resources/elasticsearch/index-field-types.json)                                                                                                                                                                                                                                                                                                                 |
| showInResponse      | Marks field to be returned during the search operation. `mod-search` adds to the Elasticsearch query all marked field paths. See also: [Source filtering](https://www.elastic.co/guide/en/elasticsearch/reference/master/search-fields.html#source-filtering)                                                                                                                                                                                              |
| searchTermProcessor | Search term processor, which pre-processes incoming value from CQL query for the search request.                                                                                                                                                                                                                                                                                                                                                           |
| mappings            | Elasticsearch fields mappings. It can contain new field mapping or can enrich referenced mappings, that comes from `index-field-types`                                                                                                                                                                                                                                                                                                                     |
| defaultValue        | The default value for the plain field                                                                                                                                                                                                                                                                                                                                                                                                                      |
| indexPlainValue     | Specifies if plain keyword value should be indexed with field or not. Works only for full-text fields. See also: [Full-text plain fields](#full-text-plain-fields)                                                                                                                                                                                                                                                                                         |
| sortDescription     | Provides sort description for field. If not specified - standard rules will be applied for the sort field. See also: [Sorting by fields](#field-sorting)                                                                                                                                                                                                                                                                                                   |

#### Object field description

| Property name | Description                                                            |
|:--------------|:-----------------------------------------------------------------------|
| properties    | Map where key - is the subfield name, value - is the field description |

#### Authority field description

| Property name | Description                                                                                                                                |
|:--------------|:-------------------------------------------------------------------------------------------------------------------------------------------|
| distinctType  | Distinct type to split single entity to multiple containing only common fields excluding all other fields marked with other distinct types |
| headingType   | Heading type that should be set to the resource if a field containing some values.                                                         |
| authRefType   | Authorized, Reference, or Auth/Ref type for divided authority record.                                                                      |

### Creating Elasticsearch mappings

Elasticsearch mappings are created using field descriptions. All fields, that are specified in the record description
will be added to the index mappings, and they will be used to prepare the
[Elasticsearch document](https://www.elastic.co/guide/en/elasticsearch/reference/current/documents-indices.html).

By default, mappings are taken from [index-field-types](src/main/resources/elasticsearch/index-field-types.json). It's
the common file containing pre-defined mapping values that can be accessed by reference from `index` field of
`PlainFieldDescription`. The field mappings for specific field can be enriched using `mapping` field. Also,
the `ResourceDescription` contains section `indexMappings` which provides for developers to add custom mappings without
specifying them in the `index-field-types.json` file.

For example, the resource description contains the following field description:

```json
{
  "fields": {
    "f1": {
      "index": "keyword",
      "mappings": {
        "copy_to": [ "sort_f1" ]
      }
    },
    "f2": {
      "index": "keyword"
    }
  },
  "indexMappings": {
    "sort_f1": {
      "type": "keyword",
      "normalizer": "keyword_lowercase"
    }
  }
}
```

Then the mappings' helper will create the following mappings object:

```json
{
  "properties": {
    "f1": {
      "type": "keyword",
      "copy_to": [ "sort_f1" ]
    },
    "f2": {
      "type": "keyword"
    },
    "sort_f1": {
      "type": "keyword",
      "normalizer": "keyword_lowercase"
    }
  }
}
```

### Full-text fields

Currently, supported 2 field types for full-text search:
* multi-language field values (see also: [Language Analyzers](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-lang-analyzer.html))
* standard tokenized field values (see also: [Standard Tokenizer](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-standard-tokenizer.html))

Also, to support the `wildcard` search by the whole phrase the plain values are added to the generated document. For
example, multi-language analyzed field with `indexPlainValue = true` (default):

Source record:
```json
{
  "title": "Semantic web primer",
  "language": "eng"
}
```

Result document:
```json
{
  "title": {
    "eng": "Semantic web primer",
    "src": "Semantic web primer"
  },
  "plain_title": "Semantic web primer"
}
```

Example of document with field with index = `standard`:

Source:
```json
{
  "contributors": [
    {
      "name": "A contributor name",
      "primary": true
    }
  ]
}
```

Result document:
```json
{
  "contributors": [
    {
      "name": "A contributor name",
      "plain_name": "A contributor name",
      "primary": true
    }
  ]
}
```

### Field Sorting

All fields marked with `searchType = sort` must be available for [sorting](https://www.elastic.co/guide/en/elasticsearch/reference/current/sort-search-results.html).
To sort by text values following field indices can be applicable:

* `keyword` (case-sensitive)
* `keyword_lowercase` (case-insensitive)

#### Sort Description

| Property name | Description                                                                                                      |
|:--------------|:-----------------------------------------------------------------------------------------------------------------|
| fieldName     | Custom field name, if it is not specified - default strategy will be applied: `sort_${fieldName}`.               |
| sortType      | Sort field type: `single` or `collection`                                                                        |
| secondarySort | List of fields that must be added as secondary sorting (eg, sorting by `itemStatus` and instance `title` fields) |

By default, if the field is only marked with `searchType = sort` - the `mod-search` will generate the following sort
condition:

```json
{
  "sort": [
    {
      "name": "sort_$field",
      "order": "${value comes from cql query: asc/desc}"
    }
  ]
}
```

if `sortDescription` contains `sortTYpe` as `collection` the following rules will be applied:
* if `sortOrder` is `asc` then the `mode` will be equal to `min`. It means that for sorting by a field containing a list of values - the lowest value will be picked for sorting.
* if `sortOrder` is `desc` the the `mode` will be equal to `max`. It means that for sorting by a field containing a list of values - the highest value will be picked for sorting.

## Testings

### Unit testing

The project uses mostly only one framework for assertions - [AssertJ](https://joel-costigliola.github.io/assertj/)
A few examples:
```
assertThat(actualQuery).isEqualTo(matchAllQuery());

assertThat(actualCollection).isNotEmpty().containsExactly("str1", "str2");

assertThatThrownBy(() -> service.doExceptionalOperation())
  .isInstanceOf(IllegalArgumentException.class)
  .hasMessage("invalid parameter");
```

### Integration testing

The module uses [Testcontainers](https://www.testcontainers.org/) to run Elasticsearch, Apache Kafka and PostgreSQL
in embedded mode. It is required to have Docker installed and available on the host where the tests are executed.
