---
layout: page
title: How to get started with Rancher environment
titleLeader: "FAQ |"
menuTopTitle: Guides
categories: development-tips
faqOrder: 9
---

## Introduction
Rancher is Kubernetes managment tool.
Folio rancher main URL https://rancher.dev.folio.org
Default dev. cluster: "folio-eks-2-us-west-2".
Basic OKAPI URL: https://<Project name>.ci.folio.org:80

## Logging in
You have to be a member of Folio organzition Team to have access to Rancher.
Go to main Rancher URL and log-in with GitHub account.
Select thet default Cluster and your Project.

## Project description
Every project has own Postgres, OKAPI, pre-installed core backends modules (and Stripes UI - under consruction).
Also every Project runs Prometeuth and Kafka.
Folio modules are installed from [Folio Helm repository](https://github.com/folio-org/folio-helm).
Postgres and Kafka are installed from Bitnami Helm repository.

## Running and building modules
By default backend modules are pulled from DockerHub/folioci repository with a 'latest' tag.
But you can build your own module and automatically deploy it with Rancher pipeline and Helm.
Please use [this pipeline](https://github.com/folio-org/mod-pubsub/blob/master/.rancher-pipeline.yml) for get started.

## Registering modules in OKAPI
Module registration runs automatically after install or upgrade procedure.
Helm uses post-install and post-upgrade hooks to run module registration job for each module.
Helm gets descriptor from 'http://folio-registry.aws.indexdata.com (latest master branch snapshot descriptor).
Default steps for module registration:
* Pushing module descriptor
* Pushing module deployment
* Creating tenant (default 'diku')
* Enabling module for tenant

## Environment variables
Environment variables storing in Kubernetes secrets (Workload -> Secrets) and installed byr default to every Project.

## Limitatons
No OKAPI securing provided.
Stripes UI deployment is under constuction.
