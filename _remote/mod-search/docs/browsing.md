---
layout: null
---

## Overview

Browse is a virtual-shelf navigation feature that lets clients page through an ordered index (subjects, call numbers,
contributors, classifications, authorities) using an **anchor value** and a **limit**. Instead of offset-based
pagination, it uses OpenSearch's `search_after` cursor mechanism, which makes deep navigation efficient at any position
in the index.

---

## API Endpoints

| Browse type          | HTTP endpoint                                              | Target field              |
|:---------------------|:-----------------------------------------------------------|:--------------------------|
| Subject              | `GET /browse/instances/by-subject`                        | `value`                   |
| Call number          | `GET /browse/instances/by-call-number/{browseOptionId}`   | `callNumber`              |
| Classification       | `GET /browse/instances/by-classification/{browseOptionId}`| `classificationNumber`    |
| Contributor          | `GET /browse/instances/by-contributor`                    | `contributor`             |
| Authority            | `GET /browse/authorities`                                  | `headingRef`              |

### Common query parameters

| Parameter              | Type    | Default      | Description                                                                                     |
|:-----------------------|:--------|:-------------|:------------------------------------------------------------------------------------------------|
| `query`                | string  | **required** | CQL range expression (see Query Syntax below)                                                   |
| `limit`                | integer | **required** | Total number of items to return in the page                                                     |
| `precedingRecordsCount`| integer | `limit / 2`  | How many of the `limit` slots go to items **before** the anchor (only meaningful for `around`)  |
| `highlightMatch`       | boolean | `true`       | When `true` and the anchor is not in the index, a placeholder item with `isAnchor=true` is injected |

**Constraint:** `precedingRecordsCount` must be strictly less than `limit`.

---

## Query Syntax

Browsing can be performed in two directions – forward and backward. Browsing around combines results from these two
queries.

| Direction          | Query                               | Description                                                                                                              |
|:-------------------|:------------------------------------|:-------------------------------------------------------------------------------------------------------------------------|
| forward            | `callNumber > F`                    | Returns all records **after** the anchor, ascending                                                                      |
| forward_including  | `callNumber >= F`                   | Returns all records **from** the anchor (inclusive), ascending                                                           |
| backward           | `callNumber < F`                    | Returns all records **before** the anchor, descending, then reversed                                                     |
| backward_including | `callNumber <= F`                   | Returns all records **up to** the anchor (inclusive), descending, then reversed                                          |
| around             | `callNumber > F or callNumber < F`  | Returns records both before and after the anchor; the anchor itself is **excluded** (placeholder injected if `highlightMatch`) |
| around_including   | `callNumber >= F or callNumber < F` | Returns records around the anchor; the anchor is **included** (real item if found, placeholder if not)                  |

_where `callNumber` is the name of the field being browsed and `F` is the anchor value._

### Adding filters

Filters can be appended to any browse query using the `and` keyword. The browse range expression must be wrapped in
parentheses when combined with additional conditions:

```
(value >= "music" or value < "music") and authorityId=="308c950f-8209-4f2e-9702-0c004a9f21bc"
```

Only fields declared with `"searchTypes": ["filter"]` in the index model support filtering.

---

## Response Structure

Every browse endpoint returns a result object with the same shape:

```json
{
  "totalRecords": 50,
  "prev": "Library science",
  "next": "Neuroscience",
  "items": [
    { "value": "Library science", "totalRecords": 6 },
    { "value": "Machine learning", "totalRecords": 7, "isAnchor": true },
    { "value": "Media studies",    "totalRecords": 3 }
  ]
}
```

| Field          | Description                                                                                                    |
|:---------------|:---------------------------------------------------------------------------------------------------------------|
| `totalRecords` | Total number of distinct values matching the applied filter conditions (not in this page). When no filters are applied this equals the full index size. When heading-type or other filters are present it reflects the filtered count. |
| `prev`         | Value of the **first** item in `items`; pass as anchor with a `<` query to navigate to the previous page.     |
| `next`         | Value of the **last** item in `items`; pass as anchor with a `>` query to navigate to the next page. `null` if the last item is the global last. |
| `items`        | Ordered list of browse items for this page.                                                                    |
| `isAnchor`     | Present and `true` only on the item that matches the requested anchor value.                                   |

