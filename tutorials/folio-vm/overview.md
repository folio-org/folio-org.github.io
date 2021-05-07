---
layout: page
title: Using a FOLIO VM - Overview
permalink: /tutorials/folio-vm/overview/
menuInclude: yes
menuLink: yes
menuTopTitle: Tutorials
---

## Goals

* Explain how to utilise a FOLIO virtual machine (VM).

## Prerequisites

* [Vagrant](https://www.vagrantup.com/) -- Recent version.
* [VirtualBox](https://www.virtualbox.org/wiki/Downloads) --
Determine the version of VirtualBox to [match](https://www.vagrantup.com/docs/virtualbox) your version of `vagrant`.
* [curl](https://curl.haxx.se) -- Only curl commands are shown in this tutorial. (Those could be [utilised](https://learning.postman.com/docs/postman/collections/importing-and-exporting-data/) via [Postman](https://postman.com/). Easier to use [command line tools](/faqs/how-to-use-apis/) exist.)

## Background

Each night the FOLIO [reference environments](/guides/automation/#reference-environments) are rebuilt using the current state of development.

The continuous integration also constructs various Vagrant boxes.
These are [available](https://github.com/folio-org/folio-ansible/blob/master/doc/index.md#prebuilt-vagrant-boxes) to download for local use, providing a ready-to-run self-contained operating system environment and up-to-date FOLIO instance.

This tutorial will only focus on the `folio/snapshot-core` VM.

## Troubleshooting and known issues

There are [troubleshooting](https://github.com/folio-org/folio-ansible/blob/master/doc/index.md#troubleshootingknown-issues) notes in the folio-ansible repository, so generally those will not be repeated here.

## Lessons and steps

Follow each lesson sequentially:

1. [Create workspace and launch VM](../01-create-workspace/) and update box.
1. [VM system overview](../02-system-overview/) and viewing logfiles.
1. [Interact with the FOLIO VM](../03-interact/).
1. [Conduct local development](../04-local-development/).

