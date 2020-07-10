---
layout: page
title: How to get started with Rancher environment
titleLeader: "FAQ |"
menuTopTitle: Guides
categories: development-tips
faqOrder: 9
---

## Introduction
Rancher is a Kubernetes management tool.

* FOLIO rancher main URL: [https://rancher.dev.folio.org](https://rancher.dev.folio.org)
* Project UI URL: `https://<Project name>.ci.folio.org`
* Basic Okapi URL: `https://<Project name>-okapi.ci.folio.org`

## Logging in
To have access to Rancher, you need to be a member of a FOLIO organization Team in GitHub. Check [here Gitgub Folio teams](https://github.com/orgs/folio-org/teams).
Go to the main Rancher URL and login with GitHub account.
Select the default Cluster and your Project.
Default cluster name is `folio-eks-2-us-west-2`.

## Project description
Every project has its own Postgres, Okapi, pre-installed core backend modules and [Stripes UI](https://github.com/folio-org/platform-complete). All these containers runs in own default namespace named same as Project name.
Also every Project runs Prometheus and Kafka.
FOLIO modules are installed from the [FOLIO Helm repository](https://github.com/folio-org/folio-helm).
Postgres and Kafka are installed from the Bitnami Helm repository.

## Running modules
All Project have installed Folio Helm repository (`Catalog` in Rancher) witch contains all backend modules.
By default the backend modules are pulled from [DockerHub/folioci](https://hub.docker.com/u/folioci) repository with a 'latest' tag.
All modules can be managed in `App` menu in Rancher. You can add new module or upgrade one there.

## Building own backend modules
You can build your own module and automatically deploy it with Rancher pipeline and Helm.
Please create you own branch and modify `.rancher-pipeline.yml` to your needs [as in this pipeline](https://github.com/folio-org/mod-pubsub/blob/master/.rancher-pipeline.yml) to get started. Go to Workloads -> Pipelines, run pipeline for that branch and Rancher will deploy new version of that module.
Recomendations about min. requirements to pipeline namespace to pass successful build:
  * Limit mCPU - 4500
  * Limit memory - 5000 Mb
Note! Stripes UI module is installed by default and cannot be built inside Rancher pipeline.

## Registering modules in Okapi
Module registration runs automatically after the install or upgrade procedure.
Helm uses post-install and post-upgrade hooks to run module registration job for each module.
Helm gets ModuleDescriptors from the [FOLIO Registry](http://folio-registry.aws.indexdata.com) - it gets the latest master branch snapshot descriptor.

Default steps for module registration:
  * Pushing module descriptor
  * Pushing module deployment
  * Creating tenant (default 'diku')
  * Enabling module for tenant

Also you can use docker commands to do registration manually:
  * Registering particular module (backend or UI module)
    `docker run --rm -e TENANT_ID=diku -e OKAPI_URL=https://<project name>-okapi.ci.folio.org -e MODULE_NAME=<module name> docker.dev.folio.org/folio-okapi-registration`
  * Registering all modules (backend and UI from 'platform-complete' list)
    `docker run --rm -e TENANT_ID=diku -e OKAPI_URL=https://<project name>-okapi.ci.folio.org -e MODULE_NAME='' docker.dev.folio.org/folio-okapi-registration`
    * Registering all UI modules only
      `docker run --rm -e TENANT_ID=diku -e OKAPI_URL=https://<project name>-okapi.ci.folio.org -e MODULE_NAME='deployStripes' docker.dev.folio.org/folio-okapi-registration`

## Setting up modules permissions
Last step after modules registration is to apply perrmissions to modules to admin user.

  * Applying permissions to all installed modules to `diku_admin`
    `docker run --rm -e TENANT_ID=diku -e ADMIN_USER=diku_admin -e ADMIN_PASSWORD=admin -e OKAPI_URL=https://<project name>-okapi.ci.folio.org docker.dev.folio.org/bootstrap-superuser`

## Environment variables
Environment variables for database and backend modules are stored in Kubernetes secrets (Workload -> Secrets) and installed by default to every Project.

## Limitations
No Okapi securing is provided.
Build Stripes UI module in Rancher is not possible due to Project resource limits.

<div class="folio-spacer-content"></div>
