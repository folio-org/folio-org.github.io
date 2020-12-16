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
[back-end](#back-end-modules) and [front-end](#front-end-modules) modules.

Each parameter can be omitted to accept the default.

The values are: `true` or `false` (or the old syntax `'yes'` or `'no'`).

## Back-end modules

A typical Maven-based, server-side FOLIO module Jenkinsfile configuration might look like
the following.
See an example at
[mod-notes/Jenkinsfile](https://github.com/folio-org/mod-notes/blob/master/Jenkinsfile)

```
buildMvn {
  publishModDescriptor = true
  mvnDeploy = true
  publishAPI = true
  runLintRamlCop = true // Deprecated. See doApiLint.
  buildNode = 'jenkins-agent-java11'

  doApiLint = true
  apiTypes = 'RAML'
  apiDirectories = 'ramls'

  doDocker = {
    buildJavaDocker {
      publishMaster = true
      healthChk = true
      healthChkCmd = 'curl -sS --fail -o /dev/null http://localhost:8081/apidocs/ || exit 1'
    }
  }
}
```

* `publishModDescriptor` -- Maven-based modules will generate the ModuleDescriptor.json file as
[explained](/guides/commence-a-module/#back-end-descriptors).
It will be published to the FOLIO Module Descriptor registry.
(Default: false)

* `mvnDeploy` -- Deploy Maven artifacts to FOLIO Maven repository.
(Default: false)

* `publishAPI` -- Generate and publish [API documentation](/reference/api/) from the module's
[RAML](/guides/commence-a-module/#back-end-ramls) and Schema files.
(Default: false)

* `runLintRamlCop` -- Run "[raml-cop](/guides/raml-cop/)" (and other tests) on back-end modules that have declared [RAML](/guides/commence-a-module/#back-end-ramls) in api.yml configuration.
Also assists with [Describe schema and properties](/guides/describe-schema/).
(Default: false)
(Deprecated. See doApiLint.)

* `doApiLint` -- Run "[api-lint](/guides/api-lint/)" to assess API descriptions, schema, and examples -- both [RAML](/guides/commence-a-module/#back-end-ramls) and OpenAPI (OAS).
See [explanation](/guides/api-lint/#usage) of required and optional parameters.
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
health of the application running inside the container.

## Front-end modules

A typical Stripes or UI module Jenkinsfile configuration might look like the following.
See two examples at
[ui-users/Jenkinsfile](https://github.com/folio-org/ui-users/blob/master/Jenkinsfile)
and
[stripes-components/Jenkinsfile](https://github.com/folio-org/stripes-components/blob/master/Jenkinsfile)

```
buildNPM {
  publishModDescriptor = true
  runLint = true
  runTest = true
  runTestOptions = '--karma.singleRun --karma.browsers=ChromeDocker'
  runRegression = 'partial'
}
```

* `publishModDescriptor` -- If a FOLIO Module Descriptor is defined in its [package.json](/guides/commence-a-module/#front-end-packagejson)
then the ModuleDescriptor.json will be generated and published to the FOLIO Module Descriptor registry.
(Default: false)

* `runLint` -- Execute 'yarn lint' as part of the build.  Ensure a 'lint' run script is
defined in package.json before enabling this option.
(Default: false)

* `runTest` -- Execute 'yarn test' as part of the build.  Ensure a 'test' run script is
defined in package.json.  'test' is typically used for unit tests.
(Default: false)

* `runTestOptions` -- Provide 'yarn test' with additional options.
The example shows options for karma-based testing.

* `runRegression` -- Execute the UI regression test suite from 'ui-testing' against a real
FOLIO backend. Option 'full' will execute the full test suite. Option 'partial' will execute only tests
specific to the UI module. Option 'none' will disable regression testing.
(Default: 'none')

* `stripesPlatform` -- Specify which Stripes platform.
(Default: 'none', so build in "app" context.)

## Further information

There are other options available to 'buildNPM', 'buildMvn', and 'buildJavaDocker' for certain
corner cases. Please ask for assistance.

