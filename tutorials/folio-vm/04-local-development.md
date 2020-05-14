---
layout: page
title: Conduct local development
permalink: /tutorials/folio-vm/04-local-development/
menuInclude: yes
menuLink: yes
menuTopTitle: Tutorials
---

This lesson introduces some ways to do local development using this VM.

## Front-end development

As explained earlier in this tutorial, the [Stripes CLI](../03-interact#interact-via-stripes-cli) is your friend.

Refer to the [Stripes CLI User Guide](https://github.com/folio-org/stripes-cli/blob/master/doc/user-guide.md).

## Back-end development

It is possible to make a back-end module service that is running on your host system available to the Okapi system running in the Vagrant VM.

The separate document [Running backend modules on your host system](https://github.com/folio-org/folio-ansible/blob/master/doc/index.md#running-backend-modules-on-your-host-system) explains the configuration.

## Module dependency graph

To determine dependencies of a certain module, following this technique.

Create a new tenant with nothing installed, then simulate installation of the module in question, to show what other modules that it would require to be installed.

```shell
#!/usr/bin/env bash

# install a fresh tenant and show dependency graph

MODULE=${1:-"mod-inventory"}

TENANT="depgraph"

OKAPIURL="http://localhost:9130"
CMD_CURL="curl"
CURL="$CMD_CURL -w\n -D - "
PATH_TMP="/tmp/folio-depgraph"

H_TENANT="-HX-Okapi-Tenant:$TENANT"
H_JSON="-HContent-type:application/json"

echo "Pulling updated ModuleDescriptors from registry ..."
$CURL $H_JSON -X POST \
  -d '{ "urls": [ "http://folio-registry.aws.indexdata.com" ] }' \
  $OKAPIURL/_/proxy/pull/modules

echo
echo "Initialise the tenant '$TENANT' ..."
cat >$PATH_TMP-tenant.json << END
{
  "id" : "$TENANT",
  "name" : "Dependency grapher"
}
END
${CMD_CURL} -s -S $H_JSON -X POST \
  -d @$PATH_TMP-tenant.json \
  $OKAPIURL/_/proxy/tenants

echo
echo "Enable Okapi internal module for tenant '$TENANT' ..."
${CMD_CURL} -s -S $H_JSON -X POST \
  -d '{"id":"okapi"}' \
  $OKAPIURL/_/proxy/tenants/$TENANT/modules

echo
echo "Get dependency graph for '$MODULE' ..."
cat >$PATH_TMP-enable.json << END
[{"id":"$MODULE","action":"enable"}]
END
${CMD_CURL} -s -S $H_JSON -X POST \
  -d @$PATH_TMP-enable.json \
  "$OKAPIURL/_/proxy/tenants/$TENANT/install?simulate=true"
echo
```

