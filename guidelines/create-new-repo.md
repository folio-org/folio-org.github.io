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

## Configuration at GitHub

If the "New" button is not available to you at [github.com/folio-org](https://github.com/folio-org) then seek FOLIO DevOps [assistance](/faqs/how-to-raise-devops-ticket/).

The repository must be "public" and not the default "private".

Otherwise follow the GitHub prompts to create a new repository, and if needed to then import an existing code base.

The following first few items can only be done by the initial creator of the repository or its owners, and should happen early. Use its "Settings" area.
(If the "Settings" tab is not available to you, then see the "support" advice above.)

<div class="attention">
Note: The person who created the repository will automatically have "Admin" permissions.
So it is their responsibility follow-up to ensure that these tasks are done.
</div>

### Disable Issues and Wiki

Disable the Issues and Wiki via Settings. We use the FOLIO [Collaboration tools](/community/#collaboration-tools) and resources instead.

Do this as soon as possible, so that issues are created in the relevant project's FOLIO issue tracker.

Add a link from the project README to its issue tracker (see instructions below).

### Access for relevant Teams

Ensure that access is configured for the relevant FOLIO GitHub [Teams](https://github.com/orgs/folio-org/teams).

Note that front-end module repositories also need the "bots" Team (with Write access) to enable the "[translations](/guides/commence-a-module/#front-end-translations)" facility.

### Concise About description

Add a concise "About" description to the GitHub repository. Consider that this will also be utilised elsewhere. This description is near the top-right of your GitHub front page.
(If its "Edit" button is not available to you, then see the "support" advice above.)

This would be a shortened version of the "Introduction" section of the project README.

For backend module repositories, note that Docker Hub imposes a [content length limit](https://github.com/peter-evans/dockerhub-description#content-limits) of 100 bytes.

### Branch protection and required checks

Note: The configuration of "branch protection" and its "required checks" can only be done after there has been an initial pull-request (and must be done within one week of its opening, as GitHub will expire the opportunity).

Use the "Settings > Branches > Add classic branch protection rule" to enable for the mainline branch.

Ensure that the branch protection required status checks include the "license/cla" for the required [FOLIO Project Contributor License Agreement](/guidelines/cla-process/).

For [front-end](#add-specific-configuration-files) repositories, when the GitHub Actions Workflows are operational then required checks can be configured here. Follow similar repositories.

For [back-end](#add-specific-configuration-files) repositories, when the Jenkinsfile is operational then required checks can be configured here. Follow similar repositories.

## Add initial files

There are various [module development bases](/guides/#module-development-bases) and facilities to assist with starting a new module.
Also follow the structure of a relevant well-configured existing module.

Follow the [Naming conventions](/guidelines/naming-conventions/) guidelines.

The [Commence a module - structure and configuration](/guides/commence-a-module/) guide explains a consistent layout.

Compare initial files with an existing FOLIO module repository (e.g.
[mod-notes](https://github.com/folio-org/mod-notes),
[ui-users](https://github.com/folio-org/ui-users)).
The Stripes/UI/backend modules might be slightly different (e.g. CHANGELOG.md = NEWS.md).

Add the required [PERSONAL_DATA_DISCLOSURE.md](https://github.com/folio-org/personal-data-disclosure) form.

Add the required LICENSE (taken from [apache.org](https://www.apache.org/licenses/LICENSE-2.0.txt)) and CONTRIBUTING.md and README.md files.

Ensure that the required copyright and license statement is near the top of the README.
Use the initial year of creation for the date.
(In subsequent years it will become a [date range](https://folio-org.atlassian.net/browse/FOLIO-1021).)

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
The Jenkinsfile needs to be committed directly to master branch.
If it is done via a pull-request then that will fail, as the initial base Sonar scan for master branch has not yet run.

**Note:** The [api-lint](/guides/api-lint/) and [api-schema-lint](/guides/describe-schema/) and [api-doc](/guides/api-doc/) are now done via GitHub Workflows, not via Jenkinsfile.

### Frontend specific

For front-end modules: package.json, .eslintrc, GitHub Workflows, etc.

Get the initial basic source files and other configuration files added first.

New front-end repositories will use GitHub Actions Workflows.
Refer to the document [Centralized UI Workflows](https://github.com/folio-org/.github/blob/master/README-UI.md)
and follow an existing similar repository.

When the code and configuration is in place, then this new repository needs to be manually added to Sonarcloud.
Seek FOLIO DevOps [assistance](/faqs/how-to-raise-devops-ticket/).

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

When the above-mentioned steps are completed, and when the new module has been fully established and its artifacts are being deployed, follow the guides to [install](/faqs/how-to-install-new-module/) it to platform and reference environments for snapshot builds.

<div class="folio-spacer-content"></div>


