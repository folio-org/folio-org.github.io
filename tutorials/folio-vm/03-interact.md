---
layout: page
title: Interact with the FOLIO VM
permalink: /tutorials/folio-vm/03-interact/
menuInclude: yes
menuLink: yes
menuTopTitle: Tutorials
---

This lesson shows some ways to interact with this FOLIO VM.

(**Note**: As explained in [Lesson 1](/tutorials/folio-vm/01-create-workspace/), if the VM is recently launched then **wait a while** because Okapi will still be starting modules.)

## Interact via web browser

Remember that the Stripes service is forwarded through port 3000, so we can interact with it from the host machine using the local web browser.

`open http://localhost:3000`

Admin login: diku_admin/admin

The Settings section shows the system information and software versions for the interfaces, services, and dependencies:\
`http://localhost:3000/settings/about`

Browse and view the Users and Inventory sections.

## Interact via Developer Settings

The UI Developer Settings section has various useful facilities.

`open http://localhost:3000/settings/developer`

Refer to explanation of some tools at [How to determine which module handles which interface and endpoint](/faqs/how-to-which-module-which-interface-endpoint/#ui-developer-settings).

## Interact via curl

Open a couple more shell terminal windows on the host system, to send requests via command-line clients.

Remember that the Okapi service is forwarded through port 9130, so we can interact with it from the host machine using 'curl' (or 'httpie' or 'postman').

```
curl -s -S -w'\n' http://localhost:9130/_/version
```

Save the following script as `run-basic.sh` in your home directory.

It provides only basic interaction with Okapi.

Expand this later to do some other queries.
The [API docs](/reference/api/) will be useful.
The [CQL docs](/reference/glossary/#cql) will explain the Contextual Query Language (CQL) used by FOLIO.
Also see various documentation [provided](/source-code/map/) for some modules.

So start talking, do: `./run-basic.sh`

```shell
#!/usr/bin/env bash

OKAPIURL="http://localhost:9130"
CURL="curl -w\n -D - "
PATH_TMP="/tmp/folio-tutorial"

H_TENANT="-HX-Okapi-Tenant:diku"
H_JSON="-HContent-type:application/json"

echo "Ensure that Okapi can be reached ..."
STATUS=$(curl -s -S -w "%{http_code}" $OKAPIURL/_/proxy/tenants -o /dev/null)
if [ "$STATUS" != "200" ]; then
  echo "Cannot contact okapi: $STATUS"
  exit
fi
VERSION_OKAPI=$(curl -s -S "$OKAPIURL/_/version")
echo "Using version ${VERSION_OKAPI}"
echo

echo "Do login and obtain our token ..."
cat >$PATH_TMP-login-credentials.json << END
{
  "username": "diku_admin",
  "password": "admin"
}
END

$CURL $H_TENANT $H_JSON --progress-bar \
  -X POST \
  -d@$PATH_TMP-login-credentials.json \
  $OKAPIURL/authn/login > $PATH_TMP-login-response.json

echo "Extract the token header from the response ..."
H_TOKEN=-H$(grep -i x-okapi-token "$PATH_TMP-login-response.json" | sed 's/ //')
echo
#echo Received a token: $H_TOKEN

echo "Test 1: Find some users"
$CURL $H_TENANT $H_JSON $H_TOKEN \
  "$OKAPIURL/users?query=personal.lastName==a*+sortBy+username"
echo

echo "Finished."
```

## Interact via Stripes CLI

The [Stripes CLI](https://github.com/folio-org/stripes-cli) command-line interface is an important tool for both front-end and back-end developers.

For example, after its installation and basic configuration, use it for concisely
[Observing Okapi requests](https://github.com/folio-org/stripes-cli/blob/master/doc/user-guide.md#observing-okapi-requests) to show what endpoints are called.

Of course there is much more that Stripes CLI can assist with your development.
Invest some time to become familiar.

## Load more data

Some sample data is already loaded with the default system.

There are various facilites to load more data via each app.
For example follow the links from documentation for
[ui-users](/source-code/map/#ui-users) and
[ui-inventory](/source-code/map/#ui-inventory) and
[ui-data-import](/source-code/map/#ui-data-import) etc.

---
Next lesson: [Conduct local development](../04-local-development/)