---

## Algorithm Details

### Context construction (`BrowseContextProvider`)

Before any OpenSearch query is issued, the CQL query string is parsed into a `BrowseContext` object that contains:

- **`anchor`** – the value extracted from the range condition (identical in both clauses for `around` queries; validated to match).
- **`precedingQuery`** – the `<` / `<=` range query builder (present only when browsing backward or around).
- **`succeedingQuery`** – the `>` / `>=` range query builder (present only when browsing forward or around).
- **`precedingLimit`** / **`succeedingLimit`** – how many slots each side of the page gets.
- **`filters`** – extra `filter` clauses extracted from any `and …` conditions in the query.

For **one-direction** queries only one of `precedingQuery`/`succeedingQuery` is populated.
For **around** queries both are populated and the sum of their limits equals `limit`.

### Limit allocation for `around` queries

```
precedingLimit  = precedingRecordsCount           (default: floor(limit / 2))
succeedingLimit = limit - precedingRecordsCount - 1   (anchor occupies one slot)
```

When `highlightMatch=false` no anchor slot is consumed, so the formula changes to:

```
succeedingLimit = limit - precedingRecordsCount   (highlightMatch=false)
```

The anchor itself is **not counted** toward either limit – it is handled as a third, separate query.

### OpenSearch execution

All browse variants use OpenSearch's `search_after` cursor (not `from`/`size`) for efficient deep navigation.

#### One-direction browse

| Anchor included? | Queries issued | How anchor is handled |
|:-----------------|:---------------|:----------------------|
| No (`>` or `<`)  | 1 main search  | Not fetched; cursor starts strictly after/before anchor value |
| Yes (`>=` or `<=`)| 2 (main + anchor) | Anchor fetched separately, prepended/appended to the page |

The anchor search uses an exact `term` query on the target field.

#### Around browse

Three OpenSearch queries are issued via a single `msearch` call:

1. **Anchor query** – `term(targetField, anchor)` – determines the exact sort values to seed the cursors.
2. **Preceding query** – `search_after` cursor descending from the anchor, fetching `precedingLimit + 1` items.
3. **Succeeding query** – `search_after` cursor ascending from the anchor, fetching `succeedingLimit + 1` items.

The `+1` overfetch on each side is used to detect whether a `prev`/`next` pointer exists beyond the current page without
issuing an extra request.

The anchor query's sort values are used to seed the `search_after` parameter of both the preceding and succeeding
queries, so they start exactly at the anchor boundary.

#### Final page assembly

```
precedingRecords  = reverse(trim(preceding results, precedingLimit))
succeedingRecords = [anchor item] + trim(succeeding results, succeedingLimit)
page              = precedingRecords + succeedingRecords
prev              = first item of precedingRecords  (null if none)
next              = last item of succeedingRecords   (null if ≤ succeedingLimit results returned)
```

When `highlightMatch=true` and the anchor value is not found in the index, a **placeholder** item is injected:

```json
{ "value": "genetics", "totalRecords": 0, "isAnchor": true }
```

When `highlightMatch=false`, no placeholder is injected and the anchor term does not appear if it has no matching
records.

---

## Subject Browse

Subject browse operates on the **`INSTANCE_SUBJECT`** resource, which is a denormalized sub-index derived from
instances. Each document represents one distinct `(value, authorityId, sourceId, typeId)` combination and stores a
nested list of instance back-references with per-tenant counts.

### Sort order

Results within a page are sorted by:

1. `value` – ICU collation ascending (case-insensitive, language-aware)
2. `authorityId` – ascending, missing values sort **last**
3. `sourceId` – ascending, missing values sort last
4. `typeId` – ascending (max mode), missing values sort last

