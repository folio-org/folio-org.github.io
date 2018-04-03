---
layout: tutorials
title: Overview
heading: Tutorials
permalink: /tutorials/foliodeveloperscurr/
---

# FOLIO Developer's Curriculum

Follow the FOLIO Developer's Curriculum to gain a better understanding of the Stripes Development server and the Okapi Gateway. 

## Introduction

This is an outline of a tutorial that can be given to a group in a workshop or followed by an individual developer in a self-paced fashion.

### Goals

* Set up a running instance of the Stripes Development UI Server
* Set up a running instance of Okapi Gateway
* Demonstrate how to deploy an Okapi Module to a tenant in Okapi Gateway and the Stripes UI Server
* Understand how Okapi Gateway routes requests to modules

### System Requirements

There are two choices: either running the Stripes Development UI Server and the Okapi Gateway directly on a developer’s machine (“on-machine”) or running Stripes and Okapi in a VirtualBox guest.
An Ansible playbook with appropriate roles is used to create the VirtualBox guest, and can also be used to automatically build a developer’s environment (making the playbook target localhost).

* macOS 10.? or higher (On-machine or VirtualBox)
* Windows 10 or higher (VirtualBox required)
* Linux (On-machine or VirtualBox)

### Prerequisites

Before attending the workshop, participants must meet these requirements.
When in doubt, using the VirtualBox guest machine is recommended.

#### On-Machine

