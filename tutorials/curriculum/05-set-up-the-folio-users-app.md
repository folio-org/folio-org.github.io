# Set up the Okapi Users app

In lesson four, we deployed Stripes and demonstrated communication between the browser and the Stripes components.
In lessons two and three, we deployed the Okapi Gateway as well as a test Okapi Module and examined the communication between them.
In this lesson five, we are connecting Stripes to the Okapi Gateway and adding the Users app.

There are two components to the Users app: the Stripes UI component and the Okapi Module component.
We will start first with the Stripes UI component.

NOTE: The Stripes package.json is out-of-date. Also we need the deployment of all user-related backend modules.

So skip ahead to the section about [Adding the mod-users module](#add-mod-users).

## Add the Users app UI component to the Stripes UI Server
Remember in $FOLIO_ROOT/stripes-tutorial-platform we have two configuration files: `package.json` and `stripes.config.js`.
Each will need changes to add the Users app.

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
    "@folio/stripes-core": "^1.6.0",
    "@folio/users": "^2.2.0",
    "@folio/trivial": "^0.0.2-test"
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
  yarn install v0.20.3
  warning No license field
  [1/4] 🔍  Resolving packages...
  [2/4] 🚚  Fetching packages...
  [3/4] 🔗  Linking dependencies...
  warning "eslint-import-resolver-webpack@0.8.1" has unmet peer dependency "eslint-plugin-import@>=1.4.0".
  [4/4] 📃  Building fresh packages...
  success Saved lockfile.
  ✨  Done in 12.12s.
$ yarn start
  yarn start v0.20.3
  $ stripes dev stripes.config.js
  Listening at http://localhost:3000
  webpack built 97b8243748d40fd3a9c1 in 14004ms
```

The Stripes portion of the Users app is now running at  [http://localhost:3000/users](http://localhost:3000/users).

At this point you likely receive a possible error, similar to:
* `ERROR: in module @folio/users operation FETCH on resource users failed, saying: Network request failed`: the Okapi Gateway is not running; see the Java command line at the [start of lesson three](http://dev.folio.org/curriculum/03_initialize_okapi_from_the_command_line#start-the-okapi-gateway)
* `ERROR: in module @folio/users operation FETCH on resource users failed, saying: No such Tenant testlib`: your Okapi Gateway is newly restarted and does not have the _testlib_ tenant; return to [lesson three under the Creating a Tenant heading](03_initialize_okapi_from_the_command_line#creating-a-tenant) to post `okapi-tenant.json` to `/_/proxy/tenants`.
* `ERROR: in module @folio/users operation FETCH on resource users failed, saying: ` (empty error message): you are in the right place.  The Users Okapi Module is not yet [registered](03_initialize_okapi_from_the_command_line#registering-okapi-test-module), [deployed](03_initialize_okapi_from_the_command_line#deploying-okapi-test-module) and/or [enabled](03_initialize_okapi_from_the_command_line#enable-test-module-for-the-testlib-tenant) for the 'testlib' tenant.  The lack of an error message is a [known issue](https://issues.folio.org/browse/STRIPES-224).

If you did not receive an error message, then your Okapi Gateway is properly configured.
The next tutorial section may be review.

## <a id="add-mod-users"/>Add the Users app Okapi Module to the Okapi Gateway

### Fetch and build the Users app Okapi Module

```shell
$ cd $FOLIO_ROOT
$ git clone --recursive https://github.com/folio-org/mod-users.git
  Cloning into 'mod-users'...
  remote: Counting objects: 645, done.
  remote: Compressing objects: 100% (41/41), done.
  remote: Total 645 (delta 9), reused 0 (delta 0), pack-reused 595
  Receiving objects: 100% (645/645), 88.87 KiB | 0 bytes/s, done.
  Resolving deltas: 100% (201/201), done.
  Submodule 'raml-util' (https://github.com/folio-org/raml.git) registered for path 'raml-util'
  Cloning into '/Users/peter/code/folio-trial/mod-users/raml-util'...
  remote: Counting objects: 409, done.
  remote: Compressing objects: 100% (7/7), done.
  remote: Total 409 (delta 2), reused 0 (delta 0), pack-reused 397
  Receiving objects: 100% (409/409), 85.73 KiB | 0 bytes/s, done.
  Resolving deltas: 100% (238/238), done.
  Submodule path 'raml-util': checked out 'b8dcdf7e1f2d9b5c4f4cc8591edf79d07deb9df6'
$ cd mod-users
$ mvn install
  [...]
  [INFO] ------------------------------------------------------------------------
  [INFO] BUILD SUCCESS
  [INFO] ------------------------------------------------------------------------
  [INFO] Total time: 01:21 min
  [INFO] Finished at: 2017-02-24T16:52:58-05:00
  [INFO] Final Memory: 74M/532M
  [INFO] ------------------------------------------------------------------------
```

### Register and Deploy the Users app Okapi Module

As part of that build process, the mod-user ModuleDescriptor and DeploymentDescriptor were generated into the "target" directory. They can be used to register and deploy the Users app Okapi Module.

```shell
$ cd $FOLIO_ROOT
$ curl -i -w '\n' -X POST -H 'Content-type: application/json' \
   -d @mod-users/target/ModuleDescriptor.json http://localhost:9130/_/proxy/modules

  HTTP/1.1 100 Continue

  HTTP/1.1 201 Created
  Content-Type: application/json
  Location: /_/proxy/modules/mod-users-14.2.2-SNAPSHOT
  X-Okapi-Trace: POST okapi-2.0.1-SNAPSHOT /_/proxy/modules : 201 4863us
  Content-Length: 5699

  {
    "id" : "mod-users-14.2.2-SNAPSHOT",
    "name" : "users",
   [...]
  }
```

You will also need to deploy the module with a Deployment Descriptor:

```shell
$ curl -i -w '\n' -X POST -H 'Content-type: application/json' \
  -d @mod-users/target/DeploymentDescriptor.json http://localhost:9130/_/discovery/modules

  HTTP/1.1 201 Created
  Content-Type: application/json
  Location: /_/discovery/modules/mod-users-14.2.2-SNAPSHOT/localhost-9133
  X-Okapi-Trace: POST okapi-2.0.1-SNAPSHOT /_/discovery/modules : 201
  Content-Length: 258

  {
    "instId" : "localhost-9133",
    "srvcId" : "mod-users-14.2.2-SNAPSHOT",
    "nodeId" : "localhost",
    "url" : "http://localhost:9133",
    "descriptor" : {
      "exec" : "java -jar ../mod-users/target/mod-users-fat.jar -Dhttp.port=%p embed_postgres=true"
    }
  }
```

(Note: Your port number in the `instId` and the `url` may vary depending on whether there are other Okapi Modules deployed on the Okapi Gateway.)
Finally, you'll need to enable the Okapi Users app module for the test tenant:

```shell
$ cat > okapi-enable-users.json <<END
{
  "id" : "mod-users-14.2.2-SNAPSHOT"
}
END
$ curl -i -w '\n' -X POST -H 'Content-type: application/json' \
   -d @okapi-enable-users.json http://localhost:9130/_/proxy/tenants/testlib/modules

HTTP/1.1 201 Created
Content-Type: application/json
Location: /_/proxy/tenants/testlib/modules/mod-users-14.2.2-SNAPSHOT
X-Okapi-Trace: POST okapi-2.0.1-SNAPSHOT /_/proxy/tenants/testlib/modules : 201
Content-Length: 40

{
  "id" : "mod-users-14.2.2-SNAPSHOT"
}
```

The FOLIO Users app is now available at [http://localhost:3000/users](http://localhost:3000/users).
You'll see the message `No results found for "". Please check your spelling and filters`.
This is because no users have yet been added.

## Add users to FOLIO

For testing purposes, the FOLIO development team has JSON documents representing factitious users that can be used to populate the dev FOLIO environment.

```shell
$ cd $FOLIO_ROOT
$ cat > User000.json <<END
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
$ cat > User001.json <<END
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
    -H 'X-Okapi-Tenant: testlib' -d @User000.json http://localhost:9130/users

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
X-Okapi-Trace: POST mod-users-14.2.2-SNAPSHOT http://localhost:9133/users : 201 250116us
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
    -H 'X-Okapi-Tenant: testlib' -d @User001.json http://localhost:9130/users

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
X-Okapi-Trace: POST mod-users-14.2.2-SNAPSHOT http://localhost:9133/users : 201 11408us
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

Now be satisfied that those users were added:

```
$ curl -i -X GET -H "Content-Type:application/json" \
    -H 'X-Okapi-Token: dummyJwt.eyJzdWIiOiJzZWIiLCJ0ZW5hbnQiOm51bGx9.sig' \
    -H "X-Okapi-Tenant:testlib" \
    http://localhost:9130/users
```

A more useful set of users is available when using the Vagrant boxes.

