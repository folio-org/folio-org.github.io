---
layout: page
title: Create workspace and launch the VM
permalink: /tutorials/folio-vm/01-create-workspace/
menuInclude: yes
menuLink: yes
menuTopTitle: Tutorials
---

This lesson will establish the local workspace, explain how to launch the box, how to know when it is ready for interaction, how to shut it down, and how to keep it up-to-date.

## Create local workspace

Make a fresh directory and change into it:

```
mkdir vm-release-core && cd vm-release-core
```

Initialise the Vagrantfile:

```
vagrant init --minimal folio/release-core
```

That setup was a once-off task.

Any file that is placed in this directory on the host system
will be shared on the guest at the /vagrant mount point.

## Launch the guest

Launch the VirtualBox guest:

```
vagrant up
```

The output will show the VM starting.
(If this is the first launch then the box will be downloaded, which will take some time.)
When the command prompt is returned, then the system will be ready to inspect.

**However wait a while** before attempting to interact, because Okapi will still be starting modules.

Some ports of the guest will be forwarded to the host, so that the FOLIO system can be reached from the outside.
Okapi will be listening on localhost port 9130, and the Stripes development server will be on localhost port 3000.

## Connect to the guest

In a terminal window on the host, connect to the VirtualBox guest:

```
vagrant ssh
```

Follow the [Okapi logfile](/tutorials/folio-vm/02-system-overview/#okapi-log)
to determine when the system is ready for interaction.

When Okapi pauses occasionally and shows bursts of "Timer" tasks, then it should be ready for interaction.

## Quick visit to UI

Use the local web browser to login to the user interface at `localhost:3000`\
The default administrative user is `diku_admin/admin`

Inspect the Settings page to find the version of Okapi, and the installed modules:\
`http://localhost:3000/settings/about`

**Note**: If errors are presented, then you probably did not wait long enough.
Do logout, wait, and then log in again.

## Halt and rest

Okay, that is enough fun.
Now we are going to get out, and show how to halt and update the box.

Do '`Ctrl-C`' to stop following the logfile.

Get out of the VM guest and return to the host. Do '`exit`'

Now put the system to rest with '`vagrant halt`'

When ready to recommence, simply do '`vagrant up`'

## Update the box

As explained in the [background overview](../overview/#background) section, the FOLIO VMs are regularly rebuilt with the current state of development.

The local system does not need to be updated every day, but when desired then do:\
'`vagrant halt`' and then '`vagrant box update`'
(followed by '`vagrant destroy`' to disable the old default machine).

The Vagrant box can then be launched again with '`vagrant up`'

## Destroy when finished

When finished with exploration, do '`vagrant destroy`' to reclaim disk space and keep your vagrant tidy.

When ready to use it again, then do '`vagrant up`' again.
Of course, if you had done additional configuration to the default system or loaded extra data or other modules, then that would need to be repeated.

For further assistance with Vagrant and management of virtual environments, see the HashiCorp Learn tutorials.
For example additional [notes](https://learn.hashicorp.com/tutorials/vagrant/getting-started-teardown) about suspend, halt, destroy.

---
Next lesson: [VM system overview](../02-system-overview/)

