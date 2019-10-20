---
layout: page
title: Branch preview on Kubernetes infrastructure
permalink: /guides/branch-preview-kubernetes/
menuInclude: no
menuTopTitle: Guides
---

## Introduction

Branch preview mode allows developers, product owners, and other interested parties to "preview"
changes to FOLIO components on a live FOLIO system before committing them to the master
branch. This can be acheived by opening a pull request against platform-core and specifying preview artifacts in the package.json and okapi-install.json files for front and back end modules respectively.

**NOTE:** This is a proof-of-concept applying only to modules included in platform-core

## How it works

Opening a pull request against platform-core triggers a build of a FOLIO tenant on a Kubernetes cluster dedicated to CI. The tenant will be built using the modules specified in the `okapi-install.json` `install-extras.json` files on the branch of platform-core where the PR is issued from. A stripes bundle for the tenant is built based on what is specified in the `package.json` file and deployed to Amazon s3. Jenkins will mark up the pull reuqest with a link to the frontend.

The following steps make up a PR preview build:

* A tenant is created on the Kubernetes FOLIO system for each build iteration of the PR. The tenant
naming convention is "`GITHUB_PROJECT NAME_ + PR_NUMBER_ + JENKINS_BUILD_NUMBER`".
For example, PR 64 for ui-users would create a tenant called 'ui_users_64_1'.  The tenant
admin user for the tenant is the same as the tenant name + 'admin'.  For example, the tenant
admin user for tenant, ui_users_64_1, would be 'ui_users_64_1_admin'. The tenant admin password
in all cases is 'admin'.

* Tenant modules are enabled, and reference and sample data for select modules are loaded
for the tenant.

* The stripes webpack is distributed to an S3 web service.
The UI is configured for the correct tenant and Okapi instance.
An AWS S3 URL to the UI is appended to the pull request.

All of the above steps happen more or less sequentially, so if a step fails for whatever reason,
the build is marked as 'FAILED'.

### Triggering a pull request on platform-core

*Instructions for triggering a PR go here (any required changes to Jenkinsfile to activate)*

### Including front-end preview artifacts in a pull request to platform core

In order to build a preview system using front end code that has not been merged to master, edit the `package.json` file on a branch of platform-core and edit the version of the module you would like to preview replacing the version number with a pointer to a github branch.

For example, to build a preview system using unmerged code for ui users on a branch called "my-feature-branch", the entry for `@folio/users` in `package.json` might look like this:

```
    ...
    "@folio/tenant-settings": "2.13.1",
    "@folio/users": "git+https://github.com/folio-org/ui-marccat.git#my-feature-branch",
    "react": "~16.8.6",
    ...
```

### Publishing backend preview artifacts

It may be desirable to create preview build that includes changes to backend modules that have not been merged into master. To achieve this, open a pull request on the backend module or modules with the publishPreview variable set to true in the main config, and in the docker configuration. A Jenkinsfile for a typical backend module might look like this:

```
buildMvn {
  publishModDescriptor = 'yes'
  publishAPI = 'yes'
  mvnDeploy = 'yes'
  runLintRamlCop = 'yes'
  publishPreview = 'yes'

  doDocker = {
    buildJavaDocker {
      publishMaster = 'yes'
      publishPreview = 'yes'
      healthChk = 'yes'
      healthChkCmd = 'curl -sS --fail -o /dev/null  http://localhost:8081/apidocs/ || exit 1'
    }
  }
}
```

Making these changes will achieve the following:
* If the docker build is successful, the image will be deployed temporarily to an internal docker registry at repository.folio.org. The image will be tagged with the version number, the pr number, and the build number. For example, mod-users-15.6.1-SNAPSHOT.11.2 where “15.6.1-SNAPSHOT” is the version, 11 is the PR number, and 2 is the build number.
* A modified module descriptor will be posted to okapi-preview.ci.folio.org
* The module will be deployed to the preview CI kubernetes namespace.

### Including backend preview artifacts in a platform

Preview builds are driven by pull requests against platform-core or platform-complete. To include a preview artifact, update the okapi-install.json file and replace the id of the module you would like to preview with the preview version. The preview version is the module’s regular version number, with the pr and build numbers appended (mod-name-version.pr.build.) For example:

...
{
  "id": "mod-users-SNAPSHOT-15.6.1",
  "action": "enable"
},...

should be replaced with:

...
{
  "id": "mod-users-SNAPSHOT-15.6.1.11.2",
  "action": "enable"
},...

Bear in mind that the module descriptor for this preview artifact is not published to the folio-registry, and is only available on okapi-preview.ci.folio.org.


## Current limitations

* Only modules included in platform-core are currently deployed to Kubernetes on build. This means previews can only be built for modules included in platform-core.

* Only the latest three releases and two snapshots of backend modules are retained in Kubernetes. A preview cannot be built using older dependencies.

* There can be multiple build iterations for each PR.  A new tenant will be created for each
iteration. However, only one Stripes bundle is retained - the one produced from the
latest build iteration.

* When a PR is closed, then all AWS S3 resources associated with the PR are removed.


## Feedback

Please post any issues or additional questions to the #devops channel on FOLIO Slack.