This means that when two subjects share the same `value` (e.g. two "Music" entries with different authority IDs) they
both appear as separate items within the same page, ordered by their `authorityId`.

### `totalRecords` per item

The count shown on a subject browse item is the **sum of instance counts** across all `instances` sub-resources
that belong to the requesting tenant (or, in consortium mode, the active affiliation).

### Filterable / facetable fields

The following fields on the subject index support filter and facet queries:

| Field         | Example filter query                                      |
|:--------------|:----------------------------------------------------------|
| `sourceId`    | `sourceId=="e62bbefe-adf5-4b1e-b3e7-43d877b0c91b"`       |
| `typeId`      | `typeId=="e62bbefe-adf5-4b1e-b3e7-43d877b0c91c"`         |
| `instances.tenantId` | `instances.tenantId=="tenant_a"`                  |
| `instances.shared`   | `instances.shared==true`                          |

---

## Authority Browse

Authority browse operates on the **`AUTHORITY`** resource. Each document in the browse index represents one
**heading entry** derived from an authority record. A single authority record typically produces multiple browse
entries: one authorized heading, zero or more reference headings (from `sft*` fields), and optionally a title
heading (from `*Title` fields).

### Index document structure

| Field              | Type          | Description                                                                                                  |
|:-------------------|:--------------|:-------------------------------------------------------------------------------------------------------------|
| `headingRef`       | `keyword_icu` | The heading text — the field being browsed and sorted                                                        |
| `headingType`      | `keyword`     | Heading category: `Personal Name`, `Corporate Name`, `Conference Name`, `Geographic Name`, `Uniform Title`, `Topical`, `Genre`, `Named Event`, `Chronological Term`, `Chronological Subdivision`, `Geographic Subdivision`, `General Subdivision`, `Form Subdivision`, `Medium of Performance Term` |
| `authRefType`      | `keyword`     | `Authorized` for the preferred heading; `Reference` for see-also entries                                     |
| `isTitleHeadingRef`| `boolean`     | `true` when the heading was sourced from a `*Title` field (e.g. `personalNameTitle`, `meetingNameTitle`). Use `isTitleHeadingRef==false` to exclude these from a name-only browse. |
| `naturalId`        | `keyword`     | External / LC control number of the authority record                                                         |
| `sourceFileId`     | `keyword`     | UUID of the authority source file the record belongs to                                                      |
| `id`               | `keyword`     | UUID of the authority record                                                                                 |
| `tenantId`         | `keyword`     | Owning tenant identifier                                                                                     |
| `shared`           | `boolean`     | Whether the authority record is shared across the consortium                                                 |
| `numberOfTitles`   | `integer`     | Count of title instances linked to this authority (present only on `Authorized` entries)                     |

### Sort order

Results are sorted by `headingRef` using **ICU collation** (case-insensitive, diacritic-aware, language-aware).
Characters with diacritics (e.g. `Ĵ`, `ä`) sort near their base-letter equivalents rather than at the end of the
alphabet.

### `totalRecords`

Reflects the **total number of browse entries matching the non-range filter conditions** (e.g. `headingType`,
`isTitleHeadingRef`, `sourceFileId`). When filters are applied this count may be significantly smaller than the
full authority index.

### Response item structure

Each authority browse item contains:

```json
{
  "headingRef": "Brian K. Vaughan",
  "isAnchor": true,
  "authority": {
    "id": "0000002b-0000-4000-a000-000000000000",
    "naturalId": "nb1994732053",
    "headingRef": "Brian K. Vaughan",
    "headingType": "Personal Name",
    "authRefType": "Authorized",
    "isTitleHeadingRef": false,
    "sourceFileId": "b4000001-5de4-4467-b77f-b2057d6d69b6",
    "tenantId": "test_tenant",
    "shared": false,
    "numberOfTitles": 0
  }
}
```

