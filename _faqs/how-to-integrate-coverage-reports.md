---
layout: page
title: How to integrate code coverage reports with SonarQube
titleLeader: "FAQ |"
menuTopTitle: Guides
categories: development-tips
faqOrder: 10
---

## Introduction

During continuous integration builds, the FOLIO Jenkins will gather the generated coverage reports and send them to [SonarCloud](https://sonarcloud.io/organizations/folio-org) for analysis.

## Front-end modules

For front-end JavaScript-based modules, the SonarQube scanner "sonar-scanner" is utilised.

The project's Jenkinsfile requires the setting: `runSonarqube = true`

(See notes for [initial configuration](/guidelines/create-new-repo/#frontend-specific) of a new front-end repository.)

A specific set of filesystem paths are [excluded](https://github.com/folio-org/jenkins-pipeline-libs/blob/master/vars/sonarqubeScanNPM.groovy#L15) by the scanner.
That covers most situations -- send a pull-request if more are needed.

The project's testing framework will generate the code coverage reports, and the sonar-scanner will look for them in these filesystem locations:

* `./artifacts/coverage/lcov.info`
* `./coverage/lcov.info`

Note that it is possible for a UI project to use two separate testing frameworks.
Configure the tools so that each one generates their report into one of those separate directories.
The SonarCloud facility will analyse and merge the reports.

## Back-end modules

For back-end Maven-based modules, the SonarQube scanner "sonar-maven-plugin" will utilise JaCoCo to generate the code coverage reports.

No additional configuration is required in the project's Jenkinsfile.

(See notes for [initial configuration](/guidelines/create-new-repo/#backend-specific) of a new back-end repository.)

## Further information

* [Code analysis and linting facilities](/guides/code-analysis/#sonarqube) including notes about rule customization.

<div class="folio-spacer-content"></div>

