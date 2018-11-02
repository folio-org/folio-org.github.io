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

Refer to an example at [mod-circulation-storage](https://github.com/folio-org/mod-circulation-storage/blob/master/ramls/loan.json)
and its generated [documentation](https://s3.amazonaws.com/foliodocs/api/mod-circulation-storage/loan-storage.html#loan_storage_loans__loanId__get) (select the "Response" tab).

Library subject-matter experts can also assist to improve these descriptions.

Add a "description" for each of the property elements within a "properties" object. Note that there may also be nested properties objects.

Some properties might have supporting attributes such as "pattern" for a UUID, "enum" to enumerate the allowed values, "default", etc.
Otherwise define constraints as part of the "description".

The relevant RAML file that utilises the schema can provide valid examples, and describe other constraints.

See other guidance at [FOLIO-1447](https://issues.folio.org/browse/FOLIO-1447)
and [FOLIO-1551](https://issues.folio.org/browse/FOLIO-1551).

The continuous-integration facility assesses the JSON Schema files of all RAML-using back-end modules to determine any missing descriptions.
At GitHub, detected issues are listed on the front page of each pull-request.

For any branch or pull-request build, follow the "details" link via the coloured checkmark through to Jenkins.
Then see "Artifacts" at the top-right for the "Lint raml-cop Report".

The analysis can also be [run locally](/guides/raml-cop/).

To contribute updates, either send a pull-request with the changes or add to a Jira issue tracker.
