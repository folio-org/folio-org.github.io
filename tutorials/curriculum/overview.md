---
layout: page
title: FOLIO Developer Curriculum - Overview
permalink: /tutorials/curriculum/overview/
menuInclude: yes
menuLink: yes
menuTopTitle: Tutorials
---

This is an outline of a tutorial that can be given to a group in a workshop or followed by an individual developer in a self-paced fashion.

<div class="attention">
Note: This is an older tutorial. Much of it is still useful, but some parts are out-of-date.
See <a href="https://issues.folio.org/browse/FOLIO-1348">FOLIO-1348</a>.
</div>

## Goals
* Set up a running instance of the Stripes Development UI Server
* Set up a running instance of Okapi Gateway
* Demonstrate how to deploy an Okapi Module to a tenant in Okapi Gateway and the Stripes UI Server
* Understand how Okapi Gateway routes requests to modules

## System Requirements
There are two choices: either running the Stripes Development UI Server and the Okapi Gateway directly on a developer’s machine (“on-machine”) or running Stripes and Okapi in a VirtualBox guest.
An Ansible playbook with appropriate roles is used to create the VirtualBox guest, and can also be used to automatically build a developer’s environment (making the playbook target localhost).

* macOS 10.? or higher (On-machine or VirtualBox)
* Windows 10 or higher (VirtualBox required)
* Linux (On-machine or VirtualBox)

## Prerequisites
Before attending the workshop, participants must meet these requirements.
When in doubt, using the VirtualBox guest machine is recommended.

### On-Machine
* Java: [8u101](/guides/troubleshooting#missing-certificate-authority-for-lets-encrypt) or higher.
* Maven 3.3.9 or higher
* Node.js 6.x or higher
* [Yarn](https://yarnpkg.com/en/) package manager v0.20.3 or higher
* [curl](https://curl.haxx.se)

### VirtualBox guest
* [VirtualBox 5.1 or higher](https://www.virtualbox.org/wiki/Downloads)
* [Vagrant 1.9.1 or higher](https://www.vagrantup.com/downloads.html), for Windows 7 use [1.9.6 .msi](https://releases.hashicorp.com/vagrant/1.9.6/) ([learn why](https://github.com/hashicorp/vagrant/issues/8783))

To download the VirtualBox guest:
1. Make a clean directory and change into it: `mkdir folio-curriculum && cd folio-curriculum`
1. Set up the Vagrantfile: `vagrant init --minimal folio/curriculum`
1. Launch the VirtualBox guest: `vagrant up`
1. Connect to the VirtualBox guest: `vagrant ssh`

Note: Do this download prior to attending a workshop.
If also doing [Lesson 6](../06-vm-stable) then get it ready beforehand too.

<div class="vagrant-note" markdown="1">
In subsequent lessons, the command lines are executed within the VirtualBox guest.
Be sure you are connected to the VirtualBox guest (from the host computer: `vagrant ssh`) before running the commands.

Other instructions and commands that are specific to the VirtualBox guest mode of using the tutorial are noted using this style of information box.

There are some FOLIO-related Vagrant tips, known issues, and troubleshooting [notes](https://github.com/folio-org/folio-ansible/blob/master/doc/index.md#troubleshootingknown-issues) available.
</div>

<div class="vagrant-on-windows-note" markdown="1">
If launching Vagrant from a Windows Command Prompt, be sure to use _Run As Administrator..._ when opening the Command Prompt itself (`cmd.exe`).  If you are seeing the error _"EPROTO: protocol error, symlink"_, the likely cause is that Vagrant was not launched with administrator privileges.  See issue [STRIPES-344](https://issues.folio.org/browse/STRIPES-344) for details.
</div>

## Set `FOLIO_ROOT` Variable for Lessons
Each lesson assumes the existence of a `$FOLIO_ROOT` shell variable.
This variable holds the path to a directory where the components of the Okapi Server and the Stripes Development UI Server are located.

<div class="vagrant-note" markdown="1">
If using the VirtualBox guest setup, it is recommended to first `cd /vagrant` before creating the empty directory. Doing so makes the Okapi and Stripes files available from the host operating system in the same directory the Vagrantfile file is located.

The first command below connects from the VirtualBox host to the VirtualBox guest.
The second command changes the working directory to the shared `vagrant` directory.

```shell
$ vagrant ssh
$ cd /vagrant
```
</div>

Create the directory, enter the directory, and save the directory location using these commands:

```shell
$ mkdir folio-tutorial-working-files
$ cd folio-tutorial-working-files
$ export FOLIO_ROOT=`pwd`
```

Each time that you open a new shell terminal window, do those latter two steps to set `$FOLIO_ROOT`.

## Lessons/Steps
1. [Clone, build and explore Okapi](../01-clone-build-and-explore-okapi)
1. [Initialize Okapi Gateway from the command line](../02-initialize-okapi-from-the-command-line)
1. [Enable Okapi Authentication](../03-enable-okapi-authentication)
1. [Deploy test Stripes package](../04-deploy-test-stripes-module)
1. Real-world application: [set up the FOLIO Users app](../05-set-up-the-folio-users-app)
1. [Interact with a FOLIO stable VM](../06-vm-stable)

