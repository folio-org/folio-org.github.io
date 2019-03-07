---
layout: page
title: Describe schema and properties
permalink: /guides/describe-schema/
menuInclude: no
menuTopTitle: Guides
---

Each property of an API schema has a "description" field.
These are utilised to explain the purpose of the properties and enable their use.
Each schema also has a top-level description explaining the overall purpose.

Refer to some examples.
The first link is the source file.
The second link is the generated API documentation, displays one place where that schema is used.
* [mod-circulation-storage loan.json](https://github.com/folio-org/mod-circulation-storage/blob/master/ramls/loan.json)
and generated [documentation](https://s3.amazonaws.com/foliodocs/api/mod-circulation-storage/p/loan-storage.html#loan_storage_loans__loanid__get).
* [mod-circulation request.json](https://github.com/folio-org/mod-circulation/blob/master/ramls/request.json)
and generated [documentation](https://s3.amazonaws.com/foliodocs/api/mod-circulation/p/circulation.html#circulation_requests__requestid__get).

Library subject-matter experts can also assist to improve these descriptions.

Add a "description" for each of the property elements within a "properties" object. Note that there may also be nested properties objects.

Some properties might have supporting attributes such as "pattern" for a UUID, "enum" to enumerate the allowed values, "format, "default", "uniqueItems", etc. and the "required" sections of the schema.
When adding new properties, utilise these from the start.

For existing properties, if those are not already present, then define such constraints in prose in the description. They can later be formalised, perhaps as a new interface version.

The relevant RAML files that utilise the schema can provide valid examples, and describe other constraints.

Use the schema property description to declare controlled vocabularies and where to find reference data.

The description can be long text, but not use markup.

See other guidance at [FOLIO-1447](https://issues.folio.org/browse/FOLIO-1447)
and [FOLIO-1551](https://issues.folio.org/browse/FOLIO-1551).

To contribute updates, either send a pull-request with the changes or add to a Jira issue tracker.

The continuous-integration facility assesses the JSON Schema files of all RAML-using back-end modules to determine any missing descriptions.
At GitHub, detected issues are listed on the front page of each pull-request.
For any branch or pull-request build, follow the "details" link via the coloured checkmark through to Jenkins.
Then see "Artifacts" at the top-right for the "Lint raml-cop Report".
The analysis can also be [run locally](/guides/raml-cop/).
