---
layout: page
title: Create a new FOLIO module and do initial setup
permalink: /guidelines/create-new-repo/
menuInclude: no
menuTopTitle: Guidelines
---

These are notes to assist developers with creating a new FOLIO module as a repository.
Initial setup files and configuration.

If the "New" button is not available to you at [github.com/folio-org](https://github.com/folio-org) then [contact](/community/#collaboration-tools) FOLIO infrastructure (e.g. via the issue tracker or the #support channel).
Otherwise follow the GitHub prompts to create a new repository, and if needed to then import an existing repository.

Take care to choose wisely for the [repository name](/guidelines/naming-conventions/#module-names). It can be disruptive to change that.

The following first few items can only be done by the initial creator of the repository or its owners, and should happen early. Use its "Settings" area.

Disable the Issues and Wiki via Settings. We use the FOLIO resources instead.

Ensure that access is configured for the relevant FOLIO GitHub [Teams](https://github.com/orgs/folio-org/teams) (e.g. foliodev-core, stripes).

Add a concise description to the GitHub repository. Consider that this will also be used elsewhere.

Copy initial files from an existing FOLIO module repository (e.g.
[mod-notes](https://github.com/folio-org/mod-notes),
[stripes-smart-components](https://github.com/folio-org/stripes-smart-components)).
The Stripes/UI/backend modules might be slightly different (e.g. CHANGELOG.md = NEWS.md).

Add LICENSE and CONTRIBUTING.md and README.md files.

Ensure that the copyright and license statement is near the top of the README.
Use the initial year of creation for the date.

Ensure that any package.json and pom.xml etc. type of configuration file has the appropriate "licence" elements.

Add [.editorconfig](/guides/developer-setup#use-editorconfig-for-consistent-whitespace) file.

Add initial NEWS.md or CHANGELOG.md file.

If necessary, add a basic .gitignore file.
Developers will have [their own ~/.gitignore_global](/guides/developer-setup#use-gitignore) to handle most.

Add other configuration files. Follow similar existing repositories.
For back-end modules: descriptors/ModuleDescriptor-template.json, Dockerfile, Jenkinsfile, etc.
For front-end modules: package.json, .eslintrc, etc.

Follow the [Naming conventions](/guidelines/naming-conventions/) guidelines.

The [Commence a module - structure and configuration](/guides/commence-a-module/) guide explains a consistent layout.

Open a Jira issue, so that the project is integrated into Jenkins, the correct permissions are set on the repo, and an appropriate Jira project can be created (if applicable). Add the label 'ci'.
There is one example at [FOLIO-949](https://issues.folio.org/browse/FOLIO-949).
Suggest a short name for the Jira project.