| Field         | Description                                                                                       |
|:--------------|:--------------------------------------------------------------------------------------------------|
| `headingRef`  | Heading text for this browse entry                                                                |
| `isAnchor`    | `true` on the anchor item (see `isAnchor` behaviour below)                                        |
| `authority`   | Nested authority object; **absent on placeholder items** (anchor values not found in the index)  |

### `isAnchor` flag behaviour

`isAnchor` is set to `true` on:
- The **real anchor** item in `aroundIncluding` queries when the anchor value exists in the index.
- A **placeholder item** (no `authority` object) injected when `highlightMatch=true` and the anchor value is not
  present in the index — this applies to both `around` and `aroundIncluding` query types.

`isAnchor` is **not set** on items returned by forward-only or backward-only queries, even when the anchor value
appears in the result.

### Filterable fields

Additional filter conditions can be appended to any browse query with `and`:

| Field              | Example filter query                                                       |
|:-------------------|:---------------------------------------------------------------------------|
| `headingType`      | `headingType==("Personal Name")` or `headingType==("Personal Name" OR "Corporate Name")` |
| `isTitleHeadingRef`| `isTitleHeadingRef==false`                                                 |
| `sourceFileId`     | `sourceFileId=="b4000001-5de4-4467-b77f-b2057d6d69b6"`                     |
| `tenantId`         | `tenantId=="test_tenant"`                                                  |
| `shared`           | `shared==false`                                                            |

### Example — browsing around with heading-type filter

```
GET /browse/authorities
  ?query=( headingRef >= "Ĵämes Röllins" or headingRef < "Ĵämes Röllins" )
         and isTitleHeadingRef==false
         and headingType==("Personal Name")
         and sourceFileId=="b4000001-5de4-4467-b77f-b2057d6d69b6"
  &limit=7
  &precedingRecordsCount=2
```

Only Personal Name entries with `isTitleHeadingRef==false` are considered. The `totalRecords` value in the
response reflects the total count of Personal Name non-title entries matching the source file filter, not the
full authority index size.

---

## Contributor Browse

Contributor browse operates on the **`INSTANCE_CONTRIBUTOR`** resource – a denormalized sub-index where each document
represents one distinct `(name, contributorNameTypeId, authorityId)` combination. A single contributor name can yield
**multiple browse items** when it appears with different name types or authority links (e.g. "John Lennon" linked to an
authority record and "John Lennon" without one are two separate items).

### Index document structure

Each contributor document contains:

| Field                   | Type              | Description                                                                 |
|:------------------------|:------------------|:----------------------------------------------------------------------------|
| `name`                  | `keyword_icu`     | Contributor name as stored on the instance (personal, corporate, or meeting) |
| `contributorNameTypeId` | `keyword`         | Links the contributor to a MARC-defined name type (e.g. personal, corporate) |
| `authorityId`           | `keyword`         | ID of the authority record that controls this heading (may be absent)        |
| `instances`             | nested object     | One entry per contributing instance/tenant pair                              |
| `instances.typeId`      | `keyword` (array) | Contributor role/type IDs attached to this contributor on that instance      |
| `instances.tenantId`    | `keyword`         | Owning tenant (for consortium filtering)                                     |
| `instances.shared`      | `bool`            | Whether the instance is shared across the consortium                         |
| `instances.count`       | integer           | Number of instances from that tenant that share this `(name, nameTypeId, authorityId)` |

### Sort order

Results within a page are sorted by:

1. `name` – ICU collation ascending (case-insensitive, language-aware). Digits sort before letters.
2. `contributorNameTypeId` – ascending, missing values sort **last**.
3. `authorityId` – ascending, missing values sort **last**.

This means that a name such as "Bon Jovi" appears as **multiple consecutive browse items** when it has more than one
`(nameTypeId, authorityId)` combination, ordered by those secondary/tertiary keys.

### `totalRecords` per item

The `totalRecords` on each browse item is the **sum of `instances.count`** across all sub-resources that belong to the
requesting tenant. In consortium mode only sub-resources for the active affiliation are counted.

### Response item fields

