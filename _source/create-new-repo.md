---
layout: source
title: Creating a New Module as a Repository
heading: Creating a New Module as a Repository
permalink: /source/create-new-repo/
---

These are notes to assist developers with creating a new FOLIO module as a repository.
Initial setup files and configuration.

Add a concise description to the GitHub repository. Consider that this will also be used elsewhere.

Ensure that access is configured for the FOLIO GitHub Teams.

Disable the Issues and Wiki via Settings. We use the FOLIO resources.

Copy initial files from an existing FOLIO module repository (e.g.
[mod-notes](https://github.com/folio-org/mod-notes),
[stripes-util-notes](https://github.com/folio-org/stripes-util-notes)).
The Stripes/UI/backend modules might be slightly different (e.g. CHANGELOG.md = NEWS.md).

Add LICENSE and CONTRIBUTING.md and README.md files.

Ensure the copyright and license statement is near the top of the README.

Ensure that any package.json and pom.xml etc. type of configuration file has the appropriate "licence" elements.

Add [.editorconfig](/devtools/codingstyle) file.

Add initial NEWS.md or CHANGELOG.md file.

If necessary, add a basic .gitignore file.
Developers will have [their own](/devtools/codingstyle/) ~/.gitignore_global to handle most.

Add other configuration files. Follow similar existing repositories.
For back-end modules: descriptors/ModuleDescriptor-template.json, Dockerfile, etc.
For front-end modules: package.json, .eslintrc, etc.

Open a Jira issue, so that the project is integrated into Jenkins, the correct permissions are set on the repo, and an appropriate Jira project can be created (if applicable). Add the label 'ci'.