* [Java 8 JDK 1.8.0-101](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html) or higher
* Maven 3.3.9 or higher
* Node.js 6.x or higher
* [Yarn](https://yarnpkg.com/en/) package manager v0.20.3 or higher
* [curl](https://curl.haxx.se)

#### VirtualBox guest

* [VirtualBox 5.1 or higher](https://www.virtualbox.org/wiki/Downloads)
* [Vagrant 1.9.1 or higher](https://www.vagrantup.com/downloads.html), for Windows 7 use [1.9.6 .msi](https://releases.hashicorp.com/vagrant/1.9.6/) ([learn why](https://github.com/hashicorp/vagrant/issues/8783))

To download the VirtualBox guest:
1. Make a clean directory and change into it: `mkdir folio-curriculum && cd folio-curriculum`
1. Set up the Vagrantfile: `vagrant init --minimal folio/curriculum`
1. Launch the VirtualBox guest: `vagrant up`
1. Connect to the VirtualBox guest: `vagrant ssh`

Note: Do this download prior to attending a workshop.
If also doing [Lesson 6](/tutorials/foliodeveloperscurr/#interact-with-the-folio-stable-vm) then get it ready beforehand too.

<div class="vagrant-note" markdown="1">
In subsequent lessons, the command lines are executed within the VirtualBox guest.
Be sure you are connected to the VirtualBox guest (from the host computer: `vagrant ssh`) before running the commands.

Other instructions and commands that are specific to the VirtualBox guest mode of using the tutorial are noted using this style of information box.

There are some FOLIO-related Vagrant tips, known issues, and troubleshooting [notes](https://github.com/folio-org/folio-ansible/blob/master/doc/index.md#troubleshootingknown-issues) available.
</div>

<div class="vagrant-on-windows-note" markdown="1">
If launching Vagrant from a Windows Command Prompt, be sure to use _Run As Administrator..._ when opening the Command Prompt itself (`cmd.exe`).  If you are seeing the error _"EPROTO: protocol error, symlink"_, the likely cause is that Vagrant was not launched with administrator privileges.  See issue [STRIPES-344](https://issues.folio.org/browse/STRIPES-344) for details.
</div>

### Set `FOLIO_ROOT` Variable

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

### Lessons/Steps
1. [Clone, build and explore Okapi](/tutorials/foliodeveloperscurr/#clone-and-install-okapi)
1. [Initialize Okapi Gateway from the command line](/tutorials/foliodeveloperscurr/#initialize-okapi)
1. [Enable Okapi Authentication](/tutorials/foliodeveloperscurr/#enable-okapi-authentication)
1. [Deploy test Stripes package](/tutorials/foliodeveloperscurr/#deploy-test-stripes-module)
1. Real-world application: [set up the FOLIO Users app](/tutorials/foliodeveloperscurr/#set-up-the-okapi-users-app)
1. [Interact with the FOLIO Stable VM](/tutorials/foliodeveloperscurr/#interact-with-the-folio-stable-vm)

### Run Jekyll Locally
To view the documentation locally:
* (once) `git clone git@github.com/folio-org/curriculum.git folio-curriculum && cd folio-curriculum && bundle install`
* `bundle exec jekyll serve`
* View the site locally at http://localhost:4000/curriculum/

### Additional information

See project [FOLIO](https://issues.folio.org/browse/FOLIO)
at the [FOLIO issue tracker](https://issues.folio.org/community/guide-issues).

Other FOLIO Developer documentation is at [dev.folio.org](http://dev.folio.org/)

## Clone, Build and Explore Okapi

### Clone and Install Okapi
```shell
$ cd $FOLIO_ROOT
$ git clone --recursive https://github.com/folio-org/okapi.git
  Cloning into 'okapi'...
  [...]
  Submodule path 'okapi-core/src/main/raml/raml-util': checked out 'a22e8c5b7ab919c692407a0d674f53c317088aac'
```

The first time Okapi is installed will take several minutes as various JAR files are downloaded from the Maven repository.
Subsequent installs will not take as long.

```shell
$ cd okapi
$ mvn install
  [...]
  [INFO] ------------------------------------------------------------------------
  [INFO] Reactor Summary:
  [INFO]
  [INFO] okapi .............................................. SUCCESS [ 10.832 s]
  [INFO] okapi-common ....................................... SUCCESS [01:28 min]
  [INFO] okapi-test-module .................................. SUCCESS [ 12.656 s]
  [INFO] okapi-test-auth-module ............................. SUCCESS [  1.374 s]
  [INFO] okapi-test-header-module ........................... SUCCESS [  1.431 s]
  [INFO] okapi-core ......................................... SUCCESS [02:15 min]
  [INFO] ------------------------------------------------------------------------
  [INFO] BUILD SUCCESS
  [INFO] ------------------------------------------------------------------------
  [INFO] Total time: 04:21 min
  [INFO] Finished at: 2017-05-23T20:23:32+00:00
  [INFO] Final Memory: 38M/264M
  [INFO] ------------------------------------------------------------------------
```

### Interact with the test modules as if you are the Okapi Gateway

The `mvn install` command builds _okapi-core_ (the Okapi Gateway server) and _okapi-common_ (utilities used by both the gateway server and by modules) along with three simple test Okapi Modules.
Before starting the Okapi Gateway, we are going to look at one of the three test Okapi Modules and interact with them as if we are the Okapi Gateway.
Okapi is an implementation of the "API Gateway" microservices pattern.
As such, the Okapi Gateway accepts RESTful requests from clients and routes them through a series of RESTful interfaces ("Okapi Modules") to build a response that is ultimately returned to the client.
(For more details about the Okapi architecture, see the [Okapi Guide and Reference](https://github.com/folio-org/okapi/blob/master/doc/guide.md#architecture).)

To see what this interaction between _okapi-core_ and Okapi Modules looks like, let's start an Okapi Module and send it some requests via `curl`.

#### Interact with Okapi-test-module

The _Okapi-test-module_ is a very simple Okapi Module.
If you make a GET request to it, it will reply "It works".
If you POST something to it, it will reply with "Hello" followed by whatever you posted.
First we start the test module:

```shell
$ cd $FOLIO_ROOT/okapi
$ java -jar okapi-test-module/target/okapi-test-module-fat.jar
  13:53:00 INFO  MainVerticle         Starting okapi-test-module 42510@Walkabout.lan on port 8080
  13:53:00 INFO  ertxIsolatedDeployer Succeeded in deploying verticle
```

With the _Okapi-test-module_ now listening on port 8080, in another terminal window send a simple `curl` command as shown below.

<div class="vagrant-note" markdown="1">
When using the VirtualBox method, you will need to open a new terminal window on your host computer, change the working directory to the location of the `Vagrantfile`, and use the `vagrant ssh` command to connect from the host computer to the guest.
<p>&nbsp;</p>
</div>

Note that the `-i` command line option tells `curl` to output the response headers in addition to the response body, and the `-w '\n'` option adds a newline to the end of the response body to ensure the shell prompt starts on a new line.

```shell
$ curl -i -w '\n' http://localhost:8080/testb
  HTTP/1.1 200 OK
  Content-Type: text/plain
  Content-Length: 8

  It works
```

Next make a HTTP POST request (using `-X POST`) and send the string `Testing Okapi` (using the -d command line option):

```shell
$ curl -i -w '\n' -X POST -d "Testing Okapi" http://localhost:8080/testb
  HTTP/1.1 200 OK
  Content-Type: text/plain
  Transfer-Encoding: chunked

  Hello Testing Okapi
```

Okapi modules would typically send and receive JSON content bodies, but in these examples simple strings are sent and returned.
Leave the Okapi Gateway running (as started by the `java -jar okapi-test-module/target/okapi-test-module-fat.jar` command above) for the next lesson section below.

#### Interact with Okapi-test-module with headers

As a RESTful interface, the Okapi Gateway communicates key data to Okapi Modules and to the client using HTTP headers.
For example: as Okapi Modules are chained together by the Okapi Gateway, a module may want to signal to the gateway that it encountered an exception and must interrupt the chain.

For example, send an HTTP GET request with an `X-my-header: blah` header (using the `-H` command line argument):

```shell
$ curl -i -w '\n' -X GET -H 'X-my-header: blah' http://localhost:8080/testb
  HTTP/1.1 200 OK
  Content-Type: text/plain
  Content-Length: 12

  It worksblah
```

This example appends the contents of the `X-my-header` to the response body.
If we add an 'X-stop-here' header, the module returns the `X-Okapi-Stop` header (which would trigger the exception handling in the Okapi gateway):

```shell
$ curl -i -w '\n' -X GET -H 'X-my-header: blah' \
    -H 'X-stop-here: because I said so.' \
    http://localhost:8080/testb
  HTTP/1.1 200 OK
  Content-Type: text/plain
  X-Okapi-Stop: because I said so.
  Content-Length: 12

  It worksblah
```

(Note that there is not an `X-stop-here` request header defined in Okapi.  This is a header specific to the _Okapi-test-module_ that forces the return of the Okapi-defined `X-Okapi-Stop` response header.)

The corresponding Okapi Module code that is handling this interaction can be found in the [okapi-test-module/.../MainVerticle.java]( https://github.com/folio-org/okapi/blob/master/okapi-test-module/src/main/java/org/folio/okapi/sample/MainVerticle.java) file.

Return to the terminal window with _Okapi-test-module_ running and press Control-C to exit it.

## Initialize Okapi

### Start the Okapi Gateway

In a terminal window, start the Okapi Gateway service.

<div class="vagrant-note" markdown="1">
When using the VirtualBox method, you will need to open a terminal window on your host computer, change the working directory to the location of the `Vagrantfile`, and use the `vagrant ssh` command to connect from the host computer to the guest.
<p>&nbsp;</p>
</div>

```shell
$ cd $FOLIO_ROOT/okapi
$ java -Dloglevel=DEBUG -jar okapi-core/target/okapi-core-fat.jar dev
  ...
  ...
  12:08:12 INFO  MainVerticle         API Gateway started PID 64161@Walkabout.lan. Listening on port 9130
```

The `dev` parameter starts the Okapi Gateway in 'development mode' (a known, clean state without any modules or tenants defined).
The Okapi Gateway is using an in-memory database (a built-in PostgreSQL database can be specified by adding `-Dstorage=postgres` before the `-jar` parameter).
We are going to run the Okapi Gateway with debugging turned on so you can see the effect of the requests passing through the gateway.
The last line of output tells us that the Okapi Gateway is running on port 9130.

Open up a second terminal window (noting that if you are using the VagrantBox method you will need to open a new terminal on your host and use the `vagrant ssh` command), then use these two curl commands to list the Okapi Modules and tenants known to the gateway:

```shell
$ curl -i -w '\n' -X GET http://localhost:9130/_/proxy/modules

  HTTP/1.1 200 OK
  Content-Type: application/json
  X-Okapi-Trace: GET okapi-2.0.1-SNAPSHOT /_/proxy/modules : 200 8733us
  Content-Length: 74

  [ {
    "id" : "okapi-2.0.1-SNAPSHOT",
    "name" : "okapi-2.0.1-SNAPSHOT"
  } ]

$ curl -i -w '\n' -X GET http://localhost:9130/_/proxy/tenants

  HTTP/1.1 200 OK
  Content-Type: application/json
  X-Okapi-Trace: GET okapi-2.0.1-SNAPSHOT /_/proxy/tenants : 200 887us
  Content-Length: 117

  [ {
    "id" : "okapi.supertenant",
    "name" : "okapi.supertenant",
    "description" : "Okapi built-in super tenant"
  } ]
```

As we have just started the gateway, there is only the internal module and the internal supertenant, meaning that the newly initialized Okapi Gateway has no actual configured modules or tenants.

Paths starting with `/_/` are core Okapi Gateway services.
`/_/proxy` is one core service; it is used to (//TODO define this).
Another core service is `/_/discovery`; it is used to interact with nodes in the Okapi cluster.
More details about these core services can be found in the [Okapi Guide and Reference](https://github.com/folio-org/okapi/blob/master/doc/guide.md#deployment-and-discovery).
In the next section we will use these two core services to register a module and a tenant.

### Defining the _okapi-test-module_ within the Okapi Gateway
Defining a module with the Okapi Gateway occurs in three steps: Registering, Deploying, and Configuring the proxy.

#### Registering _okapi-test-module_
To tell Okapi that we want to use the okapi-test-module, we create a JSON structure of a "Module Descriptor" and POST it to Okapi.
The command below creates a Module Descriptor JSON structure.
(Leave the Okapi Gateway running in one window and execute this command in another window.)

```shell
$ cd $FOLIO_ROOT
$ cat > okapi-proxy-test-basic.json <<END
  {
    "id": "test-basic-1.0.0",
    "name": "Okapi test module",
    "provides": [
      {
        "id": "test-basic",
        "version": "2.2",
        "handlers": [
          {
            "methods": [ "GET", "POST" ],
            "pathPattern": "/testb"
          }
        ]
      },
      {
        "id": "_tenant",
        "version": "1.0",
        "interfaceType": "system",
        "handlers": [
          {
            "methods": [ "POST" ],
            "pathPattern": "/_/tenant"
          }
        ]
      }
    ],
    "requires": [],
    "launchDescriptor": {
      "exec": "java -Dport=%p -jar okapi-test-module/target/okapi-test-module-fat.jar"
    }
  }
END
```

This is a module descriptor for `test-module` (the first `id` key-value pair).
It `provides` two interfaces: `test-basic` and `_tenant`.
The `test-basic` interface is how clients will communicate with the Okapi Module (as we did directly in the previous lesson).
Interfaces beginning with an underscore (such as `_tenant`) are reserved system interfaces; in this case, an interface that is called when a module is enabled or disabled for a tenant.
The `handling` dictionary tells the gateway:
* which HTTP methods are expected
* the path registered in the gateway for which this interface will receive requests
* the type of response provided by this module interface
* permissions required (enforced by the Okapi Gateway)
* permissions desired (a list of requester's permissions that the business logic of this module needs to know about)
The final entry, `launchDescriptor`, tells the gateway how to start the Okapi Module.

To deploy the module, this JSON is POSTed to the `/_/proxy/modules` core service:

```shell
$ curl -i -w '\n' -X POST -H 'Content-type: application/json' \
   -d @okapi-proxy-test-basic.json http://localhost:9130/_/proxy/modules
  HTTP/1.1 201 Created
  Content-Type: application/json
  Location: /_/proxy/modules/test-basic-1.0.0
  X-Okapi-Trace: POST ...
  Content-Length: 547

  {
    "id" : "test-basic-1.0.0",
    "name" : "Okapi test module",
    ...
  }
```

The Okapi Gateway responds with an [HTTP 201 ("Created")](https://httpstatusdogs.com/201-created) status code and returns the request body as the response body.
There is also a `Location:` header that is the URL of the newly created module.
That address can be used with other HTTP verbs ('GET' to read, 'POST' to update, 'DELETE' to remove) as one would expect for a RESTful resource.
Run these commands to list the modules known to the gateway, delete _test-module_, and list the modules again to see for yourself:

```shell
$ curl -i -w '\n' -X GET http://localhost:9130/_/proxy/modules

$ curl -i -w '\n' -X DELETE http://localhost:9130/_/proxy/modules/test-basic-1.0.0

$ curl -i -w '\n' -X GET http://localhost:9130/_/proxy/modules

$ curl -i -w '\n' -X POST -H 'Content-type: application/json' \
   -d @okapi-proxy-test-basic.json http://localhost:9130/_/proxy/modules

$ curl -i -w '\n' -X GET http://localhost:9130/_/proxy/modules
```

#### Deploying _okapi-test-module_
Although we have registered the module with the Okapi Gateway, we have not yet instantiated the module so that there is something available to respond to requests.
The module must also be deployed on one node (or more, in the case of clusters).
First, let's query the discovery service for a list of nodes it knows about in the cluster:

```shell
$ curl -i -w '\n' -X GET http://localhost:9130/_/discovery/nodes
  HTTP/1.1 200 OK
  Content-Type: application/json
  Content-Length: 67

  [ {
    "nodeId" : "localhost",
    "url" : "http://localhost:9130"
  } ]
```

The response body is a JSON document that, for our Okapi Gateway instance running with the 'dev' option, show just one node (`nodeId` of `localhost`).

To deploy the module, we create a "Deployment Descriptor" JSON document:

```shell
$ cat > okapi-deploy-test-basic.json <<END
{
  "srvcId" : "test-basic-1.0.0",
  "nodeId" : "localhost"
}
END
```

Then post this document to the `/_/discovery` core service:

```shell
$ curl -i -w '\n' -X POST -H 'Content-type: application/json' \
   -d @okapi-deploy-test-basic.json http://localhost:9130/_/discovery/modules
 HTTP/1.1 201 Created
 Content-Type: application/json
 Location: /_/discovery/modules/test-basic-1.0.0/localhost-9131
 Content-Length: 237

 {
   "instId" : "localhost-9131",
   "srvcId" : "test-basic-1.0.0",
   "nodeId" : "localhost",
   "url" : "http://localhost:9131",
   "descriptor" : {
     "exec" : "java -Dport=%p -jar okapi-test-module/target/okapi-test-module-fat.jar"
   }
 }
```

The Okapi Gateway server returns an [HTTP 201 ("Created")](https://http.cat/201) status code responds with a JSON document that includes additional information:
* an instance identifier ('instId') for this particular deployment of the module
* a URL where the instance will receive requests
* a copy of the launch descriptor line from the Module Descriptor

In addition, the gateway returns a `Location:` header that is the URL of this deployed instance.
As with module descriptors, that URL can be used to retrieve information about the deployed instance (HTTP `GET`) and stop the deployed instance (HTTP `DELETE`).
Be sure to also flip back to the terminal session running the Okapi Gateway to see the server-side debug messages.

One important note: in our developer instance, we can access the _okapi-test-module_ directly at the URL http://localhost:9131:

```shell
$ curl -i -w '\n' -X GET http://localhost:9131/testb
  HTTP/1.1 200 OK
  Content-Type: text/plain
  Content-Length: 8

  It works
```

In a production system, there would be a firewall that prevents direct access to the Okapi Module interfaces.
Requests for Okapi Module services must go through the Okapi Gateway to ensure that access control and tenant restrictions are honored.

### Creating a tenant
As noted above, all requests should be made through the Okapi Gateway.
Let's try that now:

```shell
$ curl -i -w '\n' -X GET http://localhost:9130/testb
  HTTP/1.1 403 Forbidden
  Content-Type: text/plain
  Content-Length: 14

  Missing Tenant
```

Okapi is inherently a multi-tenant system, so each request to an Okapi Module must be performed on behalf of a tenant.
Let's set up our first tenant:

```shell
$ cat > okapi-tenant.json <<END
{
  "id" : "testlib",
  "name" : "Test Library",
  "description" : "Our Own Test Library"
}
END
$ curl -i -w '\n' -X POST -H 'Content-type: application/json' \
   -d @okapi-tenant.json http://localhost:9130/_/proxy/tenants
  HTTP/1.1 201 Created
  Content-Type: application/json
  Location: /_/proxy/tenants/testlib
  Content-Length: 91

  {
   "id" : "testlib",
   "name" : "Test Library",
   "description" : "Our Own Test Library"
  }
```
### Enable _test-module_ for the _testlib_ tenant
Now that the tenant is created, we need to enable _test-module_ for that tenant:

```shell
$ cat > okapi-enable-basic.json <<END
{
  "id" : "test-basic-1.0.0"
}
END
$ curl -i -w '\n' -X POST -H 'Content-type: application/json' \
   -d @okapi-enable-basic.json http://localhost:9130/_/proxy/tenants/testlib/modules
  HTTP/1.1 201 Created
  Content-Type: application/json
  Location: /_/proxy/tenants/testlib/modules/test-basic-1.0.0
  Content-Length: 31

  {
    "id" : "test-basic-1.0.0"
  }
```

Switch back to the Okapi Gateway terminal to see the debug output for this last request.

```
21:32:59 DEBUG ProxyContext         176769/_ Assigned new reqId 176769/_
21:32:59 INFO  ProxyContext         176769/_ REQ 0:0:0:0:0:0:0:1:35269 - POST /_/proxy/tenants/testlib/modules
21:32:59 DEBUG TenantManager        findTenantInterface: prov: [{"id":"test-basic","version":"2.2","handlers":[{"methods":["GET","POST"],"pathPattern":"/testb"}]},{"id":"_tenant","version":"1.0","interfaceType":"system","handlers":[{"methods":["POST"],"pathPattern":"/_/tenant"}]}]
21:32:59 DEBUG TenantManager        findTenantInterface: Looking at test-basic
21:32:59 DEBUG TenantManager        findTenantInterface: Looking at _tenant
21:32:59 DEBUG ProxyContext         176769/_ enableModule Url: http://localhost:9131 and /_/tenant
21:32:59 DEBUG TenantWebService     Added X-Okapi-Tenant : testlib
21:32:59 INFO  OkapiClient          176769/_;005955/tenant REQ okapiClient testlib POST http://localhost:9131/_/tenant
21:32:59 DEBUG OkapiClient          176769/_;005955/tenant OkapiClient: adding header X-Okapi-Request-Id: 176769/_;005955/tenant
21:32:59 DEBUG OkapiClient          176769/_;005955/tenant OkapiClient: adding header Accept: */*
21:32:59 DEBUG OkapiClient          176769/_;005955/tenant OkapiClient: adding header X-Okapi-Tenant: testlib
21:32:59 DEBUG OkapiClient          176769/_;005955/tenant OkapiClient: adding header Content-Type: application/json; charset=UTF-8
21:32:59 INFO  OkapiClient          176769/_;005955/tenant RES 200 0us okapiClient http://localhost:9131/_/tenant
21:32:59 DEBUG OkapiClient          176769/_;005955/tenant OkapiClient Buffering response POST request to okapi-test-module tenant service for tenant testlib
21:32:59 INFO  MainVerticle         POST request to okapi-test-module tenant service for tenant testlib
21:32:59 DEBUG OkapiClient          176769/_;005955/tenant OkapiClient Buffering response {
  "module_to" : "test-basic-1.0.0"
}
21:32:59 DEBUG ProxyContext         176769/_ enableModule: Tenant init request to test-basic-1.0.0 succeeded
21:32:59 INFO  ProxyContext         176769/_ RES 201 135657us okapi
```

In this string of messages you can see the Okapi Gateway finding the tenant and, as a "loopback" OkapiClient, post a request to the reserved `/_/tenant` interface of _okapi-test-module_ on http://localhost:9191 (http://localhost:9191/_/tenant).
This allows the Okapi Module to perform an initialization routine when it is added to a new tenant.
Note the log line that says an `X-Okapi-Tenant: testlib` header is being added to the request being made by OkapiClient.
We, too, must also add an `X-Okapi-Tenant` header when sending a request to an Okapi Module:

```shell
$ curl -i -w '\n' -X GET -H 'X-Okapi-Tenant: testlib' http://localhost:9130/testb
  HTTP/1.1 200 OK
  Content-Type: text/plain
  X-Okapi-Trace: GET - Okapi test module http://localhost:9131/testb : 200 12629us
  Transfer-Encoding: chunked

  It works
```

Also note that the core interfaces behave as we expect them to by returning JSON lists.
Try these commands:

```shell
$ curl -i -w '\n' -X GET http://localhost:9130/_/proxy/tenants

$ curl -i -w '\n' -X GET http://localhost:9130/_/proxy/tenants/testlib/modules
```

## Enable Okapi Authentication

All real-world uses of Okapi will need to provide authentication and authorization services.
The Okapi Gateway itself does not handle these tasks; rather, it delegates them to one or more Okapi Modules that operates at an early phase of module requests orchestrated by the Okapi Gateway.
In this lesson we will first interact directly with a sample authentication Okapi Module.
Later in the lesson we will register and deploy the sample authentication module on the Okapi Gateway.
Authorization will be covered in a later lesson.

### Interact Directly with Okapi-test-auth-module
_Okapi-test-auth-module_ is a simple module that illustrates authentication in Okapi, and it comes with _okapi-core_.

In a terminal window, start the _okapi-test-auth-module_.

<div class="vagrant-note" markdown="1">
When using the VirtualBox method, you will need to open a terminal window on your host computer, change the working directory to the location of the `Vagrantfile`, and use the `vagrant ssh` command to connect from the host computer to the guest.
<p>&nbsp;</p>
</div>

```shell
$ cd $FOLIO_ROOT/okapi
$ java -jar okapi-test-auth-module/target/okapi-test-auth-module-fat.jar
  02:15:42 INFO  MainVerticle         Starting auth 26062@contrib-jessie on port 9020
  02:15:42 INFO  ertxIsolatedDeployer Succeeded in deploying verticle
```

The `/login` path of _okapi-test-auth-module_ takes a simple JSON document with a 'username' and a 'password' value.
In this test authentication module, if the password is the same as the username with the string '-password' appended then the authentication is successful and a token is returned.
This can be demonstrated by using this curl command in a second terminal window to send a sample JSON document to the _okapi-test-auth-module_.

```shell
$ curl -i -w '\n' -X POST -H 'X-Okapi-Tenant: blah' \
    -d '{"username": "seb", "password": "seb-password"}' \
    http://localhost:9020/authn/login
  HTTP/1.1 200 OK
  Content-Type: application/json
  X-Okapi-Token: dummyJwt.eyJzdWIiOiJzZWIiLCJ0ZW5hbnQiOm51bGx9.sig
  Content-Length: 47

  {"username": "seb", "password": "seb-password"}
```

Now try to send a JSON document in which the password does not match the expected value.
Note that the response returns an [HTTP 401 "Unauthorized"](https://http.cat/401) status.

Another path supplied by _okapi-test-auth-module_ is `/check`; it checks an _X-Okapi-Token_ to see if it is valid.
```shell
$ curl -i -w '\n' -X GET -H 'X-Okapi-Tenant: blah' \
    -H 'X-Okapi-Token: dummyJwt.eyJzdWIiOiJzZWIiLCJ0ZW5hbnQiOm51bGx9.sig' \
    http://localhost:9020/check
  HTTP/1.1 202 Accepted
  X-Okapi-Token: dummyJwt.eyJzdWIiOiJzZWIiLCJ0ZW5hbnQiOm51bGx9.sig
  X-Okapi-Module-Tokens: {}
  X-Okapi-User-Id: seb
  Content-Type: text/plain
  Transfer-Encoding: chunked
```

Note that the response returns an [HTTP 202 "Accepted"](https://httpstatusdogs.com/202-accepted) status.
Try sending a request without the required _X-Okapi-Tenant_ header.
All requests are expected to send the _X-Okapi-Tenant_ header.

Return to the terminal window with _okapi-test-auth-module_ running and press Control-C to exit it.

### Register and Deploy the _Okapi-test-auth-module_ in the Okapi Gateway
The _Okapi-test-auth-module_ is registered and deployed just like any other Okapi Module: using a ModuleDescriptor and a DeploymentDescriptor.
In the terminal window, start the Okapi Gateway with debugging turned on:

```shell
$ cd $FOLIO_ROOT/okapi
$ java -Dloglevel=DEBUG -jar okapi-core/target/okapi-core-fat.jar dev
  12:08:11 INFO  MainVerticle         git: git@github.com:folio-org/okapi 225c9c1e03c29459da430f93110abb30378e1394
  12:08:11 INFO  MainVerticle         clusterManager not in use
  12:08:11 INFO  MainVerticle         Proxy using inmemory storage
  12:08:12 WARN  Storage              Storage.resetDatabases: NORMAL
  12:08:12 INFO  TenantWebService     All tenants deployed
  12:08:12 INFO  MainVerticle         API Gateway started PID 64161@Walkabout.lan. Listening on port 9130
```

Open up a second terminal window to send JSON documents to the Okapi Gateway using _curl_ (noting that if you are using the VagrantBox method you will need to open a new terminal on your host and use the `vagrant ssh` command).
The examples in this tutorial are using the in-memory storage, so you will need to resend the _Okapi-test-module_ ModuleDescriptor and DeploymentDescriptor as well as redefine the `testlib` tenant and enable the _Okapi-test-module_.
If you completed the previous lesson, these JSON documents are in the `$FOLIO_ROOT` directory.

```shell
$ cd $FOLIO_ROOT
$ curl -i -w '\n' -X POST -H 'Content-type: application/json' \
   -d @okapi-proxy-test-basic.json http://localhost:9130/_/proxy/modules
$ curl -i -w '\n' -X POST -H 'Content-type: application/json' \
   -d @okapi-deploy-test-basic.json http://localhost:9130/_/discovery/modules
$ curl -i -w '\n' -X POST -H 'Content-type: application/json' \
   -d @okapi-tenant.json http://localhost:9130/_/proxy/tenants
$ curl -i -w '\n' -X POST -H 'Content-type: application/json' \
   -d @okapi-enable-basic.json http://localhost:9130/_/proxy/tenants/testlib/modules
```

#### Okapi Auth Module ModuleDescriptor

This example of a ModuleDescriptor is similar to the one used for the _Okapi-test-module_.

```shell
$ cat > okapi-proxy-test-module-auth.json <<END
  {
    "id": "test-auth-3.4.1",
    "name": "Okapi test auth module",
    "provides": [
      {
        "id": "test-auth",
        "version": "3.4",
        "handlers": [
          {
            "methods" : [ "POST" ],
            "pathPattern" : "/authn/login"
          }
        ]
      }
    ],
    "requires": [],
    "filters": [
      {
        "methods": [ "*" ],
        "pathPattern": "/*",
        "phase": "auth",
        "type": "headers"
      }
    ]
  }
END
$ curl -i -w '\n' -X POST -H 'Content-type: application/json' \
   -d @okapi-proxy-test-module-auth.json http://localhost:9130/_/proxy/modules
```

The significant difference is a new dictionary called `filters`.
The `filters` dictionary specifies paths and phases for which the Okapi Gateway will call this module.
At the moment, there is only one phase (`auth`) and the `methods` and `pathPattern` specify that this module will be called for all Okapi Gateway requests.
Another difference is that the `launchDescriptor` is omitted; as shown below, the `launchDescriptor` can also be defined in the DeploymentDescriptor.
(This can be useful in cases where there are command-line options specific to a particular deployment.)

#### Okapi Auth Module DeploymentDescriptor

This example of a DeploymentDescriptor is similar to the one used for the _Okapi-test-module_.
Note that the `launchDescriptor` dictionary is defined here.

```shell
$ cat > okapi-deploy-test-module-auth.json <<END
  {
    "srvcId": "test-auth-3.4.1",
    "nodeId": "localhost",
    "descriptor": {
      "exec": "java -Dport=%p -jar okapi-test-auth-module/target/okapi-test-auth-module-fat.jar"
    }
  }
END
$ curl -i -w '\n' -X POST -H 'Content-type: application/json' \
   -d @okapi-deploy-test-module-auth.json http://localhost:9130/_/discovery/modules
```

#### Enable Okapi Auth Module on tenant

```shell
$ cat > okapi-enable-auth.json <<END
  {
    "id": "test-auth-3.4.1"
  }
END
$ curl -i -w '\n' -X POST -H 'Content-type: application/json' \
   -d @okapi-enable-auth.json http://localhost:9130/_/proxy/tenants/testlib/modules
```

### Demonstrating the Impact of the Okapi Auth Module

If we now send the same test request from the end of the previous lesson to the _Okapi-test-module_, we see a different response from the Okapi Gateway.

```shell
$ curl -i -w '\n' -X GET -H 'X-Okapi-Tenant: testlib' http://localhost:9130/testb

  HTTP/1.1 401 Unauthorized
  Content-Type: text/plain
  X-Okapi-Trace: GET test-auth-3.4.1 http://localhost:9132/testb : 401 62623us
  Transfer-Encoding: chunked

  Auth.check called without X-Okapi-Token
```

With the _Okapi-test-auth-module_ filter now configured to intercept all requests to the Okapi Gateway, the Gateway responds with an [HTTP 401 ("Unauthorized")](https://http.cat/401) and in the response body tells us that the _X-Okapi-Token_ is missing.
This is the same _X-Okapi-Token_ described in the first section of this lesson.
If we send a request header with a valid _X-Okapi-Token_, the request is successful.

```shell
$ curl -i -w '\n' -X GET -H 'X-Okapi-Tenant: testlib' \
    -H 'X-Okapi-Token: dummyJwt.eyJzdWIiOiJzZWIiLCJ0ZW5hbnQiOm51bGx9.sig' \
    http://localhost:9130/testb

  HTTP/1.1 200 OK
  X-Okapi-Trace: GET test-auth-3.4.1 http://localhost:9132/testb : 202 152538us
  Content-Type: text/plain
  X-Okapi-Trace: GET test-basic-1.0.0 http://localhost:9131/testb : 200 7440us
  Transfer-Encoding: chunked

  It works
```

## Deploy test Stripes module

In this lesson we set aside the Okapi server (leave it running) and focus on the web-based user interface, Stripes.  The Okapi Gateway is not required for this lesson.

### Inform the Yarn package manager of the FOLIO UI registry location
(Note: the output of commands is artificially indented from the command line to call out the command lines.)
```
$ yarn config set @folio:registry https://repository.folio.org/repository/npm-folio/
  yarn config v0.20.3
  success Set "@folio:registry" to "https://repository.folio.org/repository/npm-folio/".
  ✨  Done in 0.04s.
```

### Set up a Stripes Development UI Server

Create an empty directory to hold the Stripes UI Server configuration (called `stripes-tutorial-platform`).

```shell
$ mkdir $FOLIO_ROOT/stripes-tutorial-platform
$ cd $FOLIO_ROOT/stripes-tutorial-platform
```

In that directory, put two configuration files: The `package.json` and `stripes.config.js` files, with the following basic content:

#### Contents of `package.json`

`package.json` is a [Node Package Manager (NPM) configuration file](https://docs.npmjs.com/files/package.json).
It is a JSON file that contains two dictionaries: _scripts_ and _dependencies_.
The _scripts_ dictionary specifies name-value pairs of commands that are used by Yarn to build and run the platform.
The _dependencies_ dictionary lists packages (and specific versions) that make up the Stripes client bundles.

At this stage of the Curriculum we are setting up a stand-alone Stripes UI Server instance that does not communicate with an Okapi back-end.
The `package.json` below builds Stripes with a 'trivial' client bundle.

```shell
$ cat > package.json <<END
{
  "scripts": {
    "build": "stripes build stripes.config.js",
    "stripes": "stripes",
    "start": "stripes dev stripes.config.js"
  },
  "dependencies": {
    "@folio/stripes-core": "^0.0.11",
    "@folio/trivial": "^0.0.2-test"
  }
}
END
```

#### Contents of `stripes.config.js`
`stripes.config.js` contains the configuration details for the Stripes UI Server.
It is referenced in _scripts_ dictionary of `package.json`.
It is a JSON file with three required dictionaries: _okapi_, _config_ and _modules_.
The _okapi_ dictionary specifies the details for connecting to the Okapi Gateway; it is not used in this lesson.
The _config_ dictionary contains two key-value pairs to bypass authentication and authorization checks.
The _modules_ dictionary contains another dictionary of Stripes package and their configuration.
The key in this dictionary is the name of the package to load from the FOLIO UI registry.
The value in this dictionary are parameters that can override the default settings of the Stripes package.

```shell
$ cat > stripes.config.js <<END
module.exports = {
  okapi: {},
  config: { disableAuth: true, hasAllPerms: true },
  modules: {
    '@folio/trivial': {}
  }
};
END
```
#### Build Stripes with the 'trivial' client bundle

Download/update Stripes along with its dependencies and modules, and link them together using the `yarn install` command:

```bash
$ yarn install
  yarn install v0.20.3
  info No lockfile found.
  warning No license field
  [1/4] 🔍  Resolving packages...
  [2/4] 🚚  Fetching packages...
  [3/4] 🔗  Linking dependencies...
  [4/4] 📃  Building fresh packages...
  success Saved lockfile.
  ✨  Done in 40.40s.
```
<div class="vagrant-on-windows-note" markdown="1">
If you are seeing the error _"EPROTO: protocol error, symlink"_ when running Vagrant on Windows, the likely cause is that Vagrant was not launched with administrator privileges.  Be sure to use _Run As Administrator..._ when opening the Command Prompt itself (`cmd.exe`).  See issue [STRIPES-344](https://issues.folio.org/browse/STRIPES-344) for details.
</div>

After the Stripes UI Server is built, run it using the `yarn start` command:

```bash
$ yarn start
  yarn start v0.20.3
  $ stripes dev stripes.config.js
  Listening at http://localhost:3000
  webpack built 554cedd72fbedc2f7499 in 7890ms
```

<div class="vagrant-note" markdown="1">
If you are using the VirtualBox guest machine, set the environment variable
`STRIPES_HOST` before running `yarn start` to allow the Stripes development
server to listen on all interfaces:

    $ STRIPES_HOST=0.0.0.0 yarn start

The Stripes UI Server is now running at http://localhost:3000.
The server will respond after the `webpack built...` message is displayed.
</div>

### Interacting with the Stripes UI Server

The Stripes UI Server homepage at http://localhost:3000 looks like the figure below.

![Stripes homepage](/images/pics/01_Stripes_homepage.png)

There is one app in this basic configuration of the Stripes UI Server -- the "Trivial" app with the green icon.  Click on it to get a form:

![Trivial homepage](/images/pics/01_Trivial_homepage.png)

Type in a greeting and name of your choice and submit the form to see the reply.

![Trivial reply](/images/pics/01_Trivial_reply.png)

This is an example of the Stripes server component communicating with a Stripes browser component.
We have not set up the Okapi part of the FOLIO system, so this interaction is strictly within the Stripes UI Server itself.

The source for the Trivial module is in the stripes-core git repository (https://github.com/folio-org/stripes-core/tree/master/examples/trivial), with the bulk of the work in the [About.js](https://github.com/folio-org/stripes-core/blob/master/examples/trivial/About.js) file.
More details about the state of the object within the module can be seen by viewing the debugging output in the browser's JavaScript console.

![Trivial reply with browser JavaScript console](/images/pics/01_Trivial_reply_with_js_console.png)

### Finish

Now stop this basic Stripes server. Do `Control-C` to exit it.

## Set up the Okapi Users app

In lesson four, we deployed Stripes and demonstrated communication between the browser and the Stripes components.
In lessons two and three, we deployed the Okapi Gateway as well as a test Okapi Module and examined the communication between them.
In this lesson five, we are connecting Stripes to the Okapi Gateway and adding the Users app.

There are two components to the Users app: the Stripes UI component and the Okapi Module component.
We will start first with the Stripes UI component.

NOTE: The Stripes package.json is out-of-date. Also we need the deployment of all user-related backend modules.

So skip ahead to the section about [Adding the mod-users module](#add-mod-users).

### Add the Users app UI component to the Stripes UI Server
Remember in $FOLIO_ROOT/stripes-tutorial-platform we have two configuration files: `package.json` and `stripes.config.js`.
Each will need changes to add the Users app.

#### Modify _package.json_
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

#### Modify _stripes.config.js_
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

#### Rebuild Stripes Server
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
* `ERROR: in module @folio/users operation FETCH on resource users failed, saying: Network request failed`: the Okapi Gateway is not running; see the Java command line at the [start of lesson three](/tutorials/foliodeveloperscurr/#start-the-okapi-gateway)
* `ERROR: in module @folio/users operation FETCH on resource users failed, saying: No such Tenant testlib`: your Okapi Gateway is newly restarted and does not have the _testlib_ tenant; return to [lesson three under the Creating a Tenant heading](/tutorials/foliodeveloperscurr/#creating-a-tenant) to post `okapi-tenant.json` to `/_/proxy/tenants`.
* `ERROR: in module @folio/users operation FETCH on resource users failed, saying: ` (empty error message): you are in the right place.  The Users Okapi Module is not yet [registered](/tutorials/foliodeveloperscurr/#registering-okapi-test-module), [deployed](/tutorials/foliodeveloperscurr/#deploying-okapi-test-module) and/or [enabled](/tutorials/foliodeveloperscurr/#enable-test-module-for-the-testlib-tenant) for the 'testlib' tenant.  The lack of an error message is a [known issue](https://issues.folio.org/browse/STRIPES-224).

If you did not receive an error message, then your Okapi Gateway is properly configured.
The next tutorial section may be review.

### <a id="add-mod-users"/>Add the Users app Okapi Module to the Okapi Gateway

#### Fetch and build the Users app Okapi Module

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

#### Register and Deploy the Users app Okapi Module

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

### Add users to FOLIO

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

## Interact with the FOLIO Stable VM

The previous lessons have provided a quick overview of deploying the parts of the system, and doing some minimal configuration.

This Lesson uses the folio-stable VM to provide a full up-to-date system.
It has all the necessary modules deployed, and users and items already loaded.

If you still have the VirtualBox guest running from the previous lessons, then change to the folio-curriculum directory and do: `vagrant halt; cd ..`

### Start the folio-stable VM

Do this step prior to attending a workshop.

Prepare the box. It will sit beside your other halted folio-curriculum box.

1. Make a clean directory and change into it: `mkdir folio-stable && cd folio-stable`
1. Set up the Vagrantfile: `vagrant init --minimal folio/stable`
1. Launch the VirtualBox guest: `vagrant up`
1. Connect to the VirtualBox guest: `vagrant ssh`

The [folio-ansible](https://github.com/folio-org/folio-ansible) notes explain the purpose of the "stable" box, [show](https://github.com/folio-org/folio-ansible/blob/master/doc/index.md) how to explore the system, view the Okapi logs and Stripes logs, and find the box version information and [release notes](https://app.vagrantup.com/folio/boxes/stable).

### Follow the log files

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

### Interact via web browser

Remember that the Stripes service is forwarded through port 3000, so we can interact with it using our local web browser.

`open http://localhost:3000`

Admin login: diku_admin/admin

View the "About" page near the top-left corner to see the current version information for the services and dependencies.

Browse and view the Users and Items sections.

### Interact via command-line

Open a couple more shell terminal windows to send requests.

Remember that the Okapi service is forwarded through port 9130, so we can interact with it using 'curl' from the host machine.

Save the following script as `run-basic.sh` in your work directory. It provides a basic interaction with Okapi.

Expand this later to do some other queries.
The [API docs](/reference/apispecifications) will be useful.
The [CQL docs](/reference/glossary) will explain the Contextual Query Language (CQL) used by FOLIO.

So start talking, do: `./run-basic.sh`

```shell
#!/bin/bash

# Run some queries against a folio-stable VM.

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
