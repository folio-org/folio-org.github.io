---
layout: tutorials
title: RAML Module Builder
heading: RAML Module Builder
permalink: /tutorials/ramlmodulebuilder/
---

We need a tool called _[RAML Module Builder](https://github.com/folio-org/raml-module-builder)_.
[RAML](http://raml.org/) is the _RESTful API Modeling Language_: it is a language for defining RESTful APIs in a concise, machine-readable form that enables easy reusability.
RAML Module Builder reads a RAML file and generates Java code that reduces much of the "boilerplate" work required when creating an Okapi module.

### Build _RAML Module Builder_
```shell
$ cd $FOLIO_ROOT
$ git clone --recursive https://github.com/folio-org/raml-module-builder.git
  Cloning into 'raml-module-builder'...
  remote: Counting objects: 6243, done.
  remote: Total 6243 (delta 0), reused 0 (delta 0), pack-reused 6243
  Receiving objects: 100% (6243/6243), 2.92 MiB | 752.00 KiB/s, done.
  Resolving deltas: 100% (2725/2725), done.
  Submodule 'raml-util' (https://github.com/folio-org/raml.git) registered for path 'raml-util'
  Cloning into '/Users/peter/code/folio-trial/raml-module-builder/raml-util'...
  remote: Counting objects: 409, done.
  remote: Compressing objects: 100% (7/7), done.
  remote: Total 409 (delta 2), reused 0 (delta 0), pack-reused 397
  Receiving objects: 100% (409/409), 85.73 KiB | 0 bytes/s, done.
  Resolving deltas: 100% (238/238), done.
  Submodule path 'raml-util': checked out 'f64234a0f482afdc5d2ea9e1e9f9ff33765f897e'
$ cd raml-module-builder
$ mvn install
  [...]
  [INFO] ------------------------------------------------------------------------
  [INFO] Reactor Summary:
  [INFO]
  [INFO] raml-module-builder ................................ SUCCESS [  1.095 s]
  [INFO] domain-models-api-aspects .......................... SUCCESS [  1.582 s]
  [INFO] domain-models-interface-extensions ................. SUCCESS [  0.735 s]
  [INFO] domain-models-api-interfaces ....................... SUCCESS [  3.379 s]
  [INFO] rules .............................................. SUCCESS [  2.330 s]
  [INFO] domain-models-runtime .............................. SUCCESS [ 48.136 s]
  [INFO] ------------------------------------------------------------------------
  [INFO] BUILD SUCCESS
  [INFO] ------------------------------------------------------------------------
  [INFO] Total time: 57.389 s
  [INFO] Finished at: 2017-02-24T16:30:33-05:00
  [INFO] Final Memory: 95M/660M
  [INFO] ------------------------------------------------------------------------
```