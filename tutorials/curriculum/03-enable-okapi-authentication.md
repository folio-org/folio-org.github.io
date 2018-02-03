# Enable Okapi Authentication

All real-world uses of Okapi will need to provide authentication and authorization services.
The Okapi Gateway itself does not handle these tasks; rather, it delegates them to one or more Okapi Modules that operates at an early phase of module requests orchestrated by the Okapi Gateway.
In this lesson we will first interact directly with a sample authentication Okapi Module.
Later in the lesson we will register and deploy the sample authentication module on the Okapi Gateway.
Authorization will be covered in a later lesson.

## Interact Directly with Okapi-test-auth-module
_Okapi-test-auth-module_ is a simple module that illustrates authentication in Okapi, and it comes with _okapi-core_.

In a terminal window, start the _okapi-test-auth-module_.

<div class="vagrant-note" markdown="1">
When using the VirtualBox method, you will need to open a terminal window on your host computer, change the working directory to the location of the `Vagrantfile`, and use the `vagrant ssh` command to connect from the host computer to the guest.
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

## Register and Deploy the _Okapi-test-auth-module_ in the Okapi Gateway
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

### Okapi Auth Module ModuleDescriptor

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

### Okapi Auth Module DeploymentDescriptor

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

### Enable Okapi Auth Module on tenant

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
