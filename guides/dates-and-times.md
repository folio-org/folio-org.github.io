---
layout: page
title: Working with dates and times
permalink: /guides/dates-and-times/
menuInclude: no
menuTopTitle: Guides
---

This document describes the general principles regarding how FOLIO operates with international date and time values.

FOLIO uses [RFC3339](https://www.ietf.org/rfc/rfc3339.txt) as the standard to represent date and time format (i.e. a profile of ISO 8601).
For example: `2019-01-21T22:00:00.000+0000`

Dates and times are stored with the back-end modules as UTC.
The APIs assume UTC on input, and store and return timestamps in UTC.

The i18n document [explains](https://github.com/folio-org/stripes/blob/master/doc/i18n.md#dates-and-times) how they are formatted for display by front-end modules.
When comparing or manipulating dates, it is safest to operate in UTC mode and leave display formatting to internationalization helpers.

With datetime properties in the JSON Schemas, the **type** "string" and **format** "date-time" should be used.
For example:

```
"startDate": {
  "type": "string",
  "format": "date-time",
  "description": "Start date example"
}
```

With datetime query parameters in RAML types, the **type** "datetime" or "date-only" should be used.
For example:

```
startDate:
  displayName: startDate
  type: datetime
  description: "Start date example"

requestedDate:
  displayName: requestedDate
  type: date-only
  description: "Requested date example"
```

In both cases (JSON schema and query parameter) the values deserialize to java.util.Date class.

To respect the tenant chosen timezone on the back-end, use direct call to mod-configuration.
FOLIO uses the [tz database](https://en.wikipedia.org/wiki/Tz_database) to specify timezone for a tenant.
Default value is "UTC".
Example: America/New_York

Note: The RAML types "datetime" and "date-only" are used with RAML 1.0 only.

