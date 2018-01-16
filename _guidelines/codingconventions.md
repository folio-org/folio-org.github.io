---
layout: guidelines
title: Coding Style
heading: Coding Style
permalink: /guidelines/codingconventions/
---

# Coding Conventions

## Style Guidelines and Configuration

Follow the coding style that is being used by each repository for each file type.

For JSON key names we use camelCase.

For Java code we basically try to adhere to Sun Java coding
[conventions](http://www.oracle.com/technetwork/java/codeconvtoc-136057.html)
(that document is old and unmaintained, but seems to be good enough as it is).

For JavaScript code we follow [ESLint](https://eslint.org), with some exceptions.

## Code analysis and linting

All code repositories have linter and code-style analysis facilities implemented as part of their continuous integration build process.
The process is explained, along with usage notes and configuration for running those tools locally.

All code repositories have linter and code-style analysis facilities implemented as part of their continuous integration. The pull requests will run the relevant static code analysis tools.

This document explains those facilities and shows how to run tools locally before pushing changes.

The client-side projects use "ESLint".
The server-side projects use "SonarQube".
Actually, the SonarQube [analysis](https://sonarcloud.io/organizations/folio-org/projects)
reports are available for all projects, and provide additional useful analysis.

### Preparing pull requests

The pull request will show the analysis messages of any new issues that arise from these code changes.

At this stage the contraventions will not prevent the merge to master.

Developers can minimise these reports by running the tools locally,
and in some cases configuring the code lines to avoid certain tests.

### SonarQube

[sonarcloud.io/organizations/folio-org](https://sonarcloud.io/organizations/folio-org/projects)

See [FOLIO-858](https://issues.folio.org/browse/FOLIO-858) to encourage 'A' ratings.

#### Local use

The [SonarLint](http://www.sonarlint.org) extension for IDEs will detect quality issues at an early stage.

Use "Connected mode" to hook directly into our project rules.

#### Rule customization

See an [example](https://github.com/folio-org/okapi/pull/367/commits/1710e99d574152cc67990d83d400951e8f11e309)
of using SuppressWarnings.

Regarding "Quality Profile" see issue [FOLIO-864](https://issues.folio.org/browse/FOLIO-864)

### ESLint for client-side projects

The [Code quality](https://github.com/folio-org/stripes-core/blob/master/doc/dev-guide.md#code-quality)
section of _The Stripes Module Developer's Guide_ explains ESLint usage, how to run it prior to commit, and how to disable some lines.

### Other lint tools: raml-cop, jq

These are not included in continuous integration, but are certainly useful as local tools.

For RAML-using server-side projects use [raml-cop](https://github.com/thebinarypenguin/raml-cop) to validate RAML/Schema and examples.

For JSON files, [jq](https://github.com/stedolan/jq) is useful for validation, pretty-printing and linting, and for many JSON processing and viewing tasks.

## Consistent whitespace

- We indent with two spaces only, because vert.x uses deeply nested callbacks.
- We _don't_ use tab characters for indents, only spaces.

For XML and JSON and RAML files, the same: two-space indent and no tabs.

Some projects do provide a `.editorconfig` file.
Remember to set your IDE and editors to remove trailing spaces on saving files,
since those produce unnecessary diffs in Git.
Refer to coding style [configuration](#style-guidelines-and-configuration) assistance.

## No license header

We do not use a license header in the top of each source code file.
Refer to the README and LICENSE file at the top of each repository.
See further [license](/guidelines/cla-process) information.
See [configuration](#no-license-header) assistance for IDEs.

## Testing

We aim to write a lot of tests -- each module should have at least some kind of
test associated with it. These can be traditional unit tests, black-box tests
that talk through the WSAPI, and/or proper integration tests.

When hunting down problems, it is considered good form to write a test that
demonstrates the problem first, then a fix that makes the test pass.

We have a Jenkins test system that gets invoked when you push something
to master, and/or make a pull request. It should flag any errors, but be
nice and run a ```mvn install``` on your own machine before every
```git commit```

## RAML

Remember to update these if you ever change anything in the API.
And update the documentation too, of course.

For Okapi, we keep the API specs in RAML files under `okapi-core/src/main/raml/`.

For [server-side modules](/source/components/#server-side-1),
the [raml](https://github.com/folio-org/raml)
repository is the master location for the traits and resource
types, while each module is the master for its own schemas, examples,
and actual RAML files.

## Best Practices for Docker Files

Since FOLIO modules can consist of range of application and programming environments,
running modules as Linux containers provides a nice way to avoid issues related to
the complexities of installing and managing a system with mixed environments.  Docker
is a popular container framework and has been adopted as a primary distribution
model for FOLIO modules.  Dockerfiles describe how to build and run an application in
a Docker container.

The following outlines some general best practices for adding Dockerfiles to
a FOLIO module project.   This is by no means a comprehensive list, and, as with
all best practices, there will always be exceptions as well as a bit of controversy
(indeed, it may be less controversial to re-title this document "FOLIO Dockerfile
tips").  This [best practice guide](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/)
from Docker also provides a good overview.

* All FOLIO modules should include one or more Dockerfiles called 'Dockerfile' that
will build and run a Docker container suitable for a runtime environment.  As a general
rule, images should be as lean and concise as possible and should not contain things
like SDKs, build dependencies, and development tools.  It is often desirable to include
a separate Dockerfile that will bootstrap a module from source to get something up and
running quickly for prototyping and development. This type of Dockerfile should be named
'Dockerfile.build' to differentiate it from the runtime Dockerfile.

* Most FOLIO Docker images will be derived from a pre-existing base image.  If possible,
use an existing base image from an "official repository" located on Docker Hub.
Examples include the following:

  - [OpenJDK for Java-based modules](https://hub.docker.com/_/openjdk)
  - [Node.js-based modules](https://hub.docker.com/_/node)
  - [Python-based modules](https://hub.docker.com/_/python)

  If it is necessary to start with an OS base image, the following are good choices:

  - [Debian OS base image](https://hub.docker.com/_/debian)
  - [Alpine OS base image](https://hub.docker.com/_/alpine)

  Alpine is ideal because of its small footprint. However, it may not be compatible
with all projects.  Test your Docker image to ensure your module functions correctly.

* Utilize the "one process per container" rule whenever possible and run the
process as PID 1 to ensure that the process responds properly to a SIGTERM sent by
'docker stop'.  Using the exec form of the CMD or ENTRYPOINT instruction will
typically accomplish this.

  ```
  CMD ["executable", "param1", "param2"]
  ENTRYPOINT ["executable", "param1", "param2"]

  ```

  This can become more complex depending on whether the process started in the container
is actually coded to exit gracefully when receiving a SIGTERM. If a different signal
should be used to gracefully stop a container process, i.e. SIGQUIT or something else,
it should be noted somewhere in the module documentation.

* If it is necessary to run more than one process in your container,  use 'supervisord'
to manage your processes. Supervisor should be run as PID 1 in this case.
See [Using Supervisor](https://docs.docker.com/engine/admin/using_supervisord/) for
additional information.

* It is often necessary to pass optional arguments to a module running inside a
container.  For example,  the FOLIO  mod-circulation module can take an optional
argument to run an embedded MongoDB data store (generally NOT a good idea for a production
module!).

  ```
  docker run -d mod-circulation embed_mongo=true

  ```

  One way to accomplish this is to exec the module using ENTRYPOINT
and include CMD with an empty array. For example:

  ```
  ENTRYPOINT ["java", "-jar", "circulation-fat.jar"]
  CMD []

  ```

* With Java-based modules, it is often necessary to pass options to Java
  (as opposed to the application) at runtime.   The exec forms of ENTRYPOINT
  and CMD in the previous example, however, do not support variable substitution.
  A method to accomplish this is to use the shell form of ENTRYPOINT instead.

  ```
  ENTRYPOINT exec java $JAVA_OPTS circulation-fat.jar

  ```

  Now run the container by passing in JAVA_OPTS as an environment
  variable:

  ```
  docker run -d -e JAVA_OPTS='-Xmx1g -Xms1g' mod-circulation

  ```

  Unfortunately, mixing the shell form of ENTRYPOINT with the exec form of CMD
  is not possible, so combining support for application options as outlined
  in the previous example with support for Java options becomes much more
  difficult.  At this point, it's probably time to start thinking about a proper
  ENTRYPOINT script.

* Limit the number of RUN steps in your Dockerfile by chaining together commands with
  '&&' when possible.

* Run the container process as a non-root user by utilizing 'USER' in your Dockerfile.
Note, it is necessary to ensure that the user exists or is created in the container image
in order for USER to work.

  ```
  # Create user/group 'folio'
  RUN groupadd folio && \
      useradd -r -d $VERTICLE_HOME -g folio -M folio && \
      chown -R folio.folio $VERTICLE_HOME

  # Run as this user
  USER folio

  ```

* The module running inside the container should log to STDOUT by default - not to a log
file inside the container.  By logging to STDOUT,  the developer can easily look at
module logs when debugging and the Docker administrator can choose to redirect the logs
elsewhere according to their own site preferences.



