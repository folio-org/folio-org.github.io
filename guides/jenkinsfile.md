---
layout: page
title: Jenkinsfile to configure continuous integration steps
permalink: /guides/jenkinsfile/
menuInclude: no
menuTopTitle: Guides
---

Each project's git repository [structure](/guides/commence-a-module/) has a top-level file called `Jenkinsfile`
which is utilized by the continuous integration [process](/guides/automation/#jenkins)
to enable each project to specify certain additional build steps.

The library primarily supports two types
of development environments at this time -- Java-based Maven projects and Nodejs-based projects.

The files and main parameters are explained below for
[back-end](#back-end-modules) and [front-end](#front-end-modules) modules.
Each parameter can be omitted to accept the default.

# Back-end modules

A typical Maven-based, server-side FOLIO module Jenkinsfile configuration might look like
the following.
See an example at
[mod-notes/Jenkinsfile](https://github.com/folio-org/mod-notes/blob/master/Jenkinsfile)

```
buildMvn {
  publishModDescriptor = 'yes'
  mvnDeploy = 'yes'
  publishAPI = 'yes'
  runLintRamlCop = 'yes'

  doDocker = {
    buildJavaDocker {
      publishMaster = 'yes'
      healthChk = 'yes'
      healthChkCmd = 'curl -sS --fail -o /dev/null http://localhost:8081/apidocs/ || exit 1'
    }
  }
}
```

* `publishModDescriptor` -- Maven-based modules will generate the ModuleDescriptor.json file as
[explained](/guides/commence-a-module/#back-end-descriptors).
It will be published to the FOLIO Module Descriptor registry.
(Default: 'no')

* `mvnDeploy` -- Deploy Maven artifacts to FOLIO Maven repository.
(Default: 'no')

* `publishAPI` -- Generate and publish [API documentation](/reference/api/) from the module's
[RAML](/guides/commence-a-module/#back-end-ramls) and Schema files.
(Default: 'no')

* `runLintRamlCop` -- Run "[raml-cop](/guides/raml-cop/)" (and other tests) on back-end modules that have declared [RAML](/guides/commence-a-module/#back-end-ramls) in api.yml configuration.
Also assists with [Describe schema and properties](/guides/describe-schema/).
(Default: 'no')

If we are creating and deploying a Docker image as part of the module's artifacts, specify
'doDocker' with 'buildJavaDocker' and the following options:

* `publishMaster` -- Publish image to 'folioci' Docker repository on Docker Hub when building
'master' branch.
(Default: 'yes')

* `healthChk` -- Perform a container healthcheck during build.  See 'healthChkCmd'.
(Default: 'no')

* `healthChkCmd` -- Use the specified command to perform container health check.   The
command is run *inside* the container and typically tests a REST endpoint to determine the
health of the application running inside the container.

# Front-end modules

A typical Stripes or UI module Jenkinsfile configuration might look like the following.
See two examples at
[ui-users/Jenkinsfile](https://github.com/folio-org/ui-users/blob/master/Jenkinsfile)
and
[stripes-components/Jenkinsfile](https://github.com/folio-org/stripes-components/blob/master/Jenkinsfile)

```
buildNPM {
  publishModDescriptor = 'yes'
  runLint = 'yes'
  runTest = 'yes'
  runTestOptions = '--karma.singleRun --karma.browsers=ChromeDocker'
  runRegression = 'partial'
}
```

* `publishModDescriptor` -- If a FOLIO Module Descriptor is defined in its [package.json](/guides/commence-a-module/#front-end-packagejson)
then the ModuleDescriptor.json will be generated and published to the FOLIO Module Descriptor registry.
(Default: 'no')

* `runLint` -- Execute 'yarn lint' as part of the build.  Ensure a 'lint' run script is
defined in package.json before enabling this option.
(Default: 'no')

* `runTest` -- Execute 'yarn test' as part of the build.  Ensure a 'test' run script is
defined in package.json.  'test' is typically used for unit tests.
(Default: 'no')

* `runTestOptions` -- Provide 'yarn test' with additional options.
The example shows options for karma-based testing.

* `runRegression` -- Execute the UI regression test suite from 'ui-testing' against a real
FOLIO backend. Option 'full' will execute the full test suite. Option 'partial' will execute only tests
specific to the UI module. Option 'none' will disable regression testing.
(Default: 'none')

* `stripesPlatform` -- Specify which Stripes platform.
(Default: 'none', so build in "app" context.)

# Further information

There are other options available to 'buildNPM', 'buildMvn', and 'buildJavaDocker' for certain
corner cases. Please ask for assistance.

