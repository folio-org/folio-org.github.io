---
layout: page
title: Create workspace and launch the VM
permalink: /tutorials/folio-vm/01-create-workspace/
menuInclude: yes
menuLink: yes
menuTopTitle: Tutorials
---

This lesson will establish the local workspace, and explain how to launch the box and shut it down, and how to keep it up-to-date.

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
When the command prompt is returned, then the system will be ready to inspect.
**However wait a few minutes** because Okapi will still be starting modules.

Some ports of the guest will be forwarded to the host, so the FOLIO system can be reached from the outside.

Okapi will be listening on localhost port 9130, and the Stripes development server will be on localhost port 3000.

## Quick visit

Use the local web browser to login to the UI at `localhost:3000`<br/>
The default administrative user is `diku_admin/admin`

Inspect the Settings page to find the version of Okapi, and the installed modules:<br/>
`http://localhost:3000/settings/about`

Send an initial request directly to Okapi:

```
curl -s -S -w'\n' http://localhost:9130/_/version
```

## Connect to the guest

In a terminal window on the host, connect to the VirtualBox guest:

```
vagrant ssh
```

Briefly inspect the [Okapi logfile](/tutorials/folio-vm/02-system-overview/#okapi-log).

Okay, that is enough fun.
Now we are going to get out, and show how to halt and update the box.

```
exit
```

## Halt and rest

Now put the system to rest with `vagrant halt`

When ready to recommence, simply do `vagrant up`

## Update the box

As explained in the [background overview](../overview/#background) section, the FOLIO VMs are rebuilt each day with the current state of development.

The local system does not need to be updated every day, but when desired then do:<br/>
`vagrant box update`
(followed by `vagrant destroy` to disable the old default machine).

The Vagrant box can then be launched again with `vagrant up`

---
Next lesson: [VM system overview](../02-system-overview/)

