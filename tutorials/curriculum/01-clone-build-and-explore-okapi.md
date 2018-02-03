# Clone, Build, and Explore Okapi

## Clone and Install Okapi

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

## Interact with the test modules as if you are the Okapi Gateway
The `mvn install` command builds _okapi-core_ (the Okapi Gateway server) and _okapi-common_ (utilities used by both the gateway server and by modules) along with three simple test Okapi Modules.
Before starting the Okapi Gateway, we are going to look at one of the three test Okapi Modules and interact with them as if we are the Okapi Gateway.
Okapi is an implementation of the "API Gateway" microservices pattern.
As such, the Okapi Gateway accepts RESTful requests from clients and routes them through a series of RESTful interfaces ("Okapi Modules") to build a response that is ultimately returned to the client.
(For more details about the Okapi architecture, see the [Okapi Guide and Reference](https://github.com/folio-org/okapi/blob/master/doc/guide.md#architecture).)

To see what this interaction between _okapi-core_ and Okapi Modules looks like, let's start an Okapi Module and send it some requests via `curl`.

### Interact with Okapi-test-module
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

### Interact with Okapi-test-module with headers
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
