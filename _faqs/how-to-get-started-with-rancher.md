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
Useful links:

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
Every project has its own PostgreSQL, Okapi, pre-installed core backend modules, and [Stripes Platform bundle](https://github.com/folio-org/platform-complete). All of these containers run in the default namespace (which is named the same as the Project name).
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

Recommendations about minimum requirements for pipeline Namespace to enable successful build:
  * Limit mCPU - 4500m
  * Limit memory - 12000Mi

## Registering modules in Okapi
Module registration runs automatically after the install or upgrade procedure.
Helm uses post-install and post-upgrade hooks to run the module registration job for each module.
Helm gets ModuleDescriptors from the FOLIO Registry (`http://folio-registry.aws.indexdata.com`) -- it gets the latest `snapshot` descriptor.

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
  resources.limits.cpu = 500m
  resources.limits.memory = 600Mi
  ```
## Questions and answers

### System wide Q&A

Q: How are the modules included by default in a project determined? for example, is it based upon a particular revision of a branch of a platform?
  + It is based on latest FolioCi images from `master` branches. These modules are not upgrading automatically in Rancher and project team members have to do in manually in `App` menu

Q: Are there any projects present at the moment, I could not find any in the list for the default cluster? How is a new project created?
  + New Project are available for authorized GitHub team members. Project deployed with Terraform already, including core backends, UI, secrets, Folio Helm Catalog etc.

Q: What is meant by module in this context? Does this 'Catalog' contain one entry for each module family (e.g. mod-inventory-storage) or one per version of a module (e.g. mod-inventory-storage 19.2.1)
  + Catalog contains module family. Module version not defined in Helm and pulling from `http://folio-registry.aws.indexdata.com` during install or upgrade

Q: Is this the `Apps` menu item at the top of the page? And when accessed from within a project it is specific to that project?
  + `App` menu is accessible to every Project member. Folio Helm repository shared for all Projects and contains complete Folio backends list

Q: Create your own branch of what, the Helm repository or the module repository?
  + Module repository. Helm repository is managed by DevOps

Q: The linked rancher configuration includes a tag `docker.dev.folio.org/mod-pubsub:folijet-latest`. Does this mean that every custom module version is published to an FOLIO local docker repository and needs to be uniquely named to avoid conflicts?
  + You should add/change any tag you want before module building to avoid conflicts

Q: Is this specific to a project or across the whole Rancher cluster? Are these the two separate menu items Workloads and Pipelines under the Resources menu?
  + All these menu same for all Projects, but contains only Project specific pipelines and Workloads

Q: What are the install or upgrade procedures (I haven't noticed them outlined elsewhere in the document)?
  + "Upgrade" button in the right corner of application. "Launch" button to start new one. Please read Rancher guides to find more information

Q: Is this the case for versions of modules built from a branch? If so, what if the branch contains updated descriptors, are those ignored?
  + You should prepare and register custom Module Descriptor in that case

Q: How are these Docker commands run? Are they executed from the Rancher UI?
  + They could be run on developer local machine

Q: Does this mean that each project is an isolated environment and can have separate tenants within it (that each could have different modules installed)?
  + Exactly

### Backend Q&A

Q: How to build, deploy and register a particular branch of a backend module (e.g mod-users/feature-x ) for diku tenant?
  + If you need replace a running module or add new one, go to Workloads→Pipelines, select 'mod-users' repository, call `Run`, select 'feature-x' branch and start building process

Q: How to provision another tenant?
  + Override 'tenantId' in module deployment, for example, in `App` menu add 'answer' to deployment properties `postJob.tenantId = mytenant`. After module deployed, helm starts a registration job with new tenant name

Q: How to build, deploy and register a particular branch of a backend module (e.g mod-users/feature-x ) for a tenant other than diku?
  + Change pipeline and add new answer parameter in Deploy stage (`postJob.tenantId = mytenant`)

Q: How can I CRUD pipelines available via Rancher?
  + It is available for Rancher admin users only

Q: How can I understand what branch and build number has been deployed for a module just by looking at Rancher UI?
  + You have to change pipeline and add Build number to image tag. Rancher pipeline has variable  ${CICD_EXECUTION_SEQUENCE} for that

Q: How to deploy more than on branch of given module?  (mod-users/feature-x and mod-users/feature-y)?
  + If you need to setup new version of a module next to existing one, you have to change pipeline source and remove deploy step and change image tag, run pipeline, go to 'App' menu and deploy built image with new name, for example 'mod-users2'. After that you should prepare new DeploymentDescriptor, ModuleDescriptor and register that module with new tenant and another module version manually

Q: What does the deploy step do?
  + Deploy step in pipeline overrides `image.repository` and `image.tag` values and starts module install/upgrade procedure in `App` menu with new docker image

Q: How prepare new DeploymentDescriptor, ModuleDescriptor and register is done, by making API requests directly to the Okapi deployed in your project?
  + Yes, use [Okapi manual](https://github.com/folio-org/okapi/blob/master/doc/guide.md) to find out more about that

Q: How to deploy (with I believe includes proxy registration, discovery registration and tenant enablement) a custom module version that has changes to the module descriptor?
  + You should prepare new descriptors and do registration manually

Q: How does that module version get deployed in order for it to be registered?
  + Module version pulling from [Folio registry](http://folio-registry.aws.indexdata.com)

Q: How to deploy coordinated breaking compatibility changes across multiple modules? For example, 1 UI, 1 BL, and 1 Storage modules should be updated together?
  + You have to deploy/register modules in Rancher with appropriate order or use bulk registration command from this documentation

Q: As I understand it, a deployment in the Rancher based projects will also enable a module version for a tenant. Is that the case? If so, this will break if that would cause compatibility rules to be broken
  + Okapi does not allow to break compatibility rules

Q: How can multiple instances of the same module version be deployed and registered with Okapi
  + Okapi does not allow to register same version of one module. And does not allow to enable more than one module for one tenant. You have to change module version and register another tenant in that case

### UI Q&A

Q: How to build, deploy and register a UI bundle which includes a particular branch of a front-end module (e.g ui-users/feature-A )?
  + Clone 'platform-core' or 'platform-complete' repository, in 'package.json' file, add/change "@folio/ui-users": "git://github.com/folio-org/ui-users.git#feature-A", build and deploy docker image into the Rancher

Q: How to run more than one bundle (e.g. one with ui-users/feature-A an one with ui-users/feature-B ) for the same tenant?
  + Deploy two or more UI bundle images. Do override Ingress URL for each bundle utilizing `answers`

Q: What is the Ingress URL?
  + URL to access modules outside Rancher. You can assign such endpoint with that rules
  ```
  ingress.enabled = true
  ingress.hosts[0].host = <project_name>-myendpoint.ci.folio.org
  ingress.hosts[0].paths[0] = /
  ```
  Always use `*.ci.folio.org` domain name template!

Q: How to run 2 bundles (e.g. one with ui-users/feature-A an one with ui-users/feature-B ) for 2 different tenants?
  + Deploy two or more UI bundle images. Do override Ingress URL for each bundle. Use bulk registration command from documentation to register another tenants

### Environment Q&A
Q: How to do a soft reset of the whole system (start from scratch without DevOps help)?
  + Wipe out Postgres data with script (do not delete Okapi system tables), restart Okapi, use bulk registration command

Q: How to do a hard reset of the whole system (DevOps)?
  + Recreate Project with Terraform

Q: Is there a way to move the whole of the system onto the latest in one step?
  + DevOps script 'recreate_modules.sh' in Terraform folder

Q: How can I provision previous release system? For example, Fameflower. That would be important for schema updates testing.
  + It is very hard to implement. Needs a lot of manual job of deployment and registration

Q: Can I create my private container registry and point Helm charts to it instead of folio-ci?
  + That is the main approach to build and deploy UI modules now

Q: Can I have 2 FOLIO systems within 1 Rancher project?
  + It is very hard to implement. Better solution is to create a new Cluster for now

Q: I forgot that I was not using a system for a while. Is it going to be automatically deleted after predefined expiration interval?
  + It can be performed by Terraform and Jenkins job. Not implemented

Q: I stopped using the system for today. Can I suspend it until tomorrow so it doesn't burn AWS resources?
  + You can switch all ReplicasCount for all modules to 0

Q: Who can do that? How is it done?
  + It can be done in `Resources->Worklods` menu. Select desired Kubernetes Pod and use `+` and `-` buttons

Q: How do developers access the logs?
  + Developer can use `View logs` in `Workloads` menu in every Kubernetes Pod. Or use `https://logs.ci.folio.org` aggregator

## Limitations
* No Okapi securing is provided.

<div class="folio-spacer-content"></div>
