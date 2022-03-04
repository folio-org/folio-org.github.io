---
layout: page
title: Create a new FOLIO module and do initial setup
permalink: /guidelines/create-new-repo/
menuInclude: no
menuTopTitle: Guidelines
---

## Introduction

These are notes to assist developers with creating a new FOLIO module as a repository,
preparing initial setup files, and configuration.

## Choose module name

Take care to choose wisely for the [module name](/guidelines/naming-conventions/#module-names). It will be disruptive to [change that](/guides/rename-module/).

## DevOps assistance

Most setup can be done by your development team, following this document.

If assistance is needed then [raise a FOLIO DevOps Jira ticket](/faqs/how-to-raise-devops-ticket/#general-folio-devops)
so that the correct permissions are set on the repo, and an appropriate Jira project can be created (if applicable).
There is one example at [FOLIO-2892](https://issues.folio.org/browse/FOLIO-2892).

## Configuration at GitHub

If the "New" button is not available to you at [github.com/folio-org](https://github.com/folio-org) then [contact](/community/#collaboration-tools) FOLIO DevOps.

Otherwise follow the GitHub prompts to create a new repository, and if needed to then import an existing repository.

The following first few items can only be done by the initial creator of the repository or its owners, and should happen early. Use its "Settings" area.
(If the "Settings" tab is not available to you, then see the "support" advice above.)

Disable the Issues and Wiki via Settings. We use the FOLIO resources instead.
Do this as soon as possible, so that issues are created in the relevant project's FOLIO issue tracker.

Ensure that access is configured for the relevant FOLIO GitHub [Teams](https://github.com/orgs/folio-org/teams).
Note that front-end module repositories also need the "bots" Team (with Write access) to enable the "[translations](/guides/commence-a-module/#front-end-translations)" facility.

Add a concise "About" description to the GitHub repository. Consider that this will also be utilised elsewhere. This description is near the top-right of your GitHub front page.
(If the "Edit" button is not available to you, then see the "support" advice above.)

## Add initial files

There are facilities to assist with starting a new module.
For front-end modules see [stripes-cli](https://github.com/folio-org/stripes-cli).
For back-end RMB-based modules see [mod-rmb-template](https://github.com/folio-org/mod-rmb-template).
Otherwise follow the structure of a relevant existing module.

Follow the [Naming conventions](/guidelines/naming-conventions/) guidelines.

The [Commence a module - structure and configuration](/guides/commence-a-module/) guide explains a consistent layout.

Compare initial files with an existing FOLIO module repository (e.g.
[mod-notes](https://github.com/folio-org/mod-notes),
[ui-users](https://github.com/folio-org/ui-users)).
The Stripes/UI/backend modules might be slightly different (e.g. CHANGELOG.md = NEWS.md).

Add the required [PERSONAL_DATA_DISCLOSURE.md](https://github.com/folio-org/personal-data-disclosure) form.

Add the required LICENSE and CONTRIBUTING.md and README.md files.

Ensure that the required copyright and license statement is near the top of the README.
Use the initial year of creation for the date.
(In subsequent years it will become a range.)

Ensure that any package.json and pom.xml etc. type of configuration file has the appropriate required "licence" elements.

In the bottom "Further information" section of the README, add a link to your project issue tracker.

Refer to the Wiki [FOLIO Code of Conduct](https://wiki.folio.org/display/COMMUNITY/FOLIO+Code+of+Conduct).

Add [.editorconfig](/faqs/how-to-use-editorconfig/) configuration file.

Add initial NEWS.md or CHANGELOG.md file.

If necessary, add a basic .gitignore file.
Developers will have [their own ~/.gitignore_global](/guides/developer-setup#use-gitignore) to handle most.

## Add specific configuration files

Follow similar existing repositories.

The [Commence a module - structure and configuration](/guides/commence-a-module/) guide explains a consistent layout and explains each type of file (so not repeated here).

### Backend specific

For back-end modules: descriptors/ModuleDescriptor-template.json, Dockerfile, POM, Jenkinsfile, etc.

Get the initial basic source files and other configuration files added first.
Then add the Jenkinsfile to initiate the CI processing.
Do this early so that CI can assist.
**Note:**
Its Jenkinsfile needs to be committed directly to master branch.
If it is done via a pull-request then that will fail, as the initial base Sonar scan for master branch has not yet run.

### Frontend specific

For front-end modules: package.json, .eslintrc, Jenkinsfile, etc.

Get the initial basic source files and other configuration files added first.
Also add the Jenkinsfile to initiate the CI processing.
Do this early so that CI can assist.
**Note:**
The Jenkinsfile setting "`runSonarqube = true`" needs to be committed directly to master branch.
If it is done via a pull-request then that will fail, as the initial base Sonar scan for master branch has not yet run.

## Module documentation

As explained in the FAQ [Where is developer documentation located](/faqs/where-is-developer-documentation-located/), one of the principles of FOLIO module development is that module documentation is managed along with its source code.

Consider the guide to [increase visibility of module documentation](/guides/visibility-module-docs/)
which provides some tips for module developers to improve the discoverability and usability of their module documentation.

## Configure Lokalise

For UI modules, when the new repository is ready, and its [translations](/guides/commence-a-module/#front-end-translations) directory is configured as explained,
then add the new module to Lokalise to enable the [translators](/faqs/explain-i18n/) to operate.

Configuration of the new repository can only be done by people with appropriate access.
See the folio-infrastructure lokalise-push [procedure](https://github.com/folio-org-priv/folio-infrastructure/tree/master/lokalise-push).

## Next steps

When a new module has been fully established and its artifacts are being deployed, follow the guides to [install](/faqs/how-to-install-new-module/) it to platform and reference environments for snapshot and testing builds.

<div class="folio-spacer-content"></div>