In addition to the common `isAnchor` / `totalRecords` fields every contributor browse item carries:

| Field                   | Description                                                                          |
|:------------------------|:-------------------------------------------------------------------------------------|
| `name`                  | Contributor name                                                                     |
| `contributorNameTypeId` | The name type UUID of this browse entry                                              |
| `authorityId`           | Authority record UUID (absent when the contributor has no authority link)            |
| `contributorTypeId`     | Deduplicated, sorted list of contributor type/role IDs gathered from all instances that share this entry |

### Filterable / facetable fields

| Field                   | Example filter / facet query                                             |
|:------------------------|:-------------------------------------------------------------------------|
| `contributorNameTypeId` | `contributorNameTypeId=="e2ef4075-310a-4447-a231-712bf10cc985"`          |
| `instances.tenantId`    | `instances.tenantId=="tenant_a"`                                         |
| `instances.shared`      | `instances.shared==true`                                                 |

Filtering by `contributorNameTypeId` is the most common use case – it restricts the browse index to only entries with a
specific name type (e.g. show only personal names).

### Example – browsing around a name with a name-type filter

```
GET /browse/instances/by-contributor
  ?query=( name >= "John Lennon" or name < "John Lennon" )
         and contributorNameTypeId=="e2ef4075-310a-4447-a231-712bf10cc985"
  &limit=5
```

Only contributor documents whose `contributorNameTypeId` equals the given UUID are considered. "John Lennon" does not
exist with that name type, so a placeholder is injected and `totalRecords` reflects the count within the filtered index.

---

## Classification Browse

Classification browse operates on the **`INSTANCE_CLASSIFICATION`** resource — a denormalized sub-index where each
document represents one distinct `(classificationNumber, classificationTypeId)` combination.

### Browse options and configuration

Unlike subject or contributor browse, the classification endpoint requires a **`browseOptionType`** path segment (e.g.
`LC`, `DEWEY`, `ALL`) that selects a pre-configured browse profile stored in the database. Each profile defines:

| Field               | Description                                                                                                         |
|:--------------------|:--------------------------------------------------------------------------------------------------------------------|
| `shelvingAlgorithm` | Algorithm used to normalize the anchor before passing it to `search_after` (e.g. `LC`, `DEWEY`, `DEFAULT`)         |
| `typeIds`           | List of classification type UUIDs to include. An **empty list means include all types** (`ALL` semantics).         |

Multiple type UUIDs can be assigned to a single browse option (e.g. `LC` option covering two different LC-family types).
The filter is expressed as a `bool.should` (OR) over the configured type IDs.

The active configuration can be updated via:
```
PUT /browse/config/instance-classification/{browseOptionType}
```

### Sort order

The browse index is sorted by a **pre-computed shelving-order field** — not by the raw classification number string.
The shelving order is computed once at index time using `ShelvingOrderCalculationHelper` with the configured algorithm
(e.g. LC shelf key). The `search_after` cursor at query time is seeded with:

```
[normalizedAnchor.toLowerCase(), rawAnchor.toLowerCase()]
```

This means two classification numbers that look alphabetically similar may be far apart in browse order (e.g.
`QA76.73.C15` sorts before `QA100` which sorts before `QA1771` in LC shelving order, even though `76 < 100 < 1771` is
not obvious from lexicographic comparison). Numeric sub-classes receive zero-padded shelf keys that preserve numeric
ordering.

Within the same browse option the secondary sort by raw classification number provides stable ordering when two entries
have identical normalized keys.

### `totalRecords` per item and instance context

The `totalRecords` on a classification browse item is the **sum of instance counts** across all sub-resources visible to
the requesting tenant (or active consortium affiliation).

Instance title and contributors are populated **only when `totalRecords == 1`**:

| `totalRecords` | `instanceTitle`     | `instanceContributors`  |
|:---------------|:--------------------|:------------------------|
| 1              | set from the single matching instance | set from the single matching instance |
| > 1            | `null`              | `null` (ambiguous — multiple instances share this number) |
| 0 (placeholder)| `null`              | `null` |

