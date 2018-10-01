---
layout: page
title: Describe schema and properties
permalink: /guides/describe-schema/
menuInclude: no
menuTopTitle: Guides
---

Each property of an API schema has a "description" field.
These are [utilised](https://issues.folio.org/browse/FOLIO-1447) to explain the purpose of the properties.
Each schema also has a top-level description.

Refer to an example at [mod-circulation-storage](https://github.com/folio-org/mod-circulation-storage/blob/master/ramls/loan.json)
and its generated [documentation](https://s3.amazonaws.com/foliodocs/api/mod-circulation-storage/loan-storage.html#loan_storage_loans__loanId__get) (select the "Response" tab).

Library subject-matter experts can assist to improve these descriptions.

The continuous-integration facility assesses the JSON Schema files of RAML-using back-end modules to determine any missing descriptions.
At GitHub, detected issues are listed on the pull-request front page.

For any branch or pull-request build, follow the "details" link via the coloured checkmark through to Jenkins.
Then see "Artifacts" at the top-right for the "Lint raml-cop Report".

The analysis can also be [run locally](/guides/raml-cop/).

To contribute updates, either send a pull-request with the changes or add to a Jira issue tracker.
