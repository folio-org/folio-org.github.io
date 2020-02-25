---
layout: page
title: Working with dates and times
permalink: /guides/dates-and-times/
menuInclude: no
menuTopTitle: Guides
---

This document describes the general principles regarding how FOLIO operates with international date and time values.

FOLIO uses [RFC 3339](https://www.ietf.org/rfc/rfc3339.txt) as the standard to represent date and time format (i.e. a profile of ISO 8601).

To support tenants that have locations and users in different time zones, FOLIO plans to support [user-level time zone setting](https://issues.folio.org/browse/UXPROD-510).

## Back-end APIs

Dates and times are stored with the back-end modules as UTC.
The APIs assume UTC on input, and store and return timestamps in UTC.

## Front-end

The [Stripes i18n document](https://github.com/folio-org/stripes/blob/master/doc/i18n.md#dates-and-times) explains how they are formatted for display by front-end modules.
When comparing or manipulating dates, it is safest to operate in UTC mode and leave display formatting to internationalization helpers.

## \*.raml and schema.json

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
  "endDate": "2019-01-01T11:12:00.6+00:00",
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

Note: The RAML types "datetime" and "date-only" are used with RAML 1.0 only.

## Tenant time zone configuration

To respect the tenant chosen timezone on the back-end, use direct call to mod-configuration.
FOLIO uses the [tz database](https://en.wikipedia.org/wiki/Tz_database) to specify timezone for a tenant.
Default value is "UTC".
Example: America/New\_York

## SQL

Getting a datetime field as a timestamp without timezone returns it in UTC (time zone +00) irrespective of the SQL client session time zone setting:

```
SET TIME ZONE '-08';
SELECT creation_date::timestamp,
       (jsonb->'metadata'->>'createdDate')::timestamp,
       (jsonb->'metadata'->>'updatedDate')::timestamp
FROM diku_mod_inventory_storage.instance;
      creation_date      |        timestamp        |        timestamp
-------------------------+-------------------------+-------------------------
 2019-02-23 08:30:57.349 | 2019-02-23 08:30:57.349 | 2019-02-23 08:30:57.349

SET TIME ZONE '+01';
SELECT creation_date::timestamp,
       (jsonb->'metadata'->>'createdDate')::timestamp,
       (jsonb->'metadata'->>'updatedDate')::timestamp
FROM diku_mod_inventory_storage.instance;
      creation_date      |        timestamp        |        timestamp
-------------------------+-------------------------+-------------------------
 2019-02-23 08:30:57.349 | 2019-02-23 08:30:57.349 | 2019-02-23 08:30:57.349
```

Use the UTC +00 time zone offset to convert the timestamp without timezone into a timestamp with timezone. The result will be in the time zone of the SQL client session:
```
SET TIME ZONE '-08';
SELECT creation_date::timestamp AT TIME ZONE '+00',
       (jsonb->'metadata'->>'createdDate')::timestamp AT TIME ZONE '+00',
       (jsonb->'metadata'->>'updatedDate')::timestamp AT TIME ZONE '+00'
FROM diku_mod_inventory_storage.instance;
          timezone          |          timezone          |          timezone
----------------------------+----------------------------+----------------------------
 2019-02-23 00:30:57.349-08 | 2019-02-23 00:30:57.349-08 | 2019-02-23 00:30:57.349-08

SET TIME ZONE '+01';
SELECT creation_date::timestamp AT TIME ZONE '+00',
       (jsonb->'metadata'->>'createdDate')::timestamp AT TIME ZONE '+00',
       (jsonb->'metadata'->>'updatedDate')::timestamp AT TIME ZONE '+00'
FROM diku_mod_inventory_storage.instance;
          timezone          |          timezone          |          timezone
----------------------------+----------------------------+----------------------------
 2019-02-23 09:30:57.349+01 | 2019-02-23 09:30:57.349+01 | 2019-02-23 09:30:57.349+01
```

PostgreSQL documentation: [Time Zones](https://www.postgresql.org/docs/current/datatype-datetime.html#DATATYPE-TIMEZONES), [AT TIME ZONE](https://www.postgresql.org/docs/current/functions-datetime.html#FUNCTIONS-DATETIME-ZONECONVERT)

