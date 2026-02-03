---
layout: null
---

# folio-spring-support

Copyright (C) 2020-2023 The Open Library Foundation

This software is distributed under the terms of the Apache License,
Version 2.0. See the file "[LICENSE](LICENSE)" for more information.

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
- [Code structure](#code-structure)
- [Execution Context](#execution-context)
- [Properties](#properties)
- [CQL support](#cql-support)
- [Logging](#logging)
  - [Default logging format](#default-logging-format)
  - [Request and Response Logging](#request-and-response-logging)
- [Custom `/_/tenant` Logic](#custom-_tenant-logic)
  - [`TenantService` Event Methods](#tenantservice-event-methods)
  - [`TenantService` Methods and Fields](#tenantservice-methods-and-fields)
  - [Event Order](#event-order)
    - [Upon Creation](#upon-creation)
    - [Upon Deletion](#upon-deletion)
  - [Sample](#sample)
- [Internationalization](#internationalization)
- [Additional information](#additional-information)
  - [Issue tracker](#issue-tracker)

## Introduction

This is a library that contains the basic functionality and main dependencies required for development of FOLIO modules using Spring framework (also known as "Spring Way").

Please find a step-by-step guide on how to create a new FOLIO Spring based module at https://github.com/folio-org/mod-spring-template

An example of the module based on folio-spring-support could be found at https://github.com/folio-org/folio-sample-modules/tree/master/mod-spring-petstore

## Code structure

The library comprises several submodules that are built as separate artifacts (jar files) and can be integrated into a project as distinct dependencies. This facilitates more precise dependency management depending on the requirements of each project.

The library includes the following submodules:
* **folio-spring-base** - provides fundamental functionality for developing FOLIO modules using the Spring framework.
* **folio-spring-cql** - facilitates CQL querying (refer to the [CQL support](#cql-support) section below)
* ~~**folio-spring-system-user**~~ - (deprecated) provides [functionality](folio-spring-system-user/README.md) for system-user creation and utilization 

## Execution Context

[FolioExecutionContext](folio-spring-base/src/main/java/org/folio/spring/FolioExecutionContext.java) is used to store
essential request headers <i>(in thread local)</i>. Folio Spring Base populates this data
using [FolioExecutionScopeFilter](folio-spring-base/src/main/java/org/folio/spring/scope/filter/FolioExecutionScopeFilter.java).
It is used by [EnrichUrlAndHeadersClient](folio-spring-base/src/main/java/org/folio/spring/client/EnrichUrlAndHeadersClient.java), to provide right tenant id and other headers for outgoing REST requests.
It is also used in [DataSourceSchemaAdvisorBeanPostProcessor](folio-spring-base/src/main/java/org/folio/spring/config/DataSourceSchemaAdvisorBeanPostProcessor.java) for selection of the appropriate schema for sql queries.

FolioExecutionContext is immutable. In order to start new execution context the construct

```
  try (var x = new FolioExecutionContextSetter(currentFolioExecutionContext)) {
    chain.doFilter(request, response);
  }
```

should be used (pick any of the available constructors).

Using try-with-resources is best practice. Not using try-with-resources is error-prone, may result in a wrong tenant and should be avoided. If not using try-with-resources ensure to call `folioExecutionContextSetter.close()` when the execution is finished. Example:

```
  // Not using try-with-resources is discouraged!
  var x = new FolioExecutionContextSetter(currentFolioExecutionContext);
  // do some stuff
  x.close();
```

***CAUTION: FolioExecutionContext should not be used in asynchronous code executions (as it is stored in thread local), unless
the appropriate data is manually set by using `FolioExecutionContextSetter`.***

Example of asynchronous execution:   
```
private final FolioModuleMetadata folioModuleMetadata;

@Async
void ayncMethod(Map<String, Collection<String>> headers) {
  try (var x = new FolioExecutionContextSetter(folioModuleMetadata, httpHeaders)) {
    _your_code_here_
  }
}
```
FOLIO scope implementation supports nested FolioExecutionContexts it means that the following code works correctly for
```
// Autowired
private final FolioModuleMetadata folioModuleMetadata;

// Autowired
protected final FolioExecutionContext context;

void someMethod(Map<String, Collection<String>> headers) {
  Map<String, Collection<String>> headers1 = getHeaderForTenant("Tenant1");
  try (var x = new FolioExecutionContextSetter(folioModuleMetadata, headers1)) {
    String tenant1 = context.getTenantId();
    businessMethod(tenant1);

    Map<String, Collection<String>> headers2 = getHeaderForTenant("Tenant2");
    try (var x = new FolioExecutionContextSetter(folioModuleMetadata, headers2)) {
      String tenant2 = context.getTenantId();
      businessMethod(tenant2);
    }
    
    String tenant1_1 = context.getTenantId();
    assert tenant1.equals(tenant1_1);
  }
}

...

void businessMethod(String tenantId) {
  _do_some_useful_stuff_
  String tenantId = context.getTenantId();

  assert tenant.equals(tenantId);
}
```


## Properties

| Property                                              | Description                                                                                                                                                                                                           | Default       | Example                      |
| ----------------------------------------------------- |-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| ------------- | ---------------------------- |
| `header.validation.x-okapi-tenant.exclude.base-paths` | Specifies base paths to exclude form `x-okapi-tenant` header validation. See [TenantOkapiHeaderValidationFilter.java](folio-spring-base/src/main/java/org/folio/spring/filter/TenantOkapiHeaderValidationFilter.java) | `/admin`      | `/admin,/swagger-ui`         |
| `folio.jpa.repository.base-packages`                  | Specifies base packages to scan for repositories                                                                                                                                                                      | `org.folio.*` | `org.folio.qm.dao`           |
| `folio.logging.request.enabled`                       | Turn on logging for incoming requests                                                                                                                                                                                 | `true`        | `true or false`              |
| `folio.logging.request.level`                         | Specifies logging level for incoming requests                                                                                                                                                                         | `basic`       | `none, basic, headers, full` |
| `folio.logging.feign.enabled`                         | Turn on logging for outgoing requests in feign clients                                                                                                                                                                | `true`        | `true or false`              |
| `folio.logging.feign.level`                           | Specifies logging level for outgoing requests                                                                                                                                                                         | `basic`       | `none, basic, headers, full` |

## CQL support

To have ability to search entities in databases by CQL-queries:

- create repository interface for needed entity
- extend it from `JpaCqlRepository<T, ID>`, where `T` is entity class and `ID` is entity's id class.
- the implementation of the repository will be created by Spring

```java
public interface PersonRepository extends JpaCqlRepository<Person, Integer> {

}
```

Two methods are available for CQL-queries:

```java
public interface JpaCqlRepository<T, ID> extends JpaRepository<T, ID> {

  Page<T> findByCql(String cql, OffsetRequest offset);

  long count(String cql);
}
```

By default a CQL search a `String` field ignores case (= is case insensitive) and ignores accents; this is for consistency with <a href="https://github.com/folio-org/raml-module-builder?tab=readme-ov-file#the-post-tenant-api">RMB based modules</a>. Use the annotations `@RespectCase` and/or `@RespectAccents` in the entity class to change the default.

## Logging

### Default logging format

Library uses [log4j2](https://logging.apache.org/log4j/2.x/) for logging. There are two default log4j2 configurations:

- `log4j2.properties` console/line based logger and it is the default
- `log4j2-json.properties` JSON structured logging

To choose the JSON structured logging by using setting: `-Dlog4j.configurationFile=log4j2-json.properties`
A module that wants to generate log4J2 logs in a different format can create a `log4j2.properties` file in the /resources directory.

### Request and Response Logging

For comprehensive information about HTTP request and response logging, including:
- Request Logging (incoming requests to your application)
- Exchange Logging (outgoing HTTP client requests)
- Logging levels (NONE, BASIC, HEADERS, FULL)
- Configuration examples
- Performance and security considerations

See the [Request Logging Guide](doc/REQUEST_LOGGING.md).

**Quick Configuration:**

```yaml
folio:
  logging:
    request:
      enabled: true
      level: BASIC    # NONE, BASIC, HEADERS, FULL
    exchange:
      enabled: true
      level: BASIC    # NONE, BASIC, HEADERS, FULL

logging:
  level:
    org.folio.spring.filter.IncomingRequestLoggingFilter: DEBUG
    org.folio.spring.client.ExchangeLoggingInterceptor: DEBUG
```

**Note:** In case you have async requests in your module (DeferredResult, CompletableFuture, etc.) then you should disable default logging for requests.

---

## Custom `/_/tenant` Logic

There are many cases where you may want to add custom logic to the
[`/_/tenant` endpoint](https://s3.amazonaws.com/foliodocs/api/folio-spring-base/s/tenant.html),
such as for loading sample data or performing more complex database migration.

In order to do this, you can extend the `TenantService` within your module and override
any of the methods listed below.

### `TenantService` Event Methods

The following methods can be overridden by your module in order to add custom logic around events
relating to tenant creation, updates, and deletion. All of these return `void`.

Many of these accept a `TenantAttributes` parameter which can provide information about the
previous module (`module_from`), the module being upgraded to (`module_to`), as well as any other
`parameters` provided.

:warning: Please note that methods with "update" in the name will be run on updates _as well as_
when new tenants are created. Be especially careful with methods run before Liquibase -- the
database schema could potentially be in an unexpected state, particularly when a new tenant is
created.

| Visibility  | Signature                                 | Purpose                                                                                         |
| ----------- | ----------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `public`    | `loadReferenceData()`                     | Load any reference data (requested with `loadReference=true` parameter)                         |
| `public`    | `loadSampleData()`                        | Load any sample data (requested with `loadSample=true` parameter)                               |
| `protected` | `beforeTenantUpdate(TenantAttributes)`    | Run custom logic before a tenant is created or updated                                          |
| `protected` | `beforeLiquibaseUpdate(TenantAttributes)` | Run custom logic immediately before Liquibase updates are started (after `beforeTenantUpdate`)  |
| `protected` | `afterLiquibaseUpdate(TenantAttributes)`  | Run custom logic immediately before Liquibase updates are finished (before `afterTenantUpdate`) |
| `protected` | `afterTenantUpdate(TenantAttributes)`     | Run custom logic after all update jobs are completed                                            |
| `protected` | `beforeTenantDeletion(TenantAttributes)`  | Run custom logic before a tenant is deleted/purged                                              |
| `protected` | `afterTenantDeletion(TenantAttributes)`   | Run custom logic after a tenant is deleted/purged (the schema will no longer exist)             |

### `TenantService` Methods and Fields

There are two methods that may be of use in your custom logic:

- `boolean tenantExists()` which will check if the database schema for this tenant exists (this
  says nothing about if it is up to date)
- `String getSchemaName()` will construct and return the name of the schema corresponding to the
  module and tenant

These fields will also be provided:

- `JdbcTemplate jdbcTemplate`, for running Postgres queries directly
- `FolioExecutionContext context`, for getting information about the module
- `FolioSpringLiquibase folioSpringLiquibase`, for interacting with Liquibase directly (this
  extends `SpringLiquibase` and may be `null` if Liquibase is not enabled!)

### Event Order

The [events](#tenantservice-event-methods) will be called in the following order:

#### Upon Creation

1. `beforeTenantUpdate`
2. If Liquibase is enabled:
   1. `beforeLiquibaseUpdate`
   2. _Internal logic to apply Liquibase changes_
   3. `afterLiquibaseUpdate`
3. `afterTenantUpdate`
4. `loadReferenceData`, if applicable
5. `loadSampleData`, if applicable

#### Upon Deletion

1. `beforeTenantDeletion`
2. _Internal logic to drop the schema_
3. `afterTenantDeletion`

### Sample

Overriding these methods to add your own custom logic is quite straightforward. Here is an example
of how to override these in your very own `@Service`:

```java
package org.folio.yourmodule.service;

import org.folio.spring.service.TenantService;
import org.folio.tenant.domain.dto.TenantAttributes;
import org.folio.yourmodule.SuperCoolDataRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Primary;
import org.springframework.stereotype.Service;

@Service
@Primary // required to ensure CustomTenantService will be loaded instead of TenantService
public class CustomTenantService extends TenantService {

  protected final SuperCoolDataRepository repository;

  /**
   * Load reference data
   */
  @Override
  protected void loadReferenceData() {
    repository.loadReferenceData();
  }

  /**
   * Add our custom initial data
   */
  @Override
  protected void beforeTenantUpdate(TenantAttributes attributes) {
    // some custom logic for potentially migrating data
  }
}
```

## Internationalization

Translations may be performed in backend modules using the `folio-spring-i18n` library.  For more information, see the [folio-spring-i18n README](folio-spring-i18n/README.md).

## Additional information

### Issue tracker

See project [FOLSPRINGB](https://issues.folio.org/browse/FOLSPRINGB)
at the [FOLIO issue tracker](https://dev.folio.org/guidelines/issue-tracker).