### Response item fields

| Field                   | Description                                                                                     |
|:------------------------|:------------------------------------------------------------------------------------------------|
| `id`                    | Stable hash of the classification number                                                        |
| `classificationNumber`  | Raw classification number as stored on the instance                                             |
| `classificationTypeId`  | UUID of the classification type (e.g. LC, Dewey)                                               |
| `totalRecords`          | Number of instances that carry this classification number (tenant-scoped)                       |
| `instanceTitle`         | Title of the matching instance — present only when `totalRecords == 1`                          |
| `instanceContributors`  | Contributor names from the matching instance — present only when `totalRecords == 1`            |
| `isAnchor`              | `true` only on the item matching the requested anchor in `aroundIncluding` queries              |

### `isAnchor` flag behaviour

`isAnchor` is set to `true` exclusively when an **`aroundIncluding`** query is used
(`number < {value} or number >= {value}`). It is **never** set for forward-only or backward-only queries
(including `forwardIncluding` / `backwardIncluding`), even though the anchor item appears in those results.

When `highlightMatch=true` (the default) and the anchor value is not present in the index, the service injects a
placeholder:

```json
{ "classificationNumber": "QA100 .X00 2000", "totalRecords": 0, "isAnchor": true }
```

`instanceTitle` and `instanceContributors` are `null` (not `[]`) on placeholder items.

### Example — browsing around an anchor with LC option

```
GET /browse/instances/by-classification/lc
  ?query=number < "QA76.73.C15" or number >= "QA76.73.C15"
  &limit=5
  &precedingRecordsCount=2
```

The LC option normalizes `QA76.73.C15` to its LC shelf key, seeds the `search_after` cursor, and returns the two
preceding entries plus up to three succeeding entries, with the matched item tagged `isAnchor=true`.

### Filterable fields

Additional filter conditions can be appended with `and`:

| Field                  | Example                                                     |
|:-----------------------|:------------------------------------------------------------|
| `classificationTypeId` | `classificationTypeId=="42471af9-7d25-4f3a-bf78-60d29dcf463b"` |
| `instances.tenantId`   | `instances.tenantId=="tenant_a"`                            |
| `instances.shared`     | `instances.shared==true`                                    |

---

## Call Number Browse

Call number browse operates on the **`INSTANCE_CALL_NUMBER`** resource. Each document in this sub-index represents
one distinct call number (across all its copies / holdings), identified by the combination of
`callNumber`, `callNumberPrefix`, `callNumberSuffix`, and `callNumberTypeId`.

### Browse option types

The browse endpoint path includes a `{browseOptionId}` segment that selects which shelving-order algorithm is used
to normalize call numbers for ordering:

| `browseOptionId` | Algorithm                    | Source data                          |
|:-----------------|:-----------------------------|:-------------------------------------|
| `all`            | Best-match across all types  | All call number types combined       |
| `lc`             | LC shelving order            | Restricted to configured LC type IDs |
| `dewey`          | Dewey decimal shelving order | Dewey type IDs                       |
| `nlm`            | NLM (National Library of Medicine) | NLM type IDs                   |
| `sudoc`          | SuDoc government document    | SuDoc type IDs                       |

Each option type can be configured with a list of allowed call number type UUIDs. When a non-empty list is
configured, **only records whose `callNumberTypeId` is in the list produce an exact-match anchor**; other types
remain visible in surrounding pages but the anchor placeholder is shown instead. When the configuration list is
empty, all types produce an exact match (useful for testing or permissive setups).

### Source field

Call numbers are sourced exclusively from **`items.effectiveCallNumberComponents`** — the resolved call number
fields on each item, which combine the item's own values with its holding's values according to FOLIO's priority
rules. Holdings-level or instance-level call numbers are not used directly.

