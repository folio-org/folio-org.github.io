---
layout: page
title: Install a new back-end module to reference environments
permalink: /guides/install-backend-module/
menuInclude: no
menuTopTitle: Guides
---

## Introduction

When the initial development of a new back-end (server-side) module (or an edge module) is [established](/guidelines/create-new-repo/), and snapshot artifacts are being reliably generated by the continuous integration, then it is able to be added to the folio-snapshot [reference environments](/guides/automation/#reference-environments).

There is a separate procedure to [install a new front-end module](/guides/install-frontend-module/).

(After the new module has been operating in snapshot reference environments, and a release is ready to be made, then instead follow the [release procedures](/guidelines/release-procedures/#add-to-platforms).)

## Avoid typical mistakes

Before proceeding, ensure that the backend module does not make some of the typical mistakes that cause disruption.

Note that this is not an exhaustive list.

* The module version number (e.g. in Maven POM) is a semantic version number and snapshot designator, i.e. in mainline branch it should be `x.y.z-SNAPSHOT`. Avoid common mistakes like `x.y-SNAPSHOT` or `x.y.z` with no appended `-SNAPSHOT`.
* If a release has been made prior to adding to the reference environments, then ensure that the [release procedures](/guidelines/release-procedures/) were correctly followed (e.g. the version in POM must have been subseqently incremented so that the semantic minor version is greater than the release version).
* The port numbers are matching -- the same in ModuleDescriptor, Dockerfile, and in program code and configuration.
* For Spring Way modules, the default port is 8080. FOLIO does not care which port. However if the module is going to use a different port, then be sure to also declare that `server.port` in its `application.yaml` file.
* For Spring Way modules, the replacement tokens in Descriptors use delimiters "@" rather than the normal "$".
* Ensure that the ModuleDescriptor is generated from its template and that tokens are replaced. For Maven-based modules, the POM will have configuration to "filter-descriptor-inputs" and "rename-descriptor-outputs".
* If the module uses the `_tenant` interface, then ensure that it is implemented and responding properly.
* Other ...

## Verify MD and required interfaces

Ensure that this new module's [ModuleDescriptor](/guides/module-descriptor/) is deployed and that any required interfaces are available.

For example, consider the `mod-notes` module.
Obtain its MD from the registry and extract the "requires" section:

```
curl -s -S -w'\n' \
  'https://folio-registry.dev.folio.org/_/proxy/modules?filter=mod-notes&latest=1&full=true' \
  | jq '.[].requires'
```

That shows that it requires various interfaces, including "`users 15.1`" and "`configuration 2.0`".

Now ensure that each needed interface version is [available](/faqs/how-to-which-module-which-interface-endpoint/).

## Ensure LaunchDescriptor

Ensure that this new module's [ModuleDescriptor](/guides/module-descriptor/) includes the Docker-based [LaunchDescriptor](/guides/module-descriptor/#launchdescriptor-properties).

Its properties will specify the memory allocation, whether this module utilises a database, and can document other environment variables, etc.

## Ensure module health endpoint

The module must provide the [module health check](/guidelines/naming-conventions/#api-endpoints) endpoint to enable verification of the module deployment.

## Prepare special requirements

If there are special requirements beyond those declared in the default LaunchDescriptor, then document those in the module README.

Remember that there are other systems operators, as well as FOLIO DevOps, that need to know how to install the module.

Also, for Edge modules explain the endpoint pattern, permissions, and institutional users. See other edge module repositories for guidance.

Also prepare beforehand if there are special requirements for FOLIO infrastructure, additional to what is already provided.
Add Jira tickets (as described below) to completely explain the services that the new module requires.
Do not expect us to know.
Allow sufficient time to establish these.

## Ensure recent local VM

(Alternatively ensure that the module operates properly in a [Rancher scratch environment](/faqs/how-to-get-started-with-rancher/).)

Ensure that the module will operate with a **recent** local Vagrant VM.
<!-- Await platform-minimal FOLIO-3253
If the new module does not yet depend on others, then `folio/release-core` VM would be easiest.
-->

Follow the guide to verify [Deploy a module](/tutorials/folio-vm/04-local-development/#deploy-a-module).

That procedure will verify that the most recent published module is ready to be installed in the reference environments.

## Request add new module

Before proceeding, verify that the module is ready to be added, including the above-mentioned steps and the guidelines at [Create a new FOLIO module and do initial setup](/guidelines/create-new-repo/).

Prepare the Jira ticket to guide the process, and request that the new backend module be enabled for the snapshot reference environments.

If there are [special requirements](#prepare-special-requirements), then provide a link to that section of the module README.

[Raise a FOLIO DevOps Jira ticket](/faqs/how-to-raise-devops-ticket/#general-folio-devops).

**Note:** Plan for plenty of time for this phase. Our team will already have a full Sprint.
So it will likely be a subsequent Sprint.

The DevOps team will configure the module and conduct various configuration tests.

## Verify deployment

After merge, await the scheduled build of the folio-snapshot [reference environments](/guides/automation/#reference-environments).

Visit the [Software versions](https://folio-snapshot.dev.folio.org/settings/about) page of each to verify that the new module is present.

<div class="folio-spacer-content"></div>

