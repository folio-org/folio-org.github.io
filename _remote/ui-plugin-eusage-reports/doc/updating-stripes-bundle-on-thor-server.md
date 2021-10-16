---
layout: null
---

# Updating the Stripes bundle for the Thor project in Rancher.

_By John Malconian, edited by Mike Taylor_

July-October 2021.

<!-- md2toc -l 2 updating-stripes-bundle-on-thor-server.md -->
* [Create the code](#create-the-code)
* [Build the UI bundle](#build-the-ui-bundle)
* [Deploy the new bundle](#deploy-the-new-bundle)
* [View the new bundle](#view-the-new-bundle)
* [If there are new permissions](#if-there-are-new-permissions)


## Create the code

* Write the code in `ui-plugin-eusage-reports` and related modules.
* Merge the changes to their respective master branches.
* Watch the progress of [the tip-of-master build job ](https://jenkins-aws.indexdata.com/job/folio-org/job/ui-plugin-eusage-reports/job/master/) and wait until it has finished.


## Build the UI bundle

* [Log into Jenkins](https://jenkins-aws.indexdata.com/)
* Navigate to [the BUILD-UI job](https://jenkins-aws.indexdata.com/job/scratch_environment/job/BUILD-UI/)
* Click on "Build with Parameters".
* Select `thor` from the "teamName" dropdown and `thor-snapshot` from the "branch" dropdown, then click the **Build** button.
* Jenkins will build a `platform-complete` snapshot Stripes bundle, taking about ten minutes, and push it to the local Docker repository, `docker.dev.folio.org`.
* Examine the Jenkins job's logs to determine the build's tag, which will be of the form `thor-`_number_, e.g. `thor-97`.

**Note.**
The image created will be called docker.dev.folio.org/platform-complete:thor-$JENKINS_BUILD_NUMBER. You can see this image, and others, in [the repository browser](https://repository.folio.org/#browse/browse:docker-ci-preview:v2%2Fplatform-complete%2Ftags%2Fthor-97)


## Deploy the new bundle

* [Log into Rancher](https://rancher.dev.folio.org/login)
* Click on the `folio-eks-2-us-west-2` cluster
* From the `folio-eks-2-us-west-2` top menu of the new page, select the `thor` project.
* Select "Apps" from the navigation bar of the new page.
* Search within the page for the `platform-complete` "app", click on the three vertical dots, and select "Upgrade".
* On the upgrade page, the only option that needs to be modified is the `image.tag` variable: set it to the tag of the docker image created in the previous step. e.g. `thor-97`.
* Click on the **Upgrade** button at the bottom of the page. Rancher will then replace the existing Stripes bundle with a Docker image of the new bundle.


## View the new bundle

* Log out of any existing thor UI sessions
* Shift-reload https://thor.ci.folio.org in your browser
* Log back into the UI.


## If there are new permissions

The process described above is sufficient assuming no new permissions have been added to the module. If new permissions are added, you will need to do two things:

1. Add them to the system: get the latest module descriptor for the UI module providing new permissions from the FOLIO MD registry, POST it to Okapi, and enable for the diku tenant. This can all be done using a single Docker command:
```
	docker run --rm -e TENANT_ID=diku -e OKAPI_URL=https://thor-okapi.ci.folio.org -e MODULE_NAME=folio_plugin-eusage-reports docker.dev.folio.org/folio-okapi-registration
```

2. Grant the permissions to a user, most conviently be adding them all in a single shot:
```
	docker run --rm -e TENANT_ID=diku -e ADMIN_USER=diku_admin -e ADMIN_PASSWORD=Thor_Admin3636 -e OKAPI_URL=https://thor-okapi.ci.folio.org folioci/bootstrap-superuser 
```

See [_How to get started with Rancher environment_](https://dev.folio.org/faqs/how-to-get-started-with-rancher/) for additional info.


