---
layout: page
title: Describe schema and properties
permalink: /guides/describe-schema/
menuInclude: no
menuTopTitle: Guides
---

Each property of an API schema has a "description" attribute.
These are utilised to explain the purpose of the properties and enable their use.
Each schema also has a top-level description explaining the overall purpose.

The [API documentation](/reference/api/) is generated from these schema and the API Description files that refer to them.

Refer to some examples.
The first link is the source JSON Schema file.
The second link is the generated API documentation, displaying one place where that schema is used.
* [mod-circulation-storage loan.json](https://github.com/folio-org/mod-circulation-storage/blob/master/ramls/loan.json)
and generated [documentation](https://s3.amazonaws.com/foliodocs/api/mod-circulation-storage/p/loan-storage.html#loan_storage_loans__loanid__get).
* [mod-circulation request.json](https://github.com/folio-org/mod-circulation/blob/master/ramls/request.json)
and generated [documentation](https://s3.amazonaws.com/foliodocs/api/mod-circulation/p/circulation.html#circulation_requests__requestid__get).

(NOTE: Those examples are demonstrating the general task of documentation.
These will be updated when [FOLIO-1925](https://issues.folio.org/browse/FOLIO-1925) is completed to provide actual examples following this documentation.)

Library subject-matter experts and developers, please assist to improve all schema descriptions.

Add a "description" for each of the property elements within a "properties" object. Note that there may also be nested properties objects.

Some properties might have supporting attributes such as "pattern" for a UUID, "enum" to enumerate the allowed values, "format, "default", "uniqueItems", etc. and the "required" sections of the schema.
When adding new properties, utilise these from the start.

For existing properties, if those are not already present, then define such constraints in prose in the description. They can later be formalised, probably as a new interface version.

Even when those supporting attributes are utilised, then it is still beneficial to provide a thorough "description". Ensure that it remains synchronised with any supporting attributes.

All of the properties should be well-documented, but it is specifically data properties, wherein the module is acting as a database, that require thorough description and specification. Consider the needs of facilities such as data reporting and data migration, where these teams require full knowledge of the data.

Documentation for each property should include:
* A description of what it means
* The precise domain of the property (range of values, controlled vocabulary, etc.)
* Whether it is required or optional
* Where to find referenced data, if the property is a foreign key
* Any other constraints on the data, e.g. only unique values

Some examples:

```
Property name:      username
Purpose:            The user's login name.  This also serves as a unique,
                    human-readable identifier for the user.
Domain:             String of alphanumeric Unicode characters, beginning
                    with an alphabetic character.  Maximum of 16 characters.
Required:           Yes
References:         N/A
Other constraints:  Unique, but may be reused after the user is deleted.

```

and

```
Property name:      patronGroup
Purpose:            The patron group that the user belongs to.
Domain:             UUID
Required:           Yes
References:         "User Groups" /groups/{groupId} (e.g. mod-users)
Other constraints:  None

```

The schema property "description" can only be a single long text string, and can not use markup. So just concatenate the relevant information.

The relevant API Description files that utilise the schema can provide valid examples. RAML files can also provide additional [RAML documentation node](https://github.com/raml-org/raml-spec/blob/master/versions/raml-10/raml-10.md#user-documentation) entries, which can utilise Markdown either in-line or via included files (e.g. [mod-courses](/reference/api/#mod-courses)). In this way other constraints be described, also with links to supporting resources.

To contribute updates, either send a pull-request with the changes or add to a Jira issue tracker.

The continuous-integration facility assesses the JSON Schema files of all RAML-using and OpenAPI-using back-end modules to determine any missing descriptions.
At GitHub, detected issues are listed on the front page of each pull-request.
For any branch or pull-request build, follow the "details" link via the coloured checkmark through to Jenkins.
Then see "Artifacts" at the top-right for the processing report.
The analysis can also be run locally with the [api-schema-lint](https://github.com/folio-org/folio-tools/tree/master/api-schema-lint) tool.
