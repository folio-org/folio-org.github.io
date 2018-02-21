---
layout: page
title: Create a new FOLIO module and do initial setup
permalink: /doc/create-new-repo/
menuInclude: no
menuTopTitle: Documentation
---

These are notes to assist developers with creating a new FOLIO module as a repository.
Initial setup files and configuration.

Take care to choose wisely for the repository name. It is disruptive to change that.

The following first few items can only be done by the initial creator of the repository or its owners, and should happen early. Use its "Settings" area.

Ensure that access is configured for the relevant FOLIO GitHub [Teams](https://github.com/orgs/folio-org/teams) (e.g. foliodev-core, stripes).

Disable the Issues and Wiki via Settings. We use the FOLIO resources.

Add a concise description to the GitHub repository. Consider that this will also be used elsewhere.

Copy initial files from an existing FOLIO module repository (e.g.
[mod-notes](https://github.com/folio-org/mod-notes),
[stripes-smart-components](https://github.com/folio-org/stripes-smart-components)).
The Stripes/UI/backend modules might be slightly different (e.g. CHANGELOG.md = NEWS.md).

Add LICENSE and CONTRIBUTING.md and README.md files.

Ensure that the copyright and license statement is near the top of the README.
Use the initial year of creation for the date.

Ensure that any package.json and pom.xml etc. type of configuration file has the appropriate "licence" elements.

Add [.editorconfig](/doc/setup#use-editorconfig-for-consistent-whitespace) file.

Add initial NEWS.md or CHANGELOG.md file.

If necessary, add a basic .gitignore file.
Developers will have [their own ~/.gitignore_global](/doc/setup#use-gitignore) to handle most.

Add other configuration files. Follow similar existing repositories.
For back-end modules: descriptors/ModuleDescriptor-template.json, Dockerfile, etc.
For front-end modules: package.json, .eslintrc, etc.

Open a Jira issue, so that the project is integrated into Jenkins, the correct permissions are set on the repo, and an appropriate Jira project can be created (if applicable). Add the label 'ci'.



