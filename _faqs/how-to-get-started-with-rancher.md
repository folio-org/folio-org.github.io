---
layout: page
title: How to get started with Rancher environment
titleLeader: "FAQ |"
menuTopTitle: FAQs
categories: development-tips
faqOrder: 10
---

## Introduction

Each development team has access to a "developer scratch environment" to ensure that their changes are ready to be finalised.

Rancher is a Kubernetes management tool.
Useful links:

* FOLIO rancher main URL: [https://rancher.ci.folio.org](https://rancher.ci.folio.org)
* [Rancher Environments](https://wiki.folio.org/display/FOLIJET/Rancher+Environments) -- Roadmap Tracker overview and links for each team environment; and Rancher Backlog of Jira [tickets](/faqs/how-to-raise-devops-ticket/#rancher-scratch-environments).
* Project UI URL: `https://<Project name>.ci.folio.org`
* Basic Okapi URL: `https://<Project name>-okapi.ci.folio.org`
* PgAdmin4 URL: `https://<Project name>-pgadmin.ci.folio.org` (login as user 'chart@example.local' or 'user@folio.org' password 'SuperSecret')
* Logs: https://logs.ci.folio.org/

Before commencing become familiar with this FAQ.
Some teams also provide [further general instructions](/guides/run-local-folio/#scratch-environments-rancher-docker).

For general assistance use the [Slack channel](/guidelines/which-forum/#slack) `#folio-rancher-support` and help via your team-specific channel.

To raise Jira tickets related to Rancher scratch environments, refer to the [FAQ](/faqs/how-to-raise-devops-ticket/#rancher-scratch-environments).
This is needed when contacting the `#folio-rancher-support` Slack channel.

See the Wiki [How to work with Rancher environments](https://folio-org.atlassian.net/wiki/spaces/FOLIJET/pages/1396559/How+to+work+with+Rancher+environments).

The [Kitfox](https://wiki.folio.org/display/FOLIJET/Kitfox+Team+DevOps+-+Dev+Support) DevOps team wiki page has further resources regarding Rancher scratch environments.

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

Here is default answers for Frontend Bundle Application deployment:
  ```
    resources.limits.cpu = 200m
    resources.limits.memory = 500Mi
    image.tag = <project_name>-latest
    ingress.enabled = true
    ingress.hosts[0].host = <project_name>.ci.folio.org
    ingress.hosts[0].paths[0] = /
 ```

In `package.json` set `--max-old-space-size=8192` to build options.

## Registering modules in Okapi
Module registration runs automatically after the install or upgrade procedure.
Helm uses post-install and post-upgrade hooks to run the module registration job for each module.
Helm gets ModuleDescriptors from the FOLIO Registry (`https://folio-registry.dev.folio.org`) -- it gets the latest `snapshot` descriptor.

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
    docker run --rm -e TENANT_ID=diku -e ADMIN_USER=diku_admin -e ADMIN_PASSWORD=admin -e OKAPI_URL=https://<project name>-okapi.ci.folio.org folioci/bootstrap-superuser
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
If you notice a pod restarting a lot, it may be that it is running out of memory. Usually increasing the `resources.limits.memory` in its yaml via Rancher will fix this. The pod limits on CPU may also be too low to allow your cluster to run reliably. If things go wrong, consider increasing `resources.limits.cpu` for a given pod. You may also consider removing the pod-level `resources.limits.cpu` limit and set a limit for your namespace instead, so as to not deplete other teams' resources on the cluster.

You can set a namespace limit in the Edit menu item in the Rancher UI:

![set namespace cpu limits](/images/edit-namespace-cpu-limits.png)

## S3 Storage
Each development team has been provided with a dedicated S3 bucket that can be used for additional storage.   The name of
each team's S3 bucket is the name of the team prepended with 'folio-'.  For example,  'folio-folijet'.  Each bucket is
read/write from any K8s pod running in the dev environment.  Additional credentials are not required.   Each bucket is
also public read-only. To share and access an object in the S3 environment outside of the dev-environment, the object
must be explicitly included in the URL. For example, to download the README.md file in the folijet team bucket, the following URL
would be used:

   ```
   http://folio-folijet.s3.amazonaws.com/README.md
   ```

## Manage scratch environment
To create, update or delete your environment in Rancher, use this Jenkins pipeline:\
<https://jenkins-aws.indexdata.com/job/scratch_environment/job/manage-scratch-environment/>

* Ensure that you are logged in to Jenkins
* Select "Build with Parameters"
* Choose your team Name:

![choose team name](/images/rancher-scratch-env.png)

* Choose which action that you want to perform:
  - Create: to create new environment in rancher
  - Update: to update your environment
  - Delete: **Be Careful!** This action will completely delete the environment from Rancher

![choose action create environment](/images/rancher-Action.png)

* Then select "Build"

## Build backend module from branch
Any backend module can be built from a specific branch. Use this Jenkins pipeline:\
<https://jenkins-aws.indexdata.com/job/scratch_environment/job/BUILD-BACKEND/>

* Ensure that you are logged in to Jenkins
* Select "Build with Parameters"
* Choose the module that you want to build
* Choose which branch that you want to build the module from
* Then select "Build"
* Select "Console Output"
* Near the end, find the full image name with the proper tag:

![choose image name tag](/images/rancher-tag.png)

* Go to your environment in Rancher –> Apps –> the module that you built
* Select the vertical ellipsis &#8942; and then "Upgrade"

![choose upgrade](/images/rancher-upgrade.png)

* In the "Answers" section, add the following:
  - Variable: `image.repository`
    - Value: `docker.dev.folio.org/module_name`
  - Variable: `image.tag`
    - Value: the tag obtained from the build

![add answers variables](/images/rancher-variables.png)

* Select "Upgrade"

## Build UI module from branch
To build UI from a specific branch, use this Jenkins pipeline:\
<https://jenkins-aws.indexdata.com/job/scratch_environment/job/BUILD-UI/>

* Ensure that you are logged in to Jenkins
* Select "Build with Parameters"
* Choose your team name
* Choose the branch that you want to build from
* Then select "Build"

![choose branch to build from](/images/rancher-UI-choose-branch.png)

The tag for the image is: docker.dev.folio.org/platform-complete:`team_name-build` number

* Go to Rancher -> Apps -> platform-complete
* Select the vertical ellipsis &#8942; and then "Upgrade"

![choose upgrade ui](/images/rancher-UI-upgrade.png)

* Add the following variables in Answers Section:
  - Variable: `image.repository`
    - Value: `docker.dev.folio.org/platform-complete`
  - Variable: `image.tag`
    - Value: `team_name-build` number

![add answers variables](/images/rancher-UI-tag.png)

* Select "Upgrade"

## Create Elasticsearch index snapshot

To create Elasticsearch index snapshot for Rancher performance testing cluster,  go to your Rancher environment, choose your performance testing cluster (`perf-ekes-team_name`):
* Find your Elasticsearch hostname, username, and password. In Rancher test environment, select your project name ( Team name ) ->Secrets.
 ![elasticsearch select secrets](/images/secrets.png)
* Scroll down and find `Namespace:team_name` and select the vertical ellipsis for `db-connect-modules`, and then choose `Edit`
![elasticsearch select db-connect-modules secrets](/images/dbconnectmodules.png)
* Copy the value of `ELASTICSEARCH_HOST`, `ELASTICSEARCH_USERNAME`, and `ELASTICSEARCH_PASSWORD`.
![elasticsearch set db-connect-modules secrets](/images/elasticsearch.png)
* Ask the Kitfox DevOps administrator to create the repository for you. (The repository is attached to persistent AWS S3 bucket.)
* Go to project name ( Team name ) -> Resources -> Workloads -> ubuntu, select the vertical ellipsis, and choose: `Execute Shell`
![choose execute shell](/images/executeshell.png)

### Create a snapshot
 `curl -XPUT 'ELASTICSEARCH_HOST/_snapshot/repository-name/snapshot-name -u ELASTICSEARCH_USERNAME:ELASTICSEARCH_PASSWORD`
### Restore a snapshot
 `curl -XPOST 'ELASTICSEARCH_HOST/_snapshot/repository-name/snapshot-name/_restore' -u ELASTICSEARCH_USERNAME:ELASTICSEARCH_PASSWORD`
### Restore a specific index
 `curl -XPOST 'ELASTICSEARCH_HOST/_snapshot/repository-name/snapshot-name/_restore' -d '{"indices": "my-index"}' -H 'Content-Type: application/json' -u ELASTICSEARCH_USERNAME:ELASTICSEARCH_PASSWORD`

## Running Karate integration tests

You can run Karate integration tests against your Rancher environment. Examples of Karate tests you can run are the [FOLIO integration tests](https://github.com/folio-org/folio-integration-tests). To run the FOLIO integration tests complete the following two steps:
1. Add a user with the username of `testing_admin` and the password of `admin` to the supertenant.
Refer to the [Introduction](#introduction) section if assistance is needed.
2. Secure the supertenant.

Securing the supertenant happens when you enable mod-authtoken on the supertenant. To secure the supertenant, create a file called enable.json with the following contents:

```
[
  {
    "id": "mod-authtoken",
    "action": "enable"
  }
]
```

Then use this file in the body of your POST request in a curl command like the following:

```
curl -X POST -H "X-Okapi-Token: $token" -H "Content-Type: application/json" -d @enable.json $okapi/_/proxy/tenants/supertenant/install
```
Note that the above command assumes that `$token` and `$okapi` have been exported to your environment.

To unsecure the supertenant repeat the process, perhaps creating another file, but this time have the `action` in your file be `disable`. Unsecuring the supertenant makes it easier to install additional modules.

Once you have created the special admin user and secured the supertenant, modify your Karate tests to point to the okapi endpoint in your Rancher project. Currently this can be done by editing the karate-config.js file in your project.

## Questions and answers

### System wide Q&A

Q: How are the modules determined that are included by default in a project? For example, is it based upon a particular revision of a branch of a platform?
  + It is based on the latest `folioci` images from `master` branches. These modules are not upgraded automatically in Rancher, so the project team members need to do it manually in the `App` menu.

Q: Are there any projects present at the moment. None could be found in the list for the default cluster? How is a new project created?
  + New Projects are available for authorized GitHub team members. Projects are already deployed with Terraform, including core backends, UI, secrets, FOLIO Helm Catalog etc.

Q: What is meant by module in this context? Does this 'Catalog' contain one entry for each module family (e.g.` mod-inventory-storage`) or one per version of a module (e.g. `mod-inventory-storage-19.2.1`)?
  + Catalog contains the module family. Module versions are not defined in Helm, and are pulled from `https://folio-registry.dev.folio.org` during install or upgrade.

Q: Is this the `Apps` menu item at the top of the page? When it is accessed from within a project, is it specific to that project?
  + The `App` menu is accessible to every Project member. The FOLIO Helm repository is shared for all Projects, and contains the complete FOLIO backends list.

Q: Create your own branch of what, the Helm repository or the module repository?
  + The module repository. The FOLIO Helm repository is managed by the Kitfox DevOps team.

Q: The linked rancher configuration includes a tag `docker.dev.folio.org/mod-pubsub:folijet-latest`. Does this mean that every custom module version is published to a FOLIO local docker repository and needs to be uniquely named to avoid conflicts?
  + Add/change any tag that is needed before the module building to avoid conflicts.

Q: Is this specific to a project or across the whole Rancher cluster? Are these the two separate menu items Workloads and Pipelines under the Resources menu?
  + All these menus are the same for all Projects, but contain only Project specific pipelines and Workloads.

Q: What are the install or upgrade procedures (they are not outlined elsewhere in this document)?
  + The "Upgrade" button is in the right-hand corner of the application. Use the "Launch" button to start a new one. Please read the Rancher guidelines for more information.

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
  + Module version pulling from the FOLIO registry (`https://folio-registry.dev.folio.org`).

Q: How to deploy coordinated breaking compatibility changes across multiple modules? For example, one UI and one business-logic module and one storage module should be updated together?
  + The deploy/register of modules in Rancher needs to be done in the appropriate order. Or use the bulk registration command from this documentation.

Q: As I understand it, a deployment in the Rancher based projects will also enable a module version for a tenant. Is that the case? If so, this will break if that would cause compatibility rules to be broken.
  + Okapi does not allow it to break compatibility rules.

Q: How can multiple instances of the same module version be deployed and registered with Okapi?
  + Okapi does not allow to register the same version of one module. And does not allow to enable more than one module for one tenant. In that case, the module version needs to be changed, and register another tenant.

### UI Q&A

Q: How to build, deploy, and register a UI bundle which includes a particular branch of a front-end module (e.g. `ui-users/feature-A`)?
  + Clone the 'platform-complete' repository, in 'package.json' file, add/change "@folio/ui-users": "git://github.com/folio-org/ui-users.git#feature-A", Then build and deploy the docker image into the Rancher.

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

Q: How to do a soft reset of the whole system (i.e. start from scratch without Kitfox DevOps help)?
  + Wipe out Postgres data with a script (do not delete Okapi system tables), restart Okapi, use the bulk registration command.

Q: How to do a hard reset of the whole system (Kitfox DevOps)?
  + Recreate Project with Terraform.

Q: Is there a way to move the whole of the system onto the latest in one step?
  + Kitfox DevOps script 'recreate_modules.sh' in the Terraform folder.

Q: How can a previous release system be provisioned (for example, [Goldenrod release](https://github.com/folio-org/platform-complete/tree/q2-2020))? That would be important for testing of schema updates.
  + Override repository and tag for each backend module and do upgrade:
    ```
    image.repository = folioorg/<MODULE_NAME>
    image.tag = <MODULE_VERSION>
    ```
    Registration Post job will register Descriptor with this version.
    Rebuild and install UI with needed version.
    Better idea is to ask Kitfox DevOps to perform it with Terraform.

Q: Can I create my private container registry and point Helm charts to it instead of folioci?
  + That is currently the main approach to build and deploy UI modules.

Q: Can there be two FOLIO systems within one Rancher project?
  + It is very hard to implement. The better solution at the moment is to create a new Cluster.

Q: I forgot that I was not using a system for a while. Is it going to be automatically deleted after a predefined expiration interval?
  + It can be performed by Terraform and Jenkins job. Not implemented.

Q: I stopped using the system for today. Can I suspend it until tomorrow so it doesn't burn AWS resources?
  + You can switch all ReplicasCount for all modules to zero.

Q: Who can do that? How is it done?
  + It can be done in the `Resources->Workloads` menu. Select the desired Kubernetes Pod and use `+` and `-` buttons.

Q: How do developers access the logs?
  + Developers can use `View logs` in `Workloads` menu in every Kubernetes Pod. Or use `https://logs.ci.folio.org` aggregator.

## Limitations
* No Okapi securing is provided.

<div class="folio-spacer-content"></div>
