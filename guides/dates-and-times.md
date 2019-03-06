---
layout: page
title: Working with dates and times
permalink: /guides/dates-and-times/
menuInclude: no
menuTopTitle: Guides
---

This document describes the general principles regarding how FOLIO operates with international date and time values.

FOLIO uses [RFC 3339](https://www.ietf.org/rfc/rfc3339.txt) as the standard to represent date and time format (i.e. a profile of ISO 8601).

Dates and times are stored with the back-end modules as UTC.
The APIs assume UTC on input, and store and return timestamps in UTC.

The i18n document [explains](https://github.com/folio-org/stripes/blob/master/doc/i18n.md#dates-and-times) how they are formatted for display by front-end modules.
When comparing or manipulating dates, it is safest to operate in UTC mode and leave display formatting to internationalization helpers.

With datetime properties in the JSON Schemas, use the **type** "string" and **format** "date-time".
For example:

```
"startDate": {
  "type": "string",
  "format": "date-time",
  "description": "Start date example"
}
```

and a corresponding JSON sample fragment:
```
  "startDate": "2018-06-01T11:12:00Z",
  "endDate": "2020-01-01T11:12:00.6+00:00",
```

With datetime query parameters in RAML 1.0 types, use the **type** "datetime" or "date-only".
For example:

```
startDate:
  type: datetime
  example: 2018-11-25T22:00:00.0+00:00

endDate:
  type: datetime
  example: 2018-11-26T16:17:18Z

requestedDate:
  type: date-only
  example: 2018-11-20
```

To respect the tenant chosen timezone on the back-end, use direct call to mod-configuration.
FOLIO uses the [tz database](https://en.wikipedia.org/wiki/Tz_database) to specify timezone for a tenant.
Default value is "UTC".
Example: America/New_York

Note: The RAML types "datetime" and "date-only" are used with RAML 1.0 only.

