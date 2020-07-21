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
* PgAdmin4 URL: `https://<Project name>-pgadmin.ci.folio.org` (login as user 'chart@example.local' or 'user@folio.org' password 'SuperSecret')
* Logs: https://logs.ci.folio.org/

## Logging in
To have access to Rancher, you need to be a member of a FOLIO organization [Team in GitHub](https://github.com/orgs/folio-org/teams).
Go to the main Rancher URL and login with GitHub account.

Select the default Cluster and your Project.
Default cluster name is `folio-eks-2-us-west-2`.

## Project description
Every project has its own Postgres, Okapi, pre-installed core backend modules, and [Stripes Platform](https://github.com/folio-org/platform-complete). All of these containers run in the default namespace (which is named the same as the Project name).
Also every Project runs Prometheus and Kafka.
FOLIO modules are installed from the [FOLIO Helm repository](https://github.com/folio-org/folio-helm).
Postgres and Kafka are installed from the Bitnami Helm repository.

## Running modules
All Projects installed FOLIO Helm repository (`Catalog` in Rancher) which contains all backend modules, UI, pgadmin.
By default the backend modules are pulled from [DockerHub/folioci](https://hub.docker.com/u/folioci) repository with a 'latest' tag.
UI module is pulled from `docker.dev.folio.org` repository with own project latest tag `<project>-latest`.
All modules can be managed in the `App` menu in Rancher, where new modules can be added or existing ones can be upgraded.

## Building Backend modules
You can build your own module, and automatically deploy it with Rancher pipeline and Helm.
To get started, create your own branch and modify `.rancher-pipeline.yml` to your needs (for example [as in this pipeline](https://github.com/folio-org/mod-pubsub/blob/master/.rancher-pipeline.yml)).

Go to Workloads -> Pipelines, run pipeline for that branch, and then Rancher will deploy the new version of that module.

## Building Frontend
Modify [sample pipeline](https://github.com/folio-org/platform-complete/blob/stripes-pipeline-unam/.rancher-pipeline.yml) and start build.

Recommendations about minimum requirements for pipeline namespace to enable successful build:
  * Limit mCPU - 4500m
  * Limit memory - 12000Mi

## Registering modules in Okapi
Module registration runs automatically after the install or upgrade procedure.
Helm uses post-install and post-upgrade hooks to run the module registration job for each module.
Helm gets ModuleDescriptors from the FOLIO Registry (`http://folio-registry.aws.indexdata.com`) -- it gets the latest master branch snapshot descriptor.

Default steps for module registration:
  * Pushing module descriptor
  * Pushing module deployment
  * Creating tenant (default 'diku')
  * Enabling module for tenant

Docker commands can also be used to do registration manually:
  * Registering a particular module (backend or UI module)
    ```
    docker run --rm -e TENANT_ID=diku -e OKAPI_URL=https://<project name>-okapi.ci.folio.org -e MODULE_NAME=<module name> docker.dev.folio.org/folio-okapi-registration
    ```
  * Registering all modules (backend and UI from 'platform-complete' list)
    ```
    docker run --rm -e TENANT_ID=diku -e OKAPI_URL=https://<project name>-okapi.ci.folio.org -e MODULE_NAME='' docker.dev.folio.org/folio-okapi-registration
    ```
  * Registering all UI modules only
    ```
    docker run --rm -e TENANT_ID=diku -e OKAPI_URL=https://<project name>-okapi.ci.folio.org -e MODULE_NAME='platform-complete' docker.dev.folio.org/folio-okapi-registration
    ```

## Apply module permissions
The last step after modules registration is to apply permissions for modules to the admin user.

  * Applying permissions for all installed modules to `diku_admin`
    ```
    docker run --rm -e TENANT_ID=diku -e ADMIN_USER=diku_admin -e ADMIN_PASSWORD=admin -e OKAPI_URL=https://<project name>-okapi.ci.folio.org docker.dev.folio.org/bootstrap-superuser
    ```

## Environment variables
Environment variables for database and backend modules are stored in Kubernetes secrets (Workload -> Secrets) and installed by default to every Project.

## Deployment tips
Some backend modules are based on SpringBoot and require more CPU to start.
To deploy those applications (such as `mod-agreements` or `mod-licenses`) you need to override CPU and memory parameters.
Add 'answers' to module deployment:
  ```
  resources.limits.cpu = "500m"
  resources.limits.memory = "600Mi"
  ```

## Limitations
* No Okapi securing is provided.

<div class="folio-spacer-content"></div>
