---
layout: page
title: Create a new FOLIO module and do initial setup
---

These are notes to assist developers with creating a new FOLIO module as a repository.
Initial setup files and configuration.

Add a concise description to the GitHub repository. Consider that this will also be used elsewhere.

Ensure that access is configured for the FOLIO GitHub Teams.

Disable the Issues and Wiki via Settings. We use the FOLIO resources.

Copy initial files from an existing FOLIO module repository. Note that Stripes/UI/backend modules might be slightly different (e.g. CHANGELOG.md = NEWS.md):

Add LICENSE and CONTRIBUTING.md and README.md files.

Ensure the copyright and license statement is near the top of the README.

Ensure that any package.json and pom.xml etc. type of configuration file has the appropriate "licence" elements.

Add .editorconfig file.

Add initial NEWS.md or CHANGELOG.md file.

Add a basic .gitignore file. Developers will have their own ~/.gitignore_global to handle most.

Add other configuration files. Follow similar existing repositories.
For back-end modules: DeploymentDescriptor.json, ModuleDescriptor.json, Dockerfile, etc.
For front-end modules: package.json, .eslintrc, etc.

Open a Jira issue, so that the project is integrated into Jenkins, the correct permissions are set on the repo, and an appropriate Jira project can be created (if applicable). Add the label 'ci'.



