---
layout: page
title: Running a local FOLIO system
permalink: /guides/run-local-folio/
menuInclude: no
menuTopTitle: Guides
---

This document introduces various ways to enable developers to run a complete FOLIO system to assist their local daily development.

## Introduction

There are various ways to run a local FOLIO system. Each technique might be relevant at different times.

A complete system includes the Okapi gateway, the main back-end modules (especially the auth and user-related modules),
sample data for tenants and users and items, and the Stripes UI development server configured for various client-side modules.

Some of the regularly updated [Prebuilt Vagrant boxes](#prebuilt-vagrant-boxes) do provide a complete system to download as a virtual machine.
It is also possible to utilise a box in conjunction with local development versions of the relevant parts.

## Prebuilt Vagrant boxes

See the [explanations](https://github.com/folio-org/folio-ansible/blob/master/doc/index.md) for each of the available boxes.
The main ones of interest at this stage are: folio/testing-backend, folio/testing, and folio/snapshot
(and the upcoming release to replace the old "stable" boxes).

The guide to [Software Build Pipeline](/guides/automation/#software-build-pipeline) further explains the process, what time of day each is built, and links to the public interfaces.

The [Primer for front-end development](/start/primer-develop-frontend/) leads to some guides for establishing a front-end developer's environment.

## Deploy via local Okapi and Stripes

Another way is to run difrectly on the host machine.

Follow the Guide to [start](https://github.com/folio-org/okapi/blob/master/doc/guide.md#running-okapi-itself)
Okapi in its clean state.

Develop a [suite](#sending-queries) of 'curl' commands to create a test tenant and then deploy the main initial backend modules and your own additional modules.
Generate and load user sample data.

For guidance follow some other developers and their local deployment facilities:
Okapi's [doc/okapi-examples.sh](https://github.com/folio-org/okapi/blob/master/doc/okapi-examples.sh) script and Guide;
the [mod-notes](https://github.com/folio-org/mod-notes) run.sh script;
the [mod-inventory running](https://github.com/folio-org/mod-inventory#running) scripts;
the script provided in [Lesson-06 Interact with the FOLIO Stable VM](/tutorials/curriculum/06-vm-stable/);
the [folio-ansible](https://github.com/folio-org/folio-ansible/) roles and tasks;
the [folio-test-env](https://github.com/folio-org/folio-test-env).
Although these other documents are intended for a production installation, they do have useful parts which assist with running a local system:
[FOLIO deployment: single server](https://github.com/folio-org/folio-install/blob/master/single-server.md) and [Securing Okapi Installation](https://github.com/folio-org/okapi/blob/master/doc/securing.md).

Follow the [Stripes: quick start](https://github.com/folio-org/stripes-core/blob/master/doc/quick-start.md) for the Stripes UI development server.
As explained there, the default will use released modules. It can be configured to use your local development versions.

## Available module versions

Send a command via the gateway:

```
curl -w '\n' http://localhost:9130/_/discovery/modules
```

or using the web interface, go to "Settings : Software versions".

## Sending queries

No matter which technique for setting up a running system, developers will need to send queries and conduct various test operations.

The resources linked via the "[local Okapi](#deploy-via-local-okapi-and-stripes)" section above will provide some guidance.

Some important points: specify the Tenant in the queries, and obtain the X-Okapi-Token header and save it for later use in the script session.

See also the [okapi-cli](https://github.com/folio-org/okapi-cli) and
the [stripes-cli](https://github.com/folio-org/stripes-cli).

## Ansible

Follow [folio-ansible](https://github.com/folio-org/folio-ansible) as a model for your own setup, and expand it to also deploy your modules and data.
