---
layout: page
title: Branch preview on Kubernetes infrastructure
permalink: /guides/branch-preview-kubernetes/
menuInclude: no
menuTopTitle: Guides
---

## Introduction

Branch preview mode allows developers, product owners, and other interested parties to "preview"
changes to FOLIO components on a live FOLIO system before merging them to the master branch. It's particularly useful for UI developers to either test or demonstrate feature branch code, but can also be used by backend developers to test module API features in the context of a FOLIO build.  The process includes a full or partial FOLIO build of either platform-complete or platform-core using the master branch of each of those repositories as a baseline for the build when a PR is opened.  Developers can substitute backend module feature branches or the master branch for released modules in the baseline in order to complement frontend module dependencies and other backend dependencies.


## How it works

The following steps describe the process of creating a FOLIO preview build based on
platform-core that consists of a frontend module feature branch and a backend module feature
branch.  In this example we are including branch builds of mod-tags and ui-tags.

### Step 1

Edit the 'Jenkinsfile' for the backend module branch.  Add the 'doKubeDeploy' and
'publishPreview' parameters.  Example Jenkinsfile configuration:

'''
buildMvn {
  publishModDescriptor = true
  publishAPI = true
  mvnDeploy = true
  runLintRamlCop = true
  doKubeDeploy = true     <---- Add this
  publishPreview = true   <---- Add this

  doDocker = {
    buildJavaDocker {
      publishMaster = true
      publishPreview = true  <---- Add this
      healthChk = true
      healthChkCmd = 'curl -sS --fail -o /dev/null  http://localhost:8081/apidocs/ || exit 1'
    }
  }
}
'''

Open PR for backend module branch.   This will initiate a branch build of the backend
module and deploy to a FOLIO kubernetes cluster.  Branch build artifacts are versioned
POM_VERSION-PR_NUMBER.JENKINS_BUILD_NUMBER.   For example,  mod-tags-0.6.0-SNAPSHOT.35.1
If build is successful, proceed to the next step.

### Step 2

Clone https://github.com/folio-org/platform-core.  Create a branch and create a file
called '.pr-custom-deps.json' in the top-level directory of the checkout.  This is a json
list that includes the modules we are substituting for the default released modules currently
specified on master.

Example .pr-custom-deps.json file:

'''
[
  {
   "id" : "mod-tags-0.6.0-SNAPSHOT.35.1",
   "action" : "enable"
  }
]
'''

Edit 'package.json'.  Specify the branch of ui-tags we want to include in the build.

'''
"dependencies": {
    "@folio/calendar": "2.7.2",
    "@folio/checkin": "1.10.1",
    "@folio/checkout": "2.0.1",
    "@folio/circulation": "1.12.0",
    "@folio/developer": "1.11.0",
    "@folio/inventory": "1.13.3",
    "@folio/myprofile": "1.8.0",
    "@folio/plugin-find-instance": "1.6.0",
    "@folio/plugin-find-user": "1.9.1",
    "@folio/requests": "1.14.3",
    "@folio/search": "1.10.0",
    "@folio/servicepoints": "1.4.2",
    "@folio/stripes": "2.12.1",
    "@folio/tags": "folio-org/ui-tags#pr-preview-test", <--- HERE
    ...
'''


Open a pull request against platform-core master branch.  This triggers a build of a FOLIO tenant on a Kubernetes cluster dedicated to CI. The tenant will be built using the modules specified in the 'okapi-install.json'.  If any modules are optionally specified in '.pr-custom-deps.json', they will replace the modules in 'okapi-install.json'.  A stripes bundle for the tenant is built based on what is specified in the `package.json` file and deployed to an Amazon s3 bucket. Jenkins will mark up the pull request with a link to the stripes bundle and the tenant admin user name.  The password is always 'admin'.


## Notes

* Only the latest three releases and two snapshots (master branch) of backend modules are
retained on the Kubernetes cluster.  A preview cannot be built using older dependencies.

* There can be multiple build iterations for each PR.  A new tenant will be created for each iteration.  However, only one Stripes bundle is retained - the one produced from the latest build iteration.

* The FOLIO PR preview tenant and AWS S3 bucket will remain available until the PR is closed.

* When closing platform PR, DO NOT MERGE, and remove the test branch.

