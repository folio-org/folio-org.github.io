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
(See [Tutorials : Using a FOLIO virtual machine](/tutorials/folio-vm/).)
It is also possible to utilise a box in conjunction with local development versions of the relevant parts
(refer to [Running backend modules on your host system](https://github.com/folio-org/folio-ansible/blob/master/doc/index.md#running-backend-modules-on-your-host-system)).

## Prebuilt Vagrant boxes

See the [explanations](https://github.com/folio-org/folio-ansible/blob/master/doc/index.md) for each of the available boxes.
The main ones of interest at this stage are: folio/snapshot, and folio/release

The guide to [Software Build Pipeline](/guides/automation/#software-build-pipeline) further explains the process, what time of day each is built, and links to the public interfaces.

The [Primer for front-end development](/start/primer-develop-frontend/) leads to some guides for establishing a front-end developer's environment.

## Local module as Docker container

Testing a back-end module as a Docker container using a Vagrant VM.
This might be a useful technique for testing memory management and other settings for a containerized back-end module.
Also in preparation to [add to reference environments](/guides/install-backend-module/#ensure-recent-local-vm).

* Bring up a FOLIO Vagrant VM (e.g. 'folio/snapshot' or 'folio/release') as normal with `vagrant up` and log in with `vagrant ssh`

* Clone the module repository and build the backend module:

```
git clone --recursive https://github.com/folio-org/mod-marccat
cd mod-marccat
mvn clean install
```

* Build the Docker image from the repository's Dockerfile:

```
sudo docker build -t mod-marccat .
```

* Edit the module descriptor in the module's `target` directory. In the `launchDescriptor` object, change the `dockerImage` key to reflect the name of the container built in the previous step (in this example: `"mod-marccat"`).
Make any other changes you want to test to the container or environment settings.
Note that in the Vagrant VMs, database connection settings are overridden by system settings.

* Post the updated module descriptor to Okapi:

```
curl -w '\n' -D - -X POST -d @target/ModuleDescriptor.json http://localhost:9130/_/proxy/modules
```

* Deploy the module and enable it for the tenant, using the module ID in the module descriptor (in this example: `mod-marccat-2.2.5-SNAPSHOT`).
Note that for this example, all of the module's requirements are already satisfied by the installed FOLIO system in the VM.
You may need to check the module's [dependency graph](/tutorials/folio-vm/04-local-development/#module-dependency-graph) first.

```
curl -w '\n' -D - -X POST \
  -d '[{"id": "mod-marccat-2.2.5-SNAPSHOT", "action": "enable"}]' \
  "http://localhost:9130/_/proxy/tenants/diku/install?deploy=true&tenantParameters=loadReference%3dtrue%2cloadSample%3dtrue"
```

The module should now be up and running for your tenant in a container.
If there are issues, check the Okapi log at `/var/log/folio/okapi/okapi.log`
or check the [container module log](https://github.com/folio-org/folio-ansible/blob/master/doc/index.md#viewing-backend-module-logs) itself using `docker logs`.

## Scratch environments, Rancher, Docker

Each development team can utilise their specific "scratch environment".
This enables a developer to use local git clones of backend repositories, building and publishing Docker images, then using their team's scratch environment via Rancher to manage Kubernetes (K8s) to interact with a complete FOLIO system.

Refer to the FAQ [How to get started with Rancher environment](/faqs/how-to-get-started-with-rancher/).

As explained, each FOLIO team has their own scratch environment.
For example, the Core Functional team Wiki [article](https://wiki.folio.org/display/FOLIJET/Back-end+module+development+using+the+scratch+environment+and+Rancher) guides their team.
Their instructions would generally apply to other teams.

## Deploy via local Okapi and Stripes

Another way is to run directly on the host machine.

Follow the Guide to [start](https://github.com/folio-org/okapi/blob/master/doc/guide.md#running-okapi-itself)
Okapi in its clean state.

Use [folio-local-run](https://github.com/adamdickmeiss/folio-local-run) which enables debugging and testing new functionality, and verifying integration with other modules.
Builds the set of modules from source.
Explains installing and configuring the requirements PostgreSQL, Elasticsearch, Apache Kafka, Apache ZooKeeper.

The [folio-tools/infrastructure/local](https://github.com/folio-org/folio-tools/tree/master/infrastructure/local) is another way to install those requirements, using Docker Compose.

Develop a [suite](#sending-queries) of 'curl' commands to create a test tenant and then deploy the main initial backend modules and your own additional modules.
Generate and load user sample data.

For guidance follow some other developers and their local deployment facilities:
Okapi's [doc/okapi-examples.sh](https://github.com/folio-org/okapi/blob/master/doc/okapi-examples.sh) script and Guide;
the [mod-notes](https://github.com/folio-org/mod-notes) run.sh script;
the [mod-inventory running](https://github.com/folio-org/mod-inventory#running) scripts;
the scripts provided in [Tutorials : Using a FOLIO virtual machine](/tutorials/folio-vm/);
the [folio-ansible](https://github.com/folio-org/folio-ansible/) roles and tasks;
the [folio-test-env](https://github.com/folio-org/folio-test-env).
Although these other documents are intended for other purposes, they do have useful parts which assist with running a local system:
[FOLIO deployment: single server](https://docs.folio.org/docs/getting-started/installation/) and [Securing Okapi Installation](https://github.com/folio-org/okapi/blob/master/doc/securing.md).

Follow the [Stripes: quick start](https://github.com/folio-org/stripes/blob/master/doc/quick-start.md) for the Stripes UI development server.
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