The components that form a call number document are:
- `callNumber` — the base shelf number
- `callNumberPrefix` — optional prefix (e.g. `"REF"`, `"Oversize"`)
- `callNumberSuffix` — optional suffix (e.g. `"c.1"`, `"FT MEADE"`)
- `callNumberTypeId` — UUID of the call number type

The **full call number** that is displayed and used as the browse anchor is computed as:

```
fullCallNumber = callNumber + " " + suffix   (when suffix is non-null)
fullCallNumber = callNumber                  (when suffix is null)
```

The prefix is stored and returned but is **not** part of the sort key or the `fullCallNumber` used for anchoring.

### Sort order

Results are sorted by:

1. `callNumber.keyword` — the normalized shelving-order key (produced by the configured shelving algorithm)
2. `callNumberSuffix.keyword` — ascending; missing values sort last
3. `callNumberPrefix.keyword` — ascending; missing values sort last
4. `callNumberTypeId.keyword` — ascending (tie-break for identical components with different types)

The shelving-order normalization converts the raw call number into a zero-padded, case-folded key so that numeric
sub-classes sort numerically rather than lexicographically (e.g. `QA9` sorts before `QA10`, not after).

### `totalRecords` per item and instance context

The `totalRecords` on a call number browse item is the **number of item records** (across all holdings) that share
the same effective call number components, scoped to the requesting tenant.

Instance title is populated **only when `totalRecords == 1`**:

| `totalRecords` | `instanceTitle`                                |
|:---------------|:-----------------------------------------------|
| 1              | Set from the single matching instance          |
| > 1            | `null` (multiple instances share this number)  |
| 0 (placeholder)| `null`                                         |

### Response item fields

| Field                | Description                                                                                        |
|:---------------------|:---------------------------------------------------------------------------------------------------|
| `id`                 | Stable hash of the call number components                                                          |
| `fullCallNumber`     | Display form: `callNumber [ + " " + suffix]`                                                       |
| `callNumber`         | Base shelf number as stored on the item                                                            |
| `callNumberPrefix`   | Optional prefix (e.g. `"REF"`, `"Oversize"`)                                                       |
| `callNumberSuffix`   | Optional suffix (e.g. `"c.1"`, `"FT MEADE"`)                                                      |
| `callNumberTypeId`   | UUID of the call number type                                                                       |
| `totalRecords`       | Number of item records sharing this call number (tenant-scoped)                                    |
| `instanceTitle`      | Title of the matching instance — present only when `totalRecords == 1`                             |
| `isAnchor`           | `true` only on the item matching the requested anchor in `aroundIncluding` queries                 |

### `isAnchor` flag behaviour

`isAnchor` is set to `true` exclusively when an **`aroundIncluding`** query is used
(`fullCallNumber >= {value} or fullCallNumber < {value}`). It is **never** set for forward-only or backward-only
queries, even if the anchor item appears in the results.

When `highlightMatch=true` (the default) and the anchor value is not present in the index, a placeholder is
injected:

```json
{ "fullCallNumber": "QA100 .X00 2000", "totalRecords": 0, "isAnchor": true }
```

### Exact-match filtering by option type

When browsing with the `lc` option, the service first checks whether the item under the anchor has a
`callNumberTypeId` that belongs to the configured LC type list. If not, the anchor resolves to a placeholder even
if the raw call number string is present in the index (e.g. a Dewey number that happens to match the query string).
Other option types (`dewey`, `nlm`, `sudoc`) follow the same rule.

The `all` option does not filter by type and always produces an exact match when the call number exists.

### Example — browsing around an anchor with LC option

```
GET /browse/instances/by-call-number/lc
  ?query=fullCallNumber >= "RC280.N4 N49" or fullCallNumber < "RC280.N4 N49"
  &limit=5
  &precedingRecordsCount=2
```

Response (only LC-type call numbers visible, 20 total in the LC sub-index):

