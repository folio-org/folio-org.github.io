---
layout: page
title: Pull requests checklists
permalink: /guidelines/pull-requests-checklists/
menuInclude: no
menuTopTitle: Guidelines
---

## Introduction

This document defines the checklists for creating and reviewing various types of pull-request (PR).

## Backend pull request checklist

* Do the changes meet the intended purpose described in the feature or story?
* Do the tests reflect the change in behaviour?
  * Do the tests describe scenarios described in the story or feature?
  * Do the tests describe common failure or validation scenarios?
* Has the API changed? (If yes, refer to the interface change checklist.)
  * Is the change compatibility breaking? (link to guidance, If yes, refer to the breaking interface change checklist)
* Does the change alter or remove existing requests to other modules, or introduce new requests? (if yes, refer to external requests / dependencies checklist)?
* Do the automated checks pass (e.g. tests, sonar, lint)?
* Does each PR name reference a JIRA issue for the correct project (at the beginning of the name)?
  * Does that issue have a fix version?
* Should the implementation version change (link to guidance)?
* Are any of the maven library dependencies a snapshot or pre-release version?

## Interface change checklist

* Do the RAML and JSON schema checks pass (e.g. RAMLCop)?
* Has the interface version been updated?
  * In the module descriptor?
  * In the interface definition?
* Do new properties follow standards and conventions (see guidance)?
  * Does the name describe the property specifically?
  * Is the name formatted correctly (e.g. camel case)?
  * Do they use the correct types (e.g. ID references should be UUIDs)?
  * Are server derived properties marked read only?
  * Does a new JSON object disallow additional properties?
  * Have the examples used in the RAML been updated?
  * Have the sample / reference records been updated?
* Do new endpoints follow standards and conventions (see guidance)?
  * Is the path formatted correctly (e.g. hyphens separating words)?
  * Is the endpoint nested within another resource appropriately?
  * Does the endpoint have its own permission in the module descriptor?
  * Does that permission exist in the [module-name].all (e.g. circulation.all) permission set?
  * Does the endpoint have the correct module permissions?
  * Are there sample or reference records for the new endpoint?
* Does the change fit in an existing interface or should a new interface be provided?
  * Is the current interface too large?
  * Do parts of the interface have different reasons to change?
  * Is a new endpoint experimental?

## Interface compatibility breaking change checklist

**Note**: Only merge the breaking change pull request when all other compatibility pull requests are also ready to be merged.

* Mark the pull request as do not merge.
* Identify modules dependent upon the changed interface:
  * using the Release Planning spreadsheet (e.g https://docs.google.com/spreadsheets/d/14zoV755B1kh5_j2CTzYAmHo1_N46RGh5-B4lyG6Qht8/edit#gid=0)
  * Using python script for checking against an existing environment - https://github.com/k-int/folio-tools/tree/interface-dependents)
* Are there JIRA issues in the relevant project for each dependent module?
  * Do they contain the appropriate level of detail? Which endpoints/schemas changed, etc.
  * Do they block the issue which introduces the breaking change?
* Are the JIRAs under active development?
  * If not, contact the project's PO and make sure they are aware of the urgency.
* Are pull requests raised to make each impacted module compatible?
  * Have they been approved?

## External requests / dependencies checklist

Use when changes are made to a dependent interface, either when:
* New features (e.g. new properties) of that interface are used,
* Requests are added to or removed from the implementation of an endpoint,
* Changes are needed for a breaking compatibility change in the interface.

Checklist:
* Has the interface version been updated in the module descriptor?
  * Is it at least the interface version where the feature was introduced?
  * If the new version is a major change, can dual support be offered?
* Are the dependent interface versions provided by another module?
* Are the correct module permissions expressed on each endpoint that uses the interface?

## Frontend pull request checklist

TODO: Add content.

