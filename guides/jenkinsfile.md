---
layout: page
title: Jenkinsfile to configure continuous integration steps
permalink: /guides/jenkinsfile/
menuInclude: no
menuTopTitle: Guides
---

## Introduction

Each project's git repository [structure](/guides/commence-a-module/) has a top-level file called `Jenkinsfile`
which is utilized by the continuous integration [process](/guides/automation/#jenkins)
to enable each project to specify certain additional build steps.

The library primarily supports two types
of development environments at this time -- Java-based Maven projects and Nodejs-based projects.

The files and main parameters are explained below for
[back-end](#back-end-modules).

Each parameter can be omitted to accept the default.

The values are: `true` or `false` (or the old syntax `'yes'` or `'no'`).

## Back-end modules

A typical Maven-based, server-side FOLIO module Jenkinsfile configuration might look like
the following.
See an example at
[mod-courses/Jenkinsfile](https://github.com/folio-org/mod-courses/blob/master/Jenkinsfile)

```
buildMvn {
  buildNode = 'jenkins-agent-java17'
  publishModDescriptor = true
  mvnDeploy = true

  doDocker = {
    buildJavaDocker {
      publishMaster = true
      healthChk = true
      healthChkCmd = 'wget --no-verbose --tries=1 --spider http://localhost:8081/admin/health || exit 1'
    }
  }
}
```

* `buildNode` -- The Jenkins node to run the CI build.
The default is `'jenkins-agent-java17'` if not specified.
The other available option is `'jenkins-agent-java21'`.
See FAQ [How to specify which Jenkins build image for CI](/faqs/how-to-specify-backend-java-ci/).
* `publishModDescriptor` -- Maven-based modules will generate the ModuleDescriptor.json file as
[explained](/guides/commence-a-module/#back-end-descriptors).
It will be published to the FOLIO Module Descriptor registry.
(Default: false)

* `mvnDeploy` -- Deploy Maven artifacts to FOLIO Maven repository.
(Default: false)

* <a id="do-upload-apidocs"></a>`doUploadApidocs` -- If the module also generates API documentation during its CI Maven phase, then upload to S3.
Uploads all generated docs found in the "`target/apidocs`" directory.
(Note: This is additional to "[api-doc](/guides/api-doc/)".)
More explanation at [FOLIO-3008](https://issues.folio.org/browse/FOLIO-3008).
Example: [mod-search](https://github.com/folio-org/mod-search/blob/master/Jenkinsfile).
(Default: false)

If we are creating and deploying a Docker image as part of the module's artifacts, specify
'doDocker' with 'buildJavaDocker' (for Spring-based modules instead use the 'buildDocker') and the following options:

* `publishMaster` -- Publish image to 'folioci' Docker repository on Docker Hub when building
'master' branch.
(Default: true)

* `healthChk` -- Perform a container healthcheck during build.  See 'healthChkCmd'.
(Default: false)

* `healthChkCmd` -- Use the specified command to perform container health check.   The
command is run *inside* the container and typically tests a REST endpoint to determine the
health of the application running inside the container.  Prefer `wget` over `curl` as Alpine
by default ships without `curl` but with [BusyBox](https://www.busybox.net/about.html), a
multi-call binary that contains `wget` with reduced number of options.

## Front-end modules

**Note**: Front-end modules are being migrated to use GitHub Actions Workflows. So for those, Jenkinsfile is not relevant.

## Further information

There are other options available to 'buildNPM', 'buildMvn', and 'buildJavaDocker' for certain
corner cases. Please ask for assistance.

<div class="folio-spacer-content"></div>

