---
layout: page
title: ModuleDescriptor
permalink: /guides/module-descriptor/
menuInclude: no
menuTopTitle: Guides
---

## Introduction

This guide provides an overview of the ModuleDescriptor.

The ModuleDescriptor (MD) is introduced in the Okapi Guide
(e.g. [here](https://github.com/folio-org/okapi/blob/master/doc/guide.md#what-are-modules)
and [here](https://github.com/folio-org/okapi/blob/master/doc/guide.md#example-4-complete-moduledescriptor)).

The MD adheres to the [ModuleDescriptor.json](https://github.com/folio-org/okapi/blob/master/okapi-core/src/main/raml/ModuleDescriptor.json) schema.

## Maintenance

### Back-end modules

For back-end modules, a template is [maintained](/guides/commence-a-module/#back-end-descriptors).
This is usually at `./descriptors/ModuleDescriptor-template.json` and is transformed by the module's build process into the `target/ModuleDescriptor.json` file.
See example at [mod-notes](https://github.com/folio-org/mod-notes/blob/master/descriptors/ModuleDescriptor-template.json).

To validate changes, utilise a JSON Schema validator such as [z-schema](https://github.com/zaggino/z-schema):

```
cd mod-notes
jq '.' descriptors/ModuleDescriptor-template.json
z-schema --pedanticCheck \
  ../okapi/okapi-core/src/main/raml/ModuleDescriptor.json \
  ./descriptors/ModuleDescriptor-template.json
```

### Front-end modules

For front-end UI modules, the `ModuleDescriptor.json` is generated from various information
that is [maintained](/guides/commence-a-module/#frontend-end-descriptors) in the `package.json` file.
See example at [ui-users](https://github.com/folio-org/ui-users/blob/master/package.json).

To validate changes, first use [stripes-cli](https://github.com/folio-org/stripes-cli/blob/master/doc/user-guide.md) to generate the MD.
Then utilise a JSON Schema validator such as [z-schema](https://github.com/zaggino/z-schema):

```
cd ui-users
jq '.' package.json
stripes mod descriptor --full --output /tmp
z-schema --pedanticCheck \
  ../okapi/okapi-core/src/main/raml/ModuleDescriptor.json \
  /tmp/users.json
```

## Registry

As part of the continuous integration process, each ModuleDescriptor.json is published to the FOLIO Registry at `https://folio-registry.aws.indexdata.com/`

## ModuleDescriptor properties

### Introduction {#md-introduction}

Refer to the general [introduction](#introduction) above.

### General MD properties

Each main property is briefly described in the
[ModuleDescriptor.json](https://github.com/folio-org/okapi/blob/master/okapi-core/src/main/raml/ModuleDescriptor.json) schema.

The following sub-sections explain some properties in more detail ...

```
TODO: Provide brief explanations of some sections.
```

### metadata

The "metadata" section enables some additional descriptive items.
The MD schema enables any JSON object.

## LaunchDescriptor properties

### Introduction {#ld-introduction}

The LaunchDescriptor (LD) is introduced in the Okapi Guide
(e.g. at sections [Deployment and Discovery](https://github.com/folio-org/okapi/blob/master/doc/guide.md#deployment-and-discovery)
and [Deployment](https://github.com/folio-org/okapi/blob/master/doc/guide.md#deployment)
and [Auto-deployment](https://github.com/folio-org/okapi/blob/master/doc/guide.md#auto-deployment)).

The LD adheres to the [LaunchDescriptor.json](https://github.com/folio-org/okapi/blob/master/okapi-core/src/main/raml/LaunchDescriptor.json) schema.

As explained in the Okapi Guide, the LaunchDescriptor can be a separate descriptor, or be part of the ModuleDescriptor.
The LaunchDescriptor can utilise various methods for [deployment](https://github.com/folio-org/okapi/blob/master/doc/guide.md#deployment).

### Default LD Docker properties

For the suite of [back-end modules](/source-code/#server-side) that are hosted in the folio-org GitHub organization, each one has a LaunchDescriptor for Docker, and the LD is included in the module's ModuleDescriptor file.

For a back-end module to [be included](/guides/install-backend-module/) in the reference environments, it must have such a LaunchDescriptor.

This enables ready default deployment.
Each module's LD settings are used directly in the FOLIO [reference environments](/guides/automation/#reference-environments).
Note that those installations have a small amount of data and low activity load.
Other installations would probably adjust or replace these LDs.

<div class="attention">
The "env" section of the "launchDescriptor" properties contains an enumeration of variables (such as DB_USERNAME and JAVA_OPTIONS) and sample values.
It is considered best practice to override these values in the Launch Descriptors created for production environments.
</div>

### General LD properties

Each main property is briefly described in the
[LaunchDescriptor.json](https://github.com/folio-org/okapi/blob/master/okapi-core/src/main/raml/LaunchDescriptor.json) schema.

The following sub-sections explain some properties in more detail.

Refer to the [example](#example-launchdescriptors) below.

### dockerCMD

Optional. Over-ride the CMD of Dockerfile. An array of string items.

Example LDs that use this:
[mod-login](https://github.com/folio-org/mod-login/blob/master/descriptors/ModuleDescriptor-template.json)

### Memory

Limit each container's memory usage.

All LDs must have the memory setting.

The setting must be expressed as bytes.

Take care to have the correct number of digits, typically nine.

As noted above, this memory level is appropriate for running a basic system such as the "folio-snapshot-load" reference environment and the Vagrant VMs. So this default container memory setting should be as low as possible.

NOTE: 20191118:
Module developers: please determine the lowest possible container memory allocation, and adjust your setting (see [FOLIO-2315](https://issues.folio.org/browse/FOLIO-2315)).

With the new directions for LaunchDescriptors and Dockerfiles
(see [FOLIO-2358](https://issues.folio.org/browse/FOLIO-2358)),
and as shown in the [example](#example-launchdescriptors) below,
two-thirds of the memory allocation will be reserved for heap space.

### HostPort binding

Okapi will map the "%p" value to the relevant port for this container.

### env {#docker-env}

The default environment for deployment.

This is an array of items, each with properties: name (required), value, description.

All LDs for Java-based modules must have the base [`JAVA_OPTIONS`](#env-java_options) setting.

If the module uses a database, then it must provide the standard set of `DB_` [database settings](#env-db-environment) shown in the example.

Other environment variables can also be documented here (see [examples](#example-launchdescriptors)).
Their default values would need to make sense in the FOLIO [reference environments](/guides/automation/#reference-environments) where these LaunchDescriptors will be used as-is.
The defaults also need to make sense in a cluster.

### env JAVA_OPTIONS

This environment variable must at least have the setting as shown in the [example](#example-launchdescriptors), which enables Java to configure the specified [memory](#memory) for the container.

<a id="dockerfile"></a>The module's Dockerfile needs to use a base image that has the feature "UseContainerSupport" -- which was backported to Java 8 (8u191+). Use that in conjunction with "MaxRAMPercentage".

Use the [folioci/alpine-jre-openjdk8:latest](https://hub.docker.com/r/folioci/alpine-jre-openjdk8/tags)

NOTE: 20191118:
This is now being applied to all modules. See [FOLIO-2358](https://issues.folio.org/browse/FOLIO-2358).

Other necessary options can be appended (e.g. -XX:+PrintFlagsFinal).

See one [explanation](https://stackoverflow.com/questions/53451103/java-using-much-more-memory-than-heap-size-or-size-correctly-docker-memory-limi/53624438#53624438) of Java memory footprint, monitoring, and profiling.

Also [note](https://medium.com/adorsys/usecontainersupport-to-the-rescue-e77d6cfea712) that
"setting -Xmx and -Xms disables the automatic heap sizing".

### env DB environment

If the module uses a database, then it must provide the standard set of `DB_` settings shown in the [example](#example-launchdescriptors).

Some need explanation:
* `DB_HOST` keyword "postgres" is automatically mapped by the relevant system.
* `DB_DATABASE` is "okapi_modules" used by all modules.


### Example LaunchDescriptors

The following example is for
[mod-notes](https://github.com/folio-org/mod-notes/blob/master/descriptors/ModuleDescriptor-template.json)
which does use a database.

As explained [above](#env-java_options), this form needs the new folio docker image.

```json
  "launchDescriptor": {
    "dockerImage": "${artifactId}:${version}",
    "dockerPull": false,
    "dockerArgs": {
      "HostConfig": {
        "Memory": 357913941,
        "PortBindings": { "8081/tcp": [ { "HostPort": "%p" } ] }
      }
    },
    "env": [
      { "name": "JAVA_OPTIONS",
        "value": "-XX:MaxRAMPercentage=66.0"
      },
      { "name": "DB_HOST", "value": "postgres" },
      { "name": "DB_PORT", "value": "5432" },
      { "name": "DB_USERNAME", "value": "folio_admin" },
      { "name": "DB_PASSWORD", "value": "folio_admin" },
      { "name": "DB_DATABASE", "value": "okapi_modules" },
      { "name": "DB_QUERYTIMEOUT", "value": "60000" },
      { "name": "DB_CHARSET", "value": "UTF-8" },
      { "name": "DB_MAXPOOLSIZE", "value": "5" }
    ]
  }
```

Other examples:

* [mod-circulation](https://github.com/folio-org/mod-circulation/blob/master/descriptors/ModuleDescriptor-template.json)
  -- does not use a database.
* [mod-users](https://github.com/folio-org/mod-users/blob/master/descriptors/ModuleDescriptor-template.json)
  -- has greater memory allocation.
* [mod-login](https://github.com/folio-org/mod-login/blob/master/descriptors/ModuleDescriptor-template.json)
  -- uses the dockerCMD.

## Testing the modifications

Use [jq](https://stedolan.github.io/jq/):

```
jq '.' descriptors/ModuleDescriptor-template.json
```
Use [z-schema](https://github.com/zaggino/z-schema):

```
z-schema --pedanticCheck \
  ../okapi/okapi-core/src/main/raml/ModuleDescriptor.json \
  descriptors/ModuleDescriptor-template.json
```

Deploy the module as a Docker container with a local FOLIO Vagrant VM (e.g. folio/testing).
See [instructions](/guides/run-local-folio/#local-module-as-docker-container).

Inspect the container, and gather some crude statistics:

```
vagrant ssh
sudo docker ps  # and find your container ID
sudo docker stats [CONTAINER...]
sudo docker exec -it CONTAINER bash
pmap -x 1
```

See other monitoring notes [above](#env-java_options).
