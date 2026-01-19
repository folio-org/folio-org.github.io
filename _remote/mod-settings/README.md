---
layout: null
---

# mod-settings

Copyright (C) 2022-2026 The Open Library Foundation

This software is distributed under the terms of the Apache License,
Version 2.0. See the file "[LICENSE](LICENSE)" for more information.

## Introduction

mod-settings is a key-value store that provides a more secure
configuration system than the old mod-configuration.

See [Fixing the security problem in mod-configuration](https://github.com/MikeTaylor/folio-docs/blob/main/doc/fixing-mod-configuration.md)
for more information.

It is currently implemented with PostgresQL as storage.

A setting consists of these required properties

* `id`: unique identifier (UUID)
* `scope`: it is a namespace for the setting. This could be module
* `key`: a readable identifier; not necessarily for display
* `value`: any type (integer, string, object, array)

And optionally:

* `userId`: the owner of the setting

We call settings without userId 'global'. Global settings must be unique
for scope and key. Non-global settings must be unique for scope, key
and userId.

Settings are protected by permissions.

In order to write to a global setting, the client must have permission
`mod-settings.global.write.`scope, where scope is used in the setting.
To read this type of setting, the client must have
`mod-settings.global.read.`scope.

In order to write to a setting with any userId, which we call a user
setting, the client must have permission `mod-settings.users.write.`scope ,
where scope is used in the setting. To read this type of setting,
the client must have `mod-settings.users.read.`scope.

In order to write to user's own setting, the client must have permission
`mod-settings.owner.write.`scope, where scope is used in the setting.
To read this type of setting, the client must have
`mod-settings.owner.read.`scope.

With 'read' in this context we mean able to read the content of
the setting. With 'write' in this context we modify storage
using POST, PUT and DELETE.

We expect that most users will have read-write permission on their own
settings, and read-only permission on global entries.

The API is CRUD-like, but with some important changes for some.

Create a setting [with](https://s3.amazonaws.com/foliodocs/api/mod-settings/settings.html#operation/postSetting):

    POST /settings/entries

This is write operation and returns 204 if successful. The
`id` property is required and must be supplied by the client.

Fetch a particular setting [with](https://s3.amazonaws.com/foliodocs/api/mod-settings/settings.html#operation/getSetting):

    GET /settings/entries/{id}

This fetch is protected by permissions. If the client does not
have permission to read the setting with the scope or if the setting
does not exist, then mod-settings will return a 404 failure. It is a
deliberate choice to not distinguish between these two cases.

Get a list of settings [with](https://s3.amazonaws.com/foliodocs/api/mod-settings/settings.html#operation/getSettings):

    GET /settings/entries

The latter takes optional `query`, `limit` (default 10), `offset` (default 0) parameters.
Query is expressed in Contextual Query Language
([CQL](https://dev.folio.org/reference/glossary/#cql))
and supports queries on the `id`, `scope`,
`key` and `userId` fields. Query terms can mostly only be used in
exact-value matching: the exception is that the key field supports
right-truncated searches, e.g. `scope=foo and key=bar*` to find all
entries in the `foo` scope that begin with `bar`.

The GET operations are "read" operations. The entries returned
are limited by client permissions.

Update a setting
[with](https://s3.amazonaws.com/foliodocs/api/mod-settings/settings.html#operation/putSetting):

    PUT /settings/entries/{id}

This returns 204 if the setting was updated. This is strictly "write", i.e.
does not return the newly modified setting.

Delete a setting
[with](https://s3.amazonaws.com/foliodocs/api/mod-settings/settings.html#operation/deleteSetting):

    DELETE /settings/entries/{id}

This is a write operation and returns 204 if the setting was deleted.

It's also possible to upload (or "import") settings
[with](https://s3.amazonaws.com/foliodocs/api/mod-settings/settings.html#operation/uploadSettings):

    PUT /settings/upload

Settings are created/updated with this service. The provided settings must
not include an identifier. An identifier will be assigned by the server when
necessary.

## Compilation

Requirements:

* Java 17 or later
* Maven 3.6.3 or later
* Docker (unless `-DskipTests` is used)

Note: Debian package maven-3.6.3-1
[does not work with Java16/Java17](https://bugs.launchpad.net/ubuntu/+source/maven/+bug/1930541)


You need `JAVA_HOME` set, e.g.:

   * Linux: `export JAVA_HOME=$(readlink -f /usr/bin/javac | sed "s:bin/javac::")`
   * macOS: `export JAVA_HOME=$(/usr/libexec/java_home -v 17)`

Build all components with: `mvn install`

## Server

You will need Postgres 12 or later.

You can create an empty database and a user with, e.g:

```
CREATE DATABASE folio_modules;
CREATE USER folio WITH CREATEROLE PASSWORD 'folio';
GRANT ALL PRIVILEGES ON DATABASE folio_modules TO folio;
```

The module's database connection is then configured by setting environment
variables:
`DB_HOST`, `DB_PORT`, `DB_USERNAME`, `DB_PASSWORD`, `DB_DATABASE`,
`DB_MAXPOOLSIZE`, `DB_SERVER_PEM`.

Once configured, start the module with:

```
java -Dport=8081 -jar target/mod-settings-fat.jar
```

## Running with Docker

If you feel adventurous and want to run mod-settings in a docker container, build the container first:

```
docker build -t mod-settings:latest .
```

And run with the module port exposed (`8081` by default):

```
docker run -e DB_HOST=host.docker.internal \
  -e DB_USERNAME=folio \
  -e DB_PASSWORD=folio \
  -e DB_DATABASE=folio_modules \
  -p 8081:8081 --name settings mod-settings:latest
```

**Note**: The magic host `host.docker.internal` is required to access
the DB and may be only available in Docker Desktop.
If it's not defined you can specify it by passing
`--add-host=host.docker.internal:<docker bridge net IP>` to the run command.

**Note**: Those docker build and run commands do work as-is with
[Colima](https://github.com/abiosoft/colima).

## Additional information

### Issue tracker

See project [MODSET](https://folio-org.atlassian.net/browse/MODSET)
at the [FOLIO issue tracker](https://dev.folio.org/guidelines/issue-tracker).

### Code of Conduct

Refer to the Wiki
[FOLIO Code of Conduct](https://wiki.folio.org/display/COMMUNITY/FOLIO+Code+of+Conduct).

### ModuleDescriptor

See the [ModuleDescriptor](descriptors/ModuleDescriptor-template.json)
for the interfaces that this module requires and provides, the permissions,
and the additional module metadata.

### API documentation

API descriptions:

 * [OpenAPI](src/main/resources/openapi/settings.yaml)
 * [Schemas](src/main/resources/openapi/schemas/)

Generated [API documentation](https://dev.folio.org/reference/api/#mod-settings).

### Code analysis

[SonarQube analysis](https://sonarcloud.io/dashboard?id=org.folio%3Amod-settings).

### Download and configuration

The built artifacts for this module are available.
See [configuration](https://dev.folio.org/download/artifacts) for repository access,
and the Docker images for [released versions](https://hub.docker.com/r/folioorg/mod-settings/)
and for [snapshot versions](https://hub.docker.com/r/folioci/mod-settings/).

