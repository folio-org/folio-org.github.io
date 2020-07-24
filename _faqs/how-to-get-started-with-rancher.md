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

Q: How are the modules determined that are included by default in a project? For example, is it based upon a particular revision of a branch of a platform?
  + It is based on the latest `folioci` images from `master` branches. These modules are not upgraded automatically in Rancher, so the project team members need to do it manually in the ``App` menu.

Q: Are there any projects present at the moment. None could be found in the list for the default cluster? How is a new project created?
  + New Projects are available for authorized GitHub team members. Projects are already deployed with Terraform, including core backends, UI, secrets, FOLIO Helm Catalog etc.

Q: What is meant by module in this context? Does this 'Catalog' contain one entry for each module family (e.g.` mod-inventory-storage`) or one per version of a module (e.g. `mod-inventory-storage-19.2.1`)?
  + Catalog contains the module family. Module versions are not defined in Helm, and are pulled from `http://folio-registry.aws.indexdata.com` during install or upgrade.

Q: Is this the `Apps` menu item at the top of the page? When it is accessed from within a project, is it specific to that project?
  + The `App` menu is accessible to every Project member. The FOLIO Helm repository is shared for all Projects, and contains the complete FOLIO backends list.

Q: Create your own branch of what, the Helm repository or the module repository?
  + The module repository. The FOLIO Helm repository is managed by the FOLIO DevOps team.

Q: The linked rancher configuration includes a tag `docker.dev.folio.org/mod-pubsub:folijet-latest`. Does this mean that every custom module version is published to a FOLIO local docker repository and needs to be uniquely named to avoid conflicts?
  + Add/change any tag that is needed, before the module building to avoid conflicts.

Q: Is this specific to a project or across the whole Rancher cluster? Are these the two separate menu items Workloads and Pipelines under the Resources menu?
  + All these menus are the same for all Projects, but contain only Project specific pipelines and Workloads.

Q: What are the install or upgrade procedures (they are not outlined elsewhere in this document)?
  + The "Upgrade" button is in the right-hand corner of the application. Use the "Launch" button to start a new one. Please read the Rancher guides for more information.

Q: Is this the case for versions of modules built from a branch? If so, what happens if the branch contains updated descriptors, are those ignored?
  + In that case, prepare and register a custom ModuleDescriptor.

Q: How are these Docker commands run? Are they executed from the Rancher UI?
  + They could be run on a developer's local machine.

Q: Does this mean that each project is an isolated environment and can have separate tenants within it (that each could have different modules installed)?
  + Exactly.

### Backend Q&A

Q: How to build, deploy, and register a particular branch of a backend module (e.g. `mod-users/feature-x`) for diku tenant?
  + If you need replace a running module or add new one, go to Workloads→Pipelines, select 'mod-users' repository, call `Run`, select 'feature-x' branch and start the building process.

Q: How to provision another tenant?
  + Override 'tenantId' in module deployment, for example, in `App` menu add 'answer' to deployment properties `postJob.tenantId = mytenant`. After the module is deployed, then Helm starts a registration job with the new tenant name.

Q: How to build, deploy, and register a particular branch of a backend module (e.g mod-users/feature-x ) for a tenant other than diku?
  + Change pipeline and add new answer parameter in the Deploy stage (`postJob.tenantId = mytenant`).

Q: How can CRUD pipelines be available via Rancher?
  + It is available only for Rancher admin users.

Q: How can I understand what branch and build number has been deployed for a module, just by looking at the Rancher UI?
  + You need to change pipeline and add Build number to the image tag. Rancher pipeline has the variable `${CICD_EXECUTION_SEQUENCE}` for that.

Q: How to deploy more than one branch of given module? For example `mod-users/feature-x` and `mod-users/feature-y`?
  + If a new version of a module needs to be setup next to existing one, then change pipeline source and remove deploy step and change image tag, run pipeline, go to 'App' menu and deploy the built image with a new name (e.g. `mod-users2`). After that, prepare a new DeploymentDescriptor, ModuleDescriptor, and register that module with new tenant and another module version manually.

Q: What does the deploy step do?
  + The deploy step in pipeline overrides `image.repository` and `image.tag` values, and starts the module install/upgrade procedure in the `App` menu with the new docker image.

Q: How is the preparation done for a new DeploymentDescriptor, ModuleDescriptor, and registered. Is it by making API requests directly to the Okapi deployed in your project?
  + Yes, use the [Okapi manual](https://github.com/folio-org/okapi/blob/master/doc/guide.md) to find out more about that.

Q: How to do deployment (which includes proxy registration, discovery registration, and tenant enablement) of a custom module version that has changes to the ModuleDescriptor?
  + Prepare new descriptors and do the registration manually.

Q: How does that module version get deployed, in order for it to be registered?
  + Module version pulling from the FOLIO registry (`http://folio-registry.aws.indexdata.com`).

Q: How to deploy coordinated breaking compatibility changes across multiple modules? For example, one UI and one business-logic module and one storage module should be updated together?
  + The deploy/register of modules in Rancher needs to be done in the appropriate order. Or use the bulk registration command from this documentation.

Q: As I understand it, a deployment in the Rancher based projects will also enable a module version for a tenant. Is that the case? If so, this will break if that would cause compatibility rules to be broken.
  + Okapi does not allow it to break compatibility rules.

Q: How can multiple instances of the same module version be deployed and registered with Okapi?
  + Okapi does not allow to register the same version of one module. And does not allow to enable more than one module for one tenant. In that case, the module version needs to be changed, and register another tenant.

### UI Q&A

Q: How to build, deploy, and register a UI bundle which includes a particular branch of a front-end module (e.g. `ui-users/feature-A`)?
  + Clone the 'platform-core' or 'platform-complete' repository, in 'package.json' file, add/change "@folio/ui-users": "git://github.com/folio-org/ui-users.git#feature-A", Then build and deploy the docker image into the Rancher.

Q: How to run more than one bundle (e.g. one with `ui-users/feature-A` and one with `ui-users/feature-B`) for the same tenant?
  + Deploy two or more UI bundle images. Do override Ingress URL for each bundle by utilizing '`answers`'.

Q: What is the Ingress URL?
  + The URL to access modules outside Rancher. Assign such an endpoint with these rules:
  ```
  ingress.enabled = true
  ingress.hosts[0].host = <project_name>-myendpoint.ci.folio.org
  ingress.hosts[0].paths[0] = /
  ```
  Always use `*.ci.folio.org` domain name template!

Q: How to run two bundles (e.g. one with `ui-users/feature-A` and one with `ui-users/feature-B`) for two different tenants?
  + Deploy two or more UI bundle images. Do override Ingress URL for each bundle. Use the bulk registration command from documentation to register another tenant.

### Environment Q&A

Q: How to do a soft reset of the whole system (i.e. start from scratch without DevOps help)?
  + Wipe out Postgres data with a script (do not delete Okapi system tables), restart Okapi, use the bulk registration command.

Q: How to do a hard reset of the whole system (DevOps)?
  + Recreate Project with Terraform.

Q: Is there a way to move the whole of the system onto the latest in one step?
  + DevOps script 'recreate_modules.sh' in the Terraform folder.

Q: How can a previous release system be provisioned (for example, Fameflower)? That would be important for testing of schema updates.
  + It is very hard to implement. Needs a lot of manual jobs of deployment and registration.

Q: Can I create my private container registry and point Helm charts to it instead of folioci?
  + That is currently the main approach to build and deploy UI modules.

Q: Can there be two FOLIO systems within one Rancher project?
  + It is very hard to implement. The better solution at the moment is to create a new Cluster.

Q: I forgot that I was not using a system for a while. Is it going to be automatically deleted after a predefined expiration interval?
  + It can be performed by Terraform and Jenkins job. Not implemented.

Q: I stopped using the system for today. Can I suspend it until tomorrow so it doesn't burn AWS resources?
  + You can switch all ReplicasCount for all modules to zero.

Q: Who can do that? How is it done?
  + It can be done in the `Resources->Worklods` menu. Select the desired Kubernetes Pod and use `+` and `-` buttons.

Q: How do developers access the logs?
  + Developers can use `View logs` in `Workloads` menu in every Kubernetes Pod. Or use `https://logs.ci.folio.org` aggregator.

## Limitations
* No Okapi securing is provided.

<div class="folio-spacer-content"></div>
