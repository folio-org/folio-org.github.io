---
layout: null
---

# Centralised GitHub Workflows for Maven

<!-- ../okapi/doc/md2toc -l 2 -h 3 README-maven.md -->
* [Introduction](#introduction)
* [Usage](#usage)
* [Configuration](#configuration)
    * [Configuration: java-version](#configuration-java-version)
    * [Configuration: publish-module-descriptor](#configuration-publish-module-descriptor)
    * [Configuration: allow-snapshots-release](#configuration-allow-snapshots-release)
    * [Configuration: do-sonar-scan](#configuration-do-sonar-scan)
    * [Configuration: do-docker](#configuration-do-docker)
    * [Configuration: docker-health-command](#configuration-docker-health-command)
    * [Configuration: docker-label-documentation](#configuration-docker-label-documentation)
* [Docker image metadata](#docker-image-metadata)
* [Install the caller Workflow](#install-the-caller-workflow)
* [Release procedures](#release-procedures)
  * [Release procedures FAQ](#release-procedures-faq)
* [Limitations](#limitations)
    * [Only top-level Dockerfile](#only-top-level-dockerfile)
* [Oddities](#oddities)
    * [Timeout at ModuleDescriptor registry](#timeout-at-moduledescriptor-registry)

## Introduction

The Workflows in this repository named `maven*.yml` are for building Maven-based back-end modules.
Docker images are published to FOLIO Docker Hub.
ModuleDescriptors are published to the FOLIO Registry.

Refer to example build system and workflows at https://github.com/folio-org/mod-settings

## Usage

Create a `.github/workflows` directory in the root of the module repository, and add a file named `maven.yml` with the following content.

If there is already a workflow named maven.yml for verifying basic Maven builds, then rename that file.
It will ease management to have the same filename at every repository.

Follow [Install the caller Workflow](#install-the-caller-workflow) section below to install the initial workflow.

After the first Actions run, do not rename this caller workflow, as that will reset the GitHub run number and so wreck the order of the ModuleDescriptor identifiers.


```yaml
name: Maven central workflow

on:
  push:
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  maven:
    uses: folio-org/.github/.github/workflows/maven.yml@v1
    # Only handle push events from the main branch or tags, to decrease PR noise
    if: github.ref_name == github.event.repository.default_branch || github.event_name != 'push' || github.ref_type == 'tag'
    secrets: inherit
```

## Configuration

If there is a need to over-ride defaults, then add configuration variables to the single "with:" section of the module maven.yml Workflow.

Add the section at the end of the Workflow immediately after the "secrets" item.
For example:

```yaml
    # ...
    secrets: inherit
    with:
      java-version: '17'
      # Add configuration variables here if needed.
```

### Configuration: java-version

Optional. Default = '21'

```yaml
    with:
      java-version: '17'
```

### Configuration: publish-module-descriptor

Some Maven-based projects do not have a ModuleDescriptor.

Optional. Default = true

```yaml
    with:
      publish-module-descriptor: false
```

### Configuration: allow-snapshots-release

Normally a release must not use dependencies that are "snapshot" versions.

On rare occasions this might be needed.

Optional. Default = false

```yaml
    with:
      allow-snapshots-release: true
```

### Configuration: do-sonar-scan

Sonar can be disabled if that is needed, for example when a new project is not yet ready to commence the scans.

Optional. Default = true

```yaml
    with:
      do-sonar-scan: false
```

### Configuration: do-docker

Some Maven-based projects do not utilise Docker. If so then provide this variable as "false".

If this variable is "false", then also no ModuleDescriptor will be published.

> [!NOTE]
> See [Limitations - Only top-level Dockerfile](#only-top-level-dockerfile) at this stage.

Optional. Default = true

```yaml
    with:
      do-docker: false
```

### Configuration: docker-health-command

If this variable is provided, then the Docker Health Check will be run prior to the final building of the image.
If it fails, then no Docker image is built, and a ModuleDescriptor will not be published.

> [!IMPORTANT]
> The Health Check is required for Docker-providing modules.
> Refer to [DR-000007 - Back End Module Health Check Protocol](https://folio-org.atlassian.net/wiki/x/kiJN).

Note that the workflow will utilise this variable if provided, but does not enforce it.
The status will be reported to the workflow "Summary".

Optional. Default = None

```yaml
    with:
      docker-health-command: 'wget --no-verbose --tries=1 --spider http://localhost:8081/admin/health || exit 1'
```

### Configuration: docker-label-documentation

If not provided then the "org.opencontainers.image.documentation" label of the Docker image will be empty.

Optional. Default = None

```yaml
    with:
      docker-label-documentation: 'https://.../documentation.md'
```

## Docker image metadata

The docker image will have various labels automatically applied.

Note: If the "org.opencontainers.image.description" label of the generated image is empty, then that is because the module's GitHub repository is missing the "About" description in the top-right corner of its GitHub front page.
See advice at [Create a new FOLIO module and do initial setup](https://dev.folio.org/guidelines/create-new-repo/),
and bear in mind that Docker Hub imposes a [content length limit](https://github.com/peter-evans/dockerhub-description#content-limits) of 100 bytes for that short-description, so it will be truncated at that.

See also the  [Configuration: docker-label-documentation](#configuration-docker-label-documentation) variable.

## Install the caller Workflow

> [!NOTE]
> If there is not yet a JIRA ticket at the co-ordination Epic [FOLIO-4443](https://folio-org.atlassian.net/browse/FOLIO-4443) then please raise one in a similar manner to the others, and add that as the Parent.

Create a new branch at the module repository.

Create a file at `.github/workflows/maven.yml` as explained at the [Usage](#usage) section.

Add other [Configuration](#configuration) variables to suit the needs of the module, e.g. `docker-health-command` variable.
Align properties with the old Jenkinsfile (noting the defaults shown in the [Configuration](#configuration) section).

Do `git mv Jenkinsfile Jenkinsfile-disabled` (so that it can be restored quickly if needed, and still be able to review its properties).

Commit and push.

(If it is desired to do a branch run prior to raising the pull-request, then "dispatch" the workflow on that branch.
However the line 12 "if:" will need to be temporarily commented-out for one run, because the workflow does not yet exist on mainline branch.)

Raise the pull-request, and review the run results.

The merge will be denied. The "check" for the old Jenkins "pr-merge" will fail.

Edit "Branch protection" to delete that check, and add a new `GitHub Actions` check:

For most Docker-providing repositories the check will be: \
`maven / docker-publish / Docker build`

For non-Docker repositories the check will be: \
`maven / Build / Build`

If assistance is needed with "Branch protection" then [contact](https://dev.folio.org/faqs/how-to-raise-devops-ticket/#general-folio-devops) FOLIO DevOps and advise the checks that you need.

Wait until after the next "Platform build" to give some time if things go amiss.
https://dev.folio.org/guides/automation/#platform-hourly-build (finishes approx 53m past)
https://github.com/folio-org/platform-complete/commits/snapshot/

Merge and watch the mainline branch run.

Review the results for the Docker image and ModuleDescriptor. The identifier for all modules will use base number 2000 plus the sequential workflow run_number (e.g. 2002 for the second run).

Visit the following resources (adjusted for the relevant repository name):
* https://hub.docker.com/r/folioci/mod-settings/tags
* https://hub.docker.com/r/folioci/mod-settings (for new generated description)
* https://folio-registry.dev.folio.org/_/proxy/modules?filter=mod-settings&latest=1
* https://folio-registry.dev.folio.org/_/proxy/modules?filter=mod-settings&latest=1&full=true
* https://repository.folio.org/#browse/browse:maven-snapshots:org%2Ffolio%2Fmod-settings
* https://sonarcloud.io/project/overview?id=org.folio:mod-settings

Await success of the subsequent "Platform hourly build" and see snapshot branch updated.

If there is a need to quickly revert to Jenkins-based build, then [delete](https://github.com/folio-org/mod-settings/blob/master/.github/workflows/delete-test-md.yml) the published ModuleDescriptor (with great care), re-configure the branch protection checks, restore the Jenkinsfile.

## Release procedures

1. Create a temporary release branch `tmp-release-X.Y.Z`;
2. Commit all relevant changes and this release's date to `NEWS.md`;
   - `git log --pretty=format:"%s" $(git describe --tags --abbrev=0)..HEAD | grep -e '^.[A-Z]\+-[0-9]\+' | sort -u` can be used to grab all commits with Jira-like names since the last tag
4. Run `mvn -DautoVersionSubmodules=true release:clean release:prepare` and follow the interactive instructions:
   - Ensure all snapshot dependencies are resolved (unless the workflow has [allow-snapshots-release](#configuration-allow-snapshots-release) enabled),
   - Use the format `vX.Y.Z` for the created tag,
   - Set the new development version by:
     - Incrementing the **minor** version for regular releases (`X.Y+1.0`) or
     - Incrementing the **patch version** for bugfix releases (`X.Y.Z+1`);
5. Push the test branch to GitHub and create a pull request against the mainline branch;
6. Once the PR passes, merge the pull request (do _not_ use a squash commit — merge the full release branch history) and push the tag (`git push --tags`);
7. Wait for the tag's GitHub Actions build to run (you can find it in the list under the `Actions` tab — look for the middle column specifying the tag's name);
8. Announce it to the world:
   - Create a release on GitHub using the tag already pushed; the description should be the same as the entries in `NEWS.md` and `latest` should be set if applicable;
   - Send an annoucement to [#folio-releases on Slack](https://open-libr-foundation.slack.com/archives/CGPMHLX9B);
   - Ensure all applicable Jira tickets were given the proper `Fix version`; and
   - Mark the Jira version as released and create a new one; and
9. Prepare for future development locally by running `mvn release:clean`.

### Release procedures FAQ

<details>
  <summary><strong>Can't use Maven's release plugin due to failing tests?</strong></summary>

  If you are unable to use the Maven release plugin due to test issues (e.g. unable to run tests on your machine's architecture), you may skip tests with the following command:
  ```sh
  mvn -DskipTests -Darguments=-DskipTests -DautoVersionSubmodules=true release:clean release:prepare
  ```
</details>

<details>
  <summary><strong>Don't want to use Maven's release plugin whatsoever?</strong></summary>

  If you don't want to use the release plugin, you may perform its steps manually. Instead of running step 3 manually, do the following (and then resume the normal release procedure):
  1. Resolve all snapshot dependencies, remove the `-SNAPSHOT` from the POM's current version, and set the source control's `<scm><tag>` to the current `vX.Y.Z` (see [this example](https://github.com/folio-org/mod-lists/pull/265/changes/b00c3820f01f741f22c94bd21a703e357883ff95));
  2. Commit these changes to your branch and create a tag `vX.Y.Z`;
  3. Restore snapshot dependencies as applicable, restore the source control's tag to `HEAD`, and set the POM's version to the next snapshot; and
  4. Commit these changes as a separate commit.
</details>

<details>
  <summary><strong>Doing a hotfix to an older branch of your repository that still uses Jenkins?</strong></summary>

  You have two options if you need to release on an older branch that does not use the new GitHub Actions workflow.

  However note that Option 1 is preferred because Jenkins might go away soon.

  1. Migrate the branch to GitHub Actions (see [Usage](#usage)); or
  2. Use Jenkins for the release.

  If using Jenkins, everything will be the same except step six. Instead, navigate to the tag's build page at `https://jenkins-aws.indexdata.com/job/folio-org/job/mod-MY-MODULE/view/tags/job/vX.Y.Z/` and click `Build now` in the sidebar. Once this is complete, resume the normal release procedure.
</details>

> [!NOTE]
> 
> Skipping local test execution (in the plugin or by bypassing the plugin entirely) will only skip tests locally — tests still **must** pass in GitHub Actions for the release to proceed.

## Limitations

### Only top-level Dockerfile

At this stage only a top-level Dockerfile is utilised. So these Workflows are not yet ready for projects that have lower-level Dockerfile.

## Oddities

### Timeout at ModuleDescriptor registry

Occasionally the job to "Publish ModuleDescriptor" gets a timeout at the registry.

In this case the Docker image would be published but not the associated ModuleDescriptor.

Do "dispatch" the workflow again to publish a new Docker image and ModuleDescriptor.
