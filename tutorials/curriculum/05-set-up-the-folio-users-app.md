---
layout: page
title: Set up the FOLIO Users app
permalink: /tutorials/curriculum/05-set-up-the-folio-users-app/
menuInclude: yes
menuLink: yes
menuTopTitle: Tutorials
---
<div class="attention">
Note: This is an older tutorial. Much of it is still useful, but some parts are out-of-date.
In particular, you may see errors in the browser console.
See <a href="https://issues.folio.org/browse/FOLIO-2035">FOLIO-2035</a>.
</div>

In lesson four, we deployed Stripes and demonstrated communication between the browser and the Stripes components.
In lessons two and three, we deployed the Okapi Gateway as well as a test Okapi Module and examined the communication between them.
In this lesson five, we are connecting Stripes to the Okapi Gateway and adding the Users app.

There are two components to the Users app: the Stripes UI component and the Okapi Module component.
We will start first with the Stripes UI component.

## Add the Users app UI component to the Stripes UI Server
Remember in $FOLIO_ROOT/stripes-tutorial-platform we have two configuration files: `package.json` and `stripes.config.js`.
Each will need changes to add the Users app
[ui-users](https://github.com/folio-org/ui-users).

### Modify _package.json_
The `package.json` file needs a new entry in the dependency section.
The revised file should look like:
```JavaScript
{
  "scripts": {
    "build": "stripes build stripes.config.js",
    "stripes": "stripes",
    "start": "stripes dev stripes.config.js"
  },
  "dependencies": {
    "@folio/stripes": "^1.0.0",
    "@folio/users": "^2.17.0",
    "@folio/trivial": "^1.2.0",
    "react": "^16.3.0"
  }
}
```

### Modify _stripes.config.js_
The `stripes.config.js` file needs not only a line for adding the Users UI component; it also needs connection information for the Okapi Gateway.
```javascript
module.exports = {
  okapi: { 'url':'http://localhost:9130', 'tenant':'testlib' },
  config: { disableAuth: true, hasAllPerms: true, reduxLog: true },
  modules: {
    '@folio/trivial': {},
    '@folio/users': {}
  }
};
```

The `okapi` line in `stripes.config.js` gives the Stripes UI Server the URL of the Okapi gateway and the name of the tenant being used by this UI Server instance.

### Rebuild Stripes Server
With the Users UI components added to the UI Server configuration, use the `yarn install` command to download and configure the necessary modules.

<div class="vagrant-note" markdown="1">
When using the VirtualBox method, you will need to open a terminal window on your host computer, change the working directory to the location of the `Vagrantfile`, and use the `vagrant ssh` command to connect from the host computer to the guest.

When starting Stripes from the command line, be sure to set the _STRIPES_HOST_ environment variable: `STRIPES_HOST=0.0.0.0 yarn start`
</div>

```shell
$ cd $FOLIO_ROOT/stripes-tutorial-platform
$ yarn install
  yarn install v1.12.3
  warning No license field
  [1/4] 🔍  Resolving packages...
  [2/4] 🚚  Fetching packages...
  [3/4] 🔗  Linking dependencies...
  [4/4] 📃  Building fresh packages...
  success Saved lockfile.
  ✨  Done in 12.12s.

$ yarn start
  yarn start v1.12.3
  $ stripes dev stripes.config.js
  Listening at http://localhost:3000
  webpack built 97b8243748d40fd3a9c1 in 14004ms
```

The Stripes portion of the Users app is now running at  [http://localhost:3000/users](http://localhost:3000/users)

At this point there might be an error, similar to these, which indicate that some bits were missed in previous steps:
* `ERROR: in module @folio/users operation FETCH on resource users failed, saying: Network request failed`: the Okapi Gateway is not running; see the Java command line at the [start of lesson three](../02-initialize-okapi-from-the-command-line#start-the-okapi-gateway)
* `ERROR: in module @folio/users operation FETCH on resource users failed, saying: No such Tenant testlib`: your Okapi Gateway is newly restarted and does not have the _testlib_ tenant; return to [lesson three under the Creating a Tenant heading](../02-initialize-okapi-from-the-command-line#creating-a-tenant) to post `okapi-tenant.json` to `/_/proxy/tenants`.

Otherwise there will be an expected error, similar to:
* `ERROR: in module @folio/users, operation GET on resource 'patronGroups' failed, saying: No suitable module found for path /groups`

You are in the right place. The Users back-end module is not yet enabled for the 'testlib' tenant.

## Add the Users app Okapi Module to the Okapi Gateway

### Fetch and build the Users app Okapi Module

```shell
$ cd $FOLIO_ROOT
$ git clone --recursive https://github.com/folio-org/mod-users.git
  Cloning into 'mod-users' ...
  [...]

$ cd mod-users
$ mvn install
  [...]
  [INFO] BUILD SUCCESS
  [...]
```

### Register and Deploy the Users app Okapi Module

As part of that build process, the mod-users ModuleDescriptor and DeploymentDescriptor were generated into the "target" directory. They can be used to register and deploy the Users app Okapi Module.

```shell
$ cd $FOLIO_ROOT
$ curl -i -w '\n' -X POST -H 'Content-type: application/json' \
   -d @mod-users/target/ModuleDescriptor.json \
   http://localhost:9130/_/proxy/modules

  HTTP/1.1 100 Continue

  HTTP/1.1 201 Created
  Content-Type: application/json
  Location: /_/proxy/modules/mod-users-15.3.0-SNAPSHOT
  X-Okapi-Trace: POST okapi-2.16.2-SNAPSHOT /_/proxy/modules : 201 17253us
  Content-Length: 7526

  {
    "id" : "mod-users-15.3.0-SNAPSHOT",
    "name" : "users",
   ...
   ...
  }
```

You will also need to deploy the module with a Deployment Descriptor:

```shell
$ curl -i -w '\n' -X POST -H 'Content-type: application/json' \
   -d @mod-users/target/DeploymentDescriptor.json \
   http://localhost:9130/_/discovery/modules

  HTTP/1.1 201 Created
  Content-Type: application/json
  Location: /_/discovery/modules/mod-users-15.3.0-SNAPSHOT/cfa31663-b4d5-4072-8159-7f51db65fa49
  X-Okapi-Trace: POST okapi-2.16.2-SNAPSHOT /_/discovery/modules : 201 14247975us
  Content-Length: 280

  {
    "instId" : "cfa31663-b4d5-4072-8159-7f51db65fa49",
    "srvcId" : "mod-users-15.3.0-SNAPSHOT",
    "nodeId" : "localhost",
    "url" : "http://localhost:9133",
    "descriptor" : {
      "exec" : "java -jar ../mod-users/target/mod-users-fat.jar -Dhttp.port=%p embed_postgres=true"
    }
  }
```

(Note: Your port number in the `instId` and the `url` may vary depending on whether there are other Okapi Modules deployed on the Okapi Gateway.)
Finally, you'll need to enable the Okapi Users app module for the test tenant.

Note: The version of mod-users that was deployed in the previous step may be different to that shown in this document. So update the version in this next step to match that:

```shell
$ cat > okapi-enable-users.json <<END
{
  "id" : "mod-users-15.3.0-SNAPSHOT"
}
END
$ curl -i -w '\n' -X POST -H 'Content-type: application/json' \
   -d @okapi-enable-users.json \
   http://localhost:9130/_/proxy/tenants/testlib/modules

HTTP/1.1 201 Created
Content-Type: application/json
Location: /_/proxy/tenants/testlib/modules/mod-users-15.3.0-SNAPSHOT
X-Okapi-Trace: POST okapi-2.16.2-SNAPSHOT /_/proxy/tenants/testlib/modules : 201 1713441us
Content-Length: 40

{
  "id" : "mod-users-15.3.0-SNAPSHOT"
}
```

Ensure that the mod-users module is properly enabled for our test tenant:

```shell
$ curl -i -w '\n' -X GET http://localhost:9130/_/proxy/tenants/testlib/modules
```

## Add users to FOLIO

For testing purposes, the FOLIO development team has JSON documents representing factitious users that can be used to populate the dev FOLIO environment.

```shell
$ cd $FOLIO_ROOT
$ cat > User001.json <<END
{
  "username" : "elyssa",
  "id" : "90f2c933-ea1e-4b17-a719-b2af6bacc735",
  "active" : true,
  "type" : "patron",
  "personal" : {
    "email" : "cordie@carroll-corwin.hi.us",
    "phone" : "791-043-4090 x776",
    "lastName" : "Ferry",
    "firstName" : "Liliane"
  },
  "meta": {
    "creation_date": "2016-11-05T0723",
    "last_login_date": ""
  }
}
END
$ cat > User002.json <<END
{
  "username" : "kody",
  "id" : "6149c8d7-ae2f-4a64-8b39-4e39f743d675",
  "active" : true,
  "type" : "patron",
  "personal" : {
    "email" : "mireille@kihn-dickinson.ki",
    "phone" : "594.070.0052",
    "lastName" : "Collins",
    "firstName" : "Courtney"
  },
  "meta": {
    "creation_date": "2016-11-05T0723",
    "last_login_date": ""
  }
}
END
$ curl -i -w '\n' -X POST -H 'Content-type: application/json' \
    -H 'X-Okapi-Token: dummyJwt.eyJzdWIiOiJzZWIiLCJ0ZW5hbnQiOm51bGx9.sig' \
    -H 'X-Okapi-Tenant: testlib' -d @User001.json \
    http://localhost:9130/users

HTTP/1.1 201 Created
X-Okapi-Trace: POST test-auth-3.4.1 http://localhost:9132/users : 202 5008us
Content-Type: application/json
Location: 373a7d26-f44f-4906-be44-0fba4a9aba44
host: localhost:9130
user-agent: curl/7.55.1
accept: */*
x-okapi-tenant: testlib
x-okapi-request-id: 760349/users
x-okapi-url: http://localhost:9130
x-okapi-permissions-required: users.item.post
x-okapi-module-permissions: {}
x-okapi-user-id: seb
x-okapi-token: dummyJwt.eyJzdWIiOiJzZWIiLCJ0ZW5hbnQiOm51bGx9.sig
X-Okapi-Trace: POST mod-users-15.3.0-SNAPSHOT http://localhost:9133/users : 201 315514us
Transfer-Encoding: chunked

{
  "username" : "elyssa",
  "id" : "90f2c933-ea1e-4b17-a719-b2af6bacc735",
  "active" : true,
  "type" : "patron",
  "meta" : {
    "creation_date" : "2016-11-05T0723",
    "last_login_date" : ""
  },
  "proxyFor" : [ ],
  "personal" : {
    "lastName" : "Ferry",
    "firstName" : "Liliane",
    "email" : "cordie@carroll-corwin.hi.us",
    "phone" : "791-043-4090 x776",
    "addresses" : [ ]
  },
  "createdDate" : "2017-10-10T07:57:00.463+0000",
  "updatedDate" : "2017-10-10T07:57:00.463+0000"
}

$ curl -i -w '\n' -X POST -H 'Content-type: application/json' \
    -H 'X-Okapi-Token: dummyJwt.eyJzdWIiOiJzZWIiLCJ0ZW5hbnQiOm51bGx9.sig' \
    -H 'X-Okapi-Tenant: testlib' -d @User002.json \
    http://localhost:9130/users

HTTP/1.1 201 Created
X-Okapi-Trace: POST test-auth-3.4.1 http://localhost:9132/users : 202 2245us
Content-Type: application/json
Location: 904d2c0a-6db0-446a-9fde-47a601919205
host: localhost:9130
user-agent: curl/7.55.1
accept: */*
x-okapi-tenant: testlib
x-okapi-request-id: 439874/users
x-okapi-url: http://localhost:9130
x-okapi-permissions-required: users.item.post
x-okapi-module-permissions: {}
x-okapi-user-id: seb
x-okapi-token: dummyJwt.eyJzdWIiOiJzZWIiLCJ0ZW5hbnQiOm51bGx9.sig
X-Okapi-Trace: POST mod-users-15.3.0-SNAPSHOT http://localhost:9133/users : 201 315514us
Transfer-Encoding: chunked

{
  "username" : "kody",
  "id" : "6149c8d7-ae2f-4a64-8b39-4e39f743d675",
  "active" : true,
  "type" : "patron",
  "meta" : {
    "creation_date" : "2016-11-05T0723",
    "last_login_date" : ""
  },
  "proxyFor" : [ ],
  "personal" : {
    "lastName" : "Collins",
    "firstName" : "Courtney",
    "email" : "mireille@kihn-dickinson.ki",
    "phone" : "594.070.0052",
    "addresses" : [ ]
  },
  "createdDate" : "2017-10-10T07:58:51.452+0000",
  "updatedDate" : "2017-10-10T07:58:51.452+0000"
}
```

Be satisfied that those users were added:

```
$ curl -i -X GET -H "Content-Type:application/json" \
    -H 'X-Okapi-Token: dummyJwt.eyJzdWIiOiJzZWIiLCJ0ZW5hbnQiOm51bGx9.sig' \
    -H "X-Okapi-Tenant:testlib" \
    http://localhost:9130/users
```

## Show insufficient authentication

Visit the FOLIO Users app at [http://localhost:3000/users](http://localhost:3000/users)

* `ERROR: in module @folio/users, operation GET on resource 'patronGroups' failed, saying: test-auth: check called without X-Okapi-Token`

That is correct. Remember that in the previous [Lesson 3](../03-enable-okapi-authentication/) we only illustrated authentication.
With our command-line curl queries we are using a dummy token.

Stop both Okapi and Stripes with `Control-C`

The lessons so far have demonstrated how all of the pieces work together.

Move on to the next [Lesson 6](../06-vm-stable/) which uses a quarterly release of FOLIO as a Vagrant box,
with all necessary modules enabled, and a more useful set of users and other data loaded.