```json
{
  "totalRecords": 20,
  "prev": "QP363 .N6 1965 FT MEADE",
  "next": "RJ421 .D3",
  "items": [
    { "fullCallNumber": "QP363 .N6 1965 FT MEADE", "callNumberSuffix": "FT MEADE", "totalRecords": 2 },
    { "fullCallNumber": "QR1.I6", "totalRecords": 1, "instanceTitle": "Sociology of Education and Schooling" },
    { "fullCallNumber": "RC280.N4 N49", "totalRecords": 1, "instanceTitle": "Game Theory and Strategic Behavior", "isAnchor": true },
    { "fullCallNumber": "RC667 .N47 2010", "totalRecords": 1, "instanceTitle": "Migration, Identity, and Belonging" },
    { "fullCallNumber": "RJ421 .D3", "totalRecords": 1, "instanceTitle": "The Ethics of Artificial Intelligence" }
  ]
}
```

### Filterable fields

Additional filter conditions can be appended with `and`:

| Field                  | Example                                                     |
|:-----------------------|:------------------------------------------------------------|
| `callNumberTypeId`     | `callNumberTypeId=="cbc422b0-1d17-4d43-9cc0-6c89b2efd014"` |
| `items.effectiveLocationId` | `items.effectiveLocationId=="65b6c2e9-8a7b-4a10-9b5d-ba1cf0313cd7"` |
| `instances.tenantId`   | `instances.tenantId=="tenant_a"`                            |
| `instances.shared`     | `instances.shared==true`                                    |

### Special characters in call numbers

Call numbers that contain backslashes must be double-escaped in the CQL query. For example, the call number
`BR\140 .J\\86` must be written in the query string as:

```
fullCallNumber >= "BR\\\\140 .J\\\\\\\\86" or fullCallNumber < "BR\\\\140 .J\\\\\\\\86"
```

And in a Java test string literal:

```java
"BR\\\\\\\\140 .J\\\\\\\\\\\\\\\86"
```

---

## Consortium / Multi-tenant Support

In ECS (consortium) mode, browse queries are automatically filtered to the **active affiliation** tenant by
`ConsortiumSearchHelper`. The `totalRecords` field on each browse item counts only items visible to that affiliation.
The top-level `totalRecords` in the response reflects the full index size across all tenants.

---

## Service Class Hierarchy

```
AbstractBrowseService<T>
│   browse(request)                 – entry point; dispatches to direction or around
│   browseInOneDirection(...)       – abstract
│   browseAround(...)               – abstract
│
└── AbstractBrowseServiceBySearchAfter<T, R>
    │   browseInOneDirection(...)   – uses search_after; handles anchor-include logic
    │   browseAround(...)           – issues msearch (2 or 3 queries); assembles page
    │   getSearchQuery(...)         – abstract (per-resource sort fields)
    │   getAnchorSearchQuery(...)   – abstract (term query on targetField)
    │   getEmptyBrowseItem(...)     – abstract (placeholder for missing anchor)
    │   mapToBrowseResult(...)      – abstract (maps raw ES doc to DTO)
    │
    ├── SubjectBrowseService          (resource: INSTANCE_SUBJECT)
    ├── ContributorBrowseService      (resource: INSTANCE_CONTRIBUTOR)
    ├── AuthorityBrowseService        (resource: AUTHORITY)
    │
    └── AbstractShelvingOrderBrowseServiceBySearchAfter<T, R>
        │   getSearchQuery(...)       – normalizes anchor via ShelvingOrderCalculationHelper
        │
        ├── CallNumberBrowseService       (resource: INSTANCE_CALL_NUMBER)
        └── ClassificationBrowseService   (resource: INSTANCE_CLASSIFICATION)
```

---

## CQL Escaping for Special Characters

Anchor values containing CQL-special characters (backslash, double-quote) must be double-escaped when placed inside a
CQL string literal. For example, the subject value:

```
backslash\ "double\-quotes\" te\st
```

must be written in a CQL query as:

```
value >= "backslash\\ \"double\\-quotes\\\" te\\st"
```

And in a Java string literal (as used in tests):

```java
"backslash\\\\ \\\"double\\\\-quotes\\\\\\\" te\\\\st"
```
