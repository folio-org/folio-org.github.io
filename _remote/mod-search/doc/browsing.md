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
