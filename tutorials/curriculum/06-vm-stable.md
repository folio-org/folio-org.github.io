---
layout: page
title: Interact with a FOLIO stable VM
permalink: /tutorials/curriculum/06-vm-stable/
menuInclude: yes
menuLink: yes
menuTopTitle: Tutorials
---

The previous lessons have provided a quick overview of deploying parts of the system, and doing some minimal configuration.

This Lesson uses a stable virtual machine (VM) to provide a prepared FOLIO system.
It has all the necessary modules deployed, and users and items already loaded.

If you still have the VirtualBox guest running from the previous lessons, then change to the folio-curriculum directory and do: `vagrant halt; cd ..`

# Start the VM

Do this step prior to attending a workshop, as it will take some time.

Prepare the box. It will sit beside your other halted folio-curriculum box.

1. Make a clean directory and change into it: `mkdir folio-stable && cd folio-stable`
1. Initialise the Vagrantfile: `vagrant init --minimal folio/Q3-2018`
1. Launch the VirtualBox guest: `vagrant up`
1. Connect to the VirtualBox guest: `vagrant ssh`

The [folio-ansible](https://github.com/folio-org/folio-ansible) notes explain the purpose of the various boxes, [show](https://github.com/folio-org/folio-ansible/blob/master/doc/index.md) how to explore a system, view the Okapi logs and Stripes logs, find the box version information and release notes, and [troubleshooting](https://github.com/folio-org/folio-ansible/blob/master/doc/index.md#troubleshootingknown-issues) notes.

# Follow the log files

Open a couple more shell terminal windows to follow the Okapi and Stripes log files.

Following these log files is [explained](https://github.com/folio-org/folio-ansible/blob/master/doc/index.md#viewing-the-okapi-log), as well as how to follow the log of each backend module.

```shell
$ cd folio-stable
$ vagrant ssh
$ tail -f /var/log/folio/okapi/okapi.log
```

```shell
$ cd folio-stable
$ vagrant ssh
$ docker logs stripes_stripes_1 --follow
```

# Interact via web browser

Remember that the Stripes service is forwarded through port 3000, so we can interact with it from the host machine using the local web browser.

`open http://localhost:3000`

Admin login: diku_admin/admin

The Settings section shows the system information and software versions for the interfaces, services, and dependencies.

Browse and view the Users and Inventory sections.

# Interact via curl

Open a couple more shell terminal windows to send requests via command-line clients.

Remember that the Okapi service is forwarded through port 9130, so we can interact with it from the host machine using 'curl' (or 'httpie' or 'postman').

Save the following script as `run-basic.sh` in your work directory. It provides a basic interaction with Okapi.

Expand this later to do some other queries.
The [API docs](/reference/api/) will be useful.
The [CQL docs](/reference/glossary/#cql) will explain the Contextual Query Language (CQL) used by FOLIO.

So start talking, do: `./run-basic.sh`

```shell
#!/bin/bash

# Run some queries.

OKAPIURL="http://localhost:9130"
CURL="curl -w\n -D - "
PATH_TMP="/tmp/folio-demo"

H_TENANT="-HX-Okapi-Tenant:diku"
H_JSON="-HContent-type:application/json"

echo Ensuring that Okapi can be reached ...
$CURL $OKAPIURL/_/proxy/tenants
STATUS=$?
if [ $STATUS != 0 ]; then
  echo "Cannot contact Okapi: $STATUS"
  exit
fi
echo

echo Doing login and getting our token ...
cat >$PATH_TMP-login-credentials.json << END
{
  "userId": "diku_admin",
  "password": "admin"
}
END

$CURL $H_TENANT $H_JSON --progress-bar \
  -X POST \
  -d@$PATH_TMP-login-credentials.json \
  $OKAPIURL/authn/login > $PATH_TMP-login-response.json

echo Extracting the token header from the response ...
H_TOKEN=-H`grep -i x-okapi-token "$PATH_TMP-login-response.json" | sed 's/ //' `

# echo Received a token $H_TOKEN
echo

echo Test 1: Find some users
$CURL $H_TENANT $H_TOKEN \
  $OKAPIURL/users?query=personal.lastName==ab*+sortBy+username
echo

echo Finished.
```

