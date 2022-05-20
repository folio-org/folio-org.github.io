---
layout: null
---

## Overview

### Query Syntax

Browsing can be performed in two directions - forward and backward. Browsing around combines results from these two
queries.

| Direction          | Query                               | Description                                                                                                              |
|:-------------------|:------------------------------------|:-------------------------------------------------------------------------------------------------------------------------|
| forward            | `callNumber > F`                    | Request with that query will return all records after the specified anchor in ascending alphabetical order               |
| forward_including  | `callNumber >= F`                   | Request with that query will return all records after the specified anchor in ascending alphabetical order including it  |
| backward           | `callNumber < F`                    | Request with that query will return all records before the specified anchor in ascending alphabetical order              |
| backward_including | `callNumber <= F`                   | Request with that query will return all records before the specified anchor in ascending alphabetical order including it |
| around             | `callNumber < F or callNumber > F`  | Request with that query will return all records around the anchor                                                        |
| around_including   | `callNumber < F or callNumber >= F` | Request with that query will return all records around the anchor including it                                           |

_where the `callNumber` is the name of field for browsing, `F` is the anchor value_

### Call-Number Browsing

[Call Number Browse API](https://s3.amazonaws.com/foliodocs/api/mod-search/s/mod-search.html#operation/browseInstancesByCallNumber)

#### Approach

_Numeric representation of `items.effectiveShelvingOrder` is used to narrow down the number of results in response. It
increases the response time significantly because by default there is no other way to sort instances in the index by
effective shelving key. This can be explained by the structure of the instance record. For Elasticsearch it contains all
fields from the instance and corresponding items\holding as inner arrays. This results in fields
like `items.effectiveShelvingOrder` to store multiple values. For correct browsing one of the values must be chosen
every time depending on the user input. Script-based sorting solves this problem because the right value from the array
can be chosen by the binary search algorithm from the core `Collections` class. Sorting of items before indexing
operation reduces the overall complexity of script sorting._

The implemented solution contains two parts:

1) instance resource index preparation contains such steps as:

- Sorting inner items by `effectiveShelvingOrder`. It's allows to have a prepared sorted list of shelf keys for browsing
- Calculating the long representation of the shelf key per each item using the
  following [algorithm](#string-to-number-algorithm-description)

2) Search query and result processing consist of the following steps:

- Creating the [exists query](https://www.elastic.co/guide/en/elasticsearch/reference/7.13/query-dsl-exists-query.html)
  that is used to browse only on instances that contain `effectiveShelvingOrder` field values
- Creating a painless script
  for [Script Based sorting](https://www.elastic.co/guide/en/elasticsearch/reference/7.13/sort-search-results.html#script-based-sorting)
  depending on the direction for browsing (for `around` and `around-including` two queries are sent in the one `msearch`
  request)
- Multiplying the incoming `size` by the value from the configuration. It's required to perform proper records
  collapsing
- Processing received search hits from Elasticsearch by the `mod-search` service:
  - All records before are populated by the shelf-key value that can be faced between the results (for example, if one
    instance contains two items with call-numbers `A11` and `A12` and the next - `B12`, `B13` only first values
    from `effectiveShelvingOrder` arrays will be found by Elasticsearch script. The `A12` value must be populated in
    search results too because this is a valid call-number value);
  - Adjacent records with the same `effectiveShelvingOrder` are collapsed together according to the acceptance criteria
    of the story
  - If it is the browsing around or around including - the anchor value is highlighted with the boolean flag
    - `isAnchor` (This can be disabled by passing query parameter - `highlightMatch=false`)
  - Extra records exceeding the requested limit are removed (for browsing around and around including limit is
    calculated from the query parameters - `size` and `precedingRecordsCount`)

#### String to number algorithm

This algorithm helps in the runtime to reduce the number of records for Script-Based Sorting for Elasticsearch. It
consists of the following parts:

- Cleaning the input string by removing the invalid characters (see [supported character](#supported-characters)). Only
  52 characters can be supported without overflowing result long value.
- Input string is trimmed to size equal to 10 (it's the maximum amount of characters without overflowing result long
  value)
- For each value the unique long value is generated:
  - only 10 first characters can be used, then the long value will be overflowed
  - all unsupported value are removed from string
  - Each character value is calculated by following formula (`{integer value} * 52 ^ (10 - {character position}`)

#### Supported characters:

| Char value | Num value |
|:----------:|:---------:|
|            |     0     |
|     #      |     1     |
|     $      |     2     |
|     +      |     3     |
|     ,      |     4     |
|     -      |     5     |
|     .      |     6     |
|     /      |     7     |
|     0      |     8     |
|     1      |     9     |
|     2      |    10     |
|     3      |    11     |
|     4      |    12     |
|     5      |    13     |
|     6      |    14     |
|     7      |    15     |
|     8      |    16     |
|     9      |    17     |
|     :      |    18     |
|     ;      |    19     |
|     =      |    20     |
|     ?      |    21     |
|     @      |    22     |
|     A      |    23     |
|     B      |    24     |
|     C      |    25     |
|     D      |    26     |
|     E      |    27     |
|     F      |    28     |
|     G      |    29     |
|     H      |    30     |
|     I      |    31     |
|     J      |    32     |
|     K      |    33     |
|     L      |    34     |
|     M      |    35     |
|     N      |    36     |
|     O      |    37     |
|     P      |    38     |
|     Q      |    39     |
|     R      |    40     |
|     S      |    41     |
|     T      |    42     |
|     U      |    43     |
|     V      |    44     |
|     W      |    45     |
|     X      |    46     |
|     Y      |    47     |
|     Z      |    48     |
|     \      |    49     |
|     _      |    50     |
|     ~      |    51     |

#### Call-Number Browsing Optimization

Range queries can significantly reduce the response time if the lower/upper boundary is specified. The optimized query
for call-number browsing forward will look like:

```callNumber >= F and callNumber <= G```

_This query will work assuming that the number of records between `F` and `G` is more than call-number browsing page_

Elasticsearch [range aggregation](https://www.elastic.co/guide/en/elasticsearch/reference/7.13/search-aggregations-bucket-range-aggregation.html)
allow retrieving the number of resources per specified interval (not that this aggregation includes the `from` value and
excludes the `to` value for each range). As a result, the intervals and corresponding resources are saved into a list of
range values:

| Field     | Type   | Description                                                                   |
|:----------|:-------|:------------------------------------------------------------------------------|
| key       | String | Digits and letters, used as the lower boundary for browsing                   |
| keyAsLong | long   | Numeric representation of the `key`                                           |
| count     | long   | Number of instances that found in the interval between current and next value |

`mod-search` caches this list and found in it the correct lower/upper boundary for call-number browsing depending on the
browsing direction and number of instances to return.

**Example**

_Let's assume that the Elasticsearch index provided to `mod-search` following intervals:_

| Key | Count |
|-----|-------|
| A   | 20    |
| B   | 30    |
| C   | 10    |
| D   | 25    |

- _If a user is browsing by query `callNumber >= B` and `size` equal to 10, then the service will provide an upper
  boundary for that query the `key` - `C` because interval `B` contains more than 10 records._
- _If a user is browsing by query `callNumber > CZ`  and size equal to 100, then the service won't return the upper
  boundary because size exceeds the sum of instances after `CZ`. The Interval `C-D` is ignored because the anchor
  value is larger than the `key`, and only an open interval `D -` can be considered.

An optimization can be disabled by passing environment variable to `mod-search` container:
`CN_BROWSE_OPTIMIZATION_ENABLED = false`
