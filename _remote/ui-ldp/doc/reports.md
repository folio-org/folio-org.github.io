---
layout: null
---

# Authoring reports for the FOLIO Reporting App

<!-- md2toc -l 2 reports.md -->
* [Overview](#overview)
* [Storing and publishing reports](#storing-and-publishing-reports)
* [Writing an SQL report](#writing-an-sql-report)
* [Writing JSON metadata for your report](#writing-json-metadata-for-your-report)
* [Setting up the Reporting app to find your report](#setting-up-the-reporting-app-to-find-your-report)
* [Using your report](#using-your-report)



## Overview

Version 2.0 of the FOLIO Reporting App (formerly known as LDP) introduced a major new feature in reporting. This facility allows users to run SQL reports stored in GitHub or GitLab, filling in parameters to get the specific information they need. (Go to the "Run report" tab of the Reporting app in your FOLIO instance.)

While the reporting facility does not require end-users to write SQL, authoring reports to be used by this facility requires writing an SQL query and packaging it as a SQL function. This document provides an overview of the requirements.


##  Storing and publishing reports

Authoring and editing of templated reports is not done from within the Reporting app. This is done elsewhere using whatever tools the developer finds optimal: the app only consumes them.

Reports compatible with this app consist of two files that share a basename: one is the SQL report itself, named `NAME.sql`; the other is metadata about the report, written in JSON and named `NAME.json`. Optionally a third file, `NAME.md` can be created to hold further documentation about the report.

Reports are published by pushing them to a GitHub or GitLab repository -- specifically, a particular directory within a particular branch of a repository. The source is specified as a git site user, repository name within the user's area, branch name and directory within the repository.

Since the Reporting app can draw reports from multiple sources (see below), it's possible for a FOLIO instance to be configured with (for example) a global source holding reports developed by the FOLIO reporting community, a local source for reports developed within the institition, and perhaps a development source for reports still being worked on. Other configurations are possible.

For example, https://github.com/MikeTaylor/dummy-ldp-queries/tree/main/queries contains some dummy reports created during the software development process. One is represented by the files `users_by_creation_date.sql` and `users_by_creation_date.json`, the other by the files `mikes_query.sql`, `mikes_query.json` and (for documentation only) `mikes_query.md`.


## Writing an SQL report

A SQL report, contained in a file ending in `.sql`, contains a SQL query packaged as a SQL function.  The structure of this file takes the following form:

* The first line is a directive:
  * For LDP: `--ldp:function <NAME>`
  * For Metadb: `--metadb:function <NAME>`
* A blank line.
* A `DROP FUNCTION IF EXISTS <NAME>` SQL statement that drops the function.
* A blank line.
* A `CREATE FUNCTION <NAME>` SQL statement that creates the function.

where `<NAME>` is the name of the report.

For more information about creating SQL reports:
* For LDP: [LDP User Guide > Creating reports](https://github.com/library-data-platform/ldp/blob/main/doc/User_Guide.md#5-creating-reports)
* For Metadb: [Metadb Documentation > Creating reports](https://metadb.dev/doc/#_creating_reports)

In a simple LDP 2.x report to list users created between specified dates, the SQL file might look like this:
```
--ldp:function get_users

DROP FUNCTION IF EXISTS get_users;

CREATE FUNCTION get_users(
    start_date date DEFAULT '2000-01-01',
    end_date date DEFAULT '2050-01-01')
RETURNS TABLE(
    id uuid,
    barcode text,
    created_date timestamptz)
AS $$
SELECT id,
       barcode,
       created_date
    FROM user_users
    WHERE start_date <= created_date AND created_date < end_date
$$
LANGUAGE SQL
STABLE
PARALLEL SAFE;
```

## Writing JSON metadata for your report

The metadata file associated with the SQL report specifies what template parameters exist and how they should be supplied. From this, the Reporting app generates a form for the user to enter values for these parameters. Parameters can be mandatory or optional, free-text or selected from a controlled vocabulary.

This file also contain additional whole-report information, such as a human-readable name and description, and a guide to providing parameter values.

Such a file might look like this (for the SQL report above):
```
{
    "displayName": "List users by date of creation",
    "description": "Created by Kurt to exercise mod-ldp's reporting facility",
    "instructions": "Choose a start and end date for the user-creation period.",
    "parameters": [
        {
            "name": "start_date",
            "displayName": "Earliest date of user creation",
            "type": "date",
            "required": false
        },
        {
            "name": "end_date",
            "displayName": "Latest date of user creation",
            "type": "date",
            "required": false
        }
    ]
}
```

The fields at the top level are:

* `displayName` -- the name by which the report is known in the UI.
* `description` -- an explanation of what the report is for, and optionally details such as who created and maintains it.
* `instructions` -- information of how to fill in the form.
* `parameters` -- an array of parameters for which the user can fill in values.

Each element of the `parameters` array is an object with the following keys:
* `name` -- the machine-reaadable name of of the parameter, which must match one of those declared in the SQL report.
* `displayName` -- the human-readable name of the parameter, which is displayed to the user in the form.
* `required` -- a boolean indicating whether or not the field is mandatory. If omitted, the default is that the field is optional.
* `type` -- one of a small number of short strings indicating the type of the field. Possible values include:
  * `text` -- a string, which by default can be freely entered, but which may be controlled as described below.
  * `date` -- a date, which is chosen using a date-picker.
* `default` -- if provided, a string or number that is placed into the generated form as a default value for the parameter.
* `controlled.options` -- if the type is `text` and this is provided, then it must be an array of strings from which the user will be invited to select one.
* `controlled.allowOtherValues` -- if provided and true, occurring in a parameter with `controlled.options`, then the user is able to enter other values that those provided in the dropdown.
* `controlled.fetchOptions` -- if the type is `text` and this is provided, then it is a specification for how the UI should fetch option values to be presented to the user, by reference to the running FOLIO system. The value of this parameter can take two forms:
  * It may be a full specification: an object with the following keys:
    * `wsapiPath` -- the path of the WSAPI call that must be made to an Okapi-mediated service to obtain the elements of the controlled vocabulary.
    * `query` -- if provided, a value to be used as the `query` parameter of the WSAPI call. This is useful, for example, is searching in mod-settings and limiting to a specific scope.
    * `sortSpec` -- if provided, a CQL sort-specification to be used in the WSAPI call. If this is provided but no `query` is specified, then `cql.allRecords=1` (find all records) is used as the query.
    * `limit` -- if provided, a record-count limit to be passed as the `limit` parameter of the WSAPI call. When this is not specified, different services have different default behaviour, but defaulting to ten records is common.
    * `resultPath` -- the path to the part of the WSAPI's HTTP response that contains the records. Can be faceted, e.g. if the response has a `data` obeject which contains a list of records is called `recs`, then `data.recs` may be used.
    * `queryField` -- the name of the field within the result records whose value should be used in SQL searches -- typically `id`.
    * `displaySpec` -- a specification for how to build string shown to user for each option. This takes the form of [a Handlebars template](https://handlebarsjs.com/guide/) -- often just `name` when the records have a `name` field.
  * If the `controlled.fetchOptions` value is a simple string, then it is taken to be a reference to one of a small number of pre-packaged controlled vocabularies (`locations`, `userGroups`, etc.) which are [defined in the source code](https://github.com/folio-org/ui-ldp/blob/master/src/util/vocabDescriptors.js). These pre-packaged vocabularies are also useful examples of how the full specification facility can be used. The pre-packaged vocabularies will likely cover most requirements.
* `disabled` -- if provided and true, then the parameter is disabled, and will be omitted from the generated form.


## Setting up the Reporting app to find your report

Once a report or reports have been pushed to GitHub or GitLab, you can make the Reporting app aware of them by going to **Settings** &rarr; **Reporting** &rarr; **Report repositories**.

This page lists all the report sources currently known. You can edit the information about existing sources, or click the `+` sign at the bottom of the list to add a new source. Then enter the git site username, repo name, branch and directory. For example, to use reports from https://github.com/MikeTaylor/dummy-ldp-queries/tree/main/queries enter:
* Git user `MikeTaylor`
* Repository name within user's area `dummy-ldp-queries`
* Branch of the specified repository `main`
* Directory within repository `queries`


## Using your report

Go the the Reporting app and click on the "Run report" tab in the left bar. The list of reports that appears will include your new report (and any others from the same directory).

Click on the report's name to display the form generated from its metadata, fill in the form and click **Submit**.

When the results appear, they can be exported in CSV format using the **CSV** button at top right, and the resulting file loaded into a spreadsheet.

The results can be dismissed by the cross at top left.


