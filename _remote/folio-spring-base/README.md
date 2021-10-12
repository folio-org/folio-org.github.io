---
layout: null
---

# folio-spring-base

Copyright (C) 2020 The Open Library Foundation

This software is distributed under the terms of the Apache License,
Version 2.0. See the file "[LICENSE](LICENSE)" for more information.

This is a library (jar) that contains the basic functionality and main dependencies required for development FOLIO modules using Spring framework.

## Properties

| Property | Description | Default | Example |
| -------- | ----------- | --------| --------|
| `header.validation.x-okapi-tenant.exclude.base-paths` | Specifies base paths to exclude form `x-okapi-tenant` header validation.  See [TenantOkapiHeaderValidationFilter.java](src/main/java/org/folio/spring/filter/TenantOkapiHeaderValidationFilter.java) | `/admin` | `/admin,/swagger-ui` |
| `folio.jpa.repository.base-packages` | Specifies base packages to scan for repositories  | `org.folio.*` | `org.folio.qm.dao` |
| `folio.logging.request.enabled` | Turn on logging for incoming requests | `true` | `true or false` |
| `folio.logging.request.level` | Specifies logging level for incoming requests | `basic` | `none, basic, headers, full` |
| `folio.logging.feign.enabled` | Turn on logging for outgoing requests in feign clients  | `true` | `true or false` |
| `folio.logging.feign.level` | Specifies logging level for outgoing requests  | `basic` | `none, basic, headers, full` |

## CQL support
To have ability to search entities in databases by CQL-queries:
 * create repository interface for needed entity 
 * extend it from `JpaCqlRepository<T, ID>`, where `T` is entity class and `ID` is entity's id class.
 * the implementation of the repository will be created by Spring
```java
public interface PersonRepository extends JpaCqlRepository<Person, Integer> {

}
```

Two methods are available for CQL-queries:
```java
public interface JpaCqlRepository<T, ID> extends JpaRepository<T, ID> {

  Page<T> findByCQL(String cql, OffsetRequest offset);

  long count(String cql);
}
```

## Logging
### Default logging format
Library uses [log4j2](https://logging.apache.org/log4j/2.x/) for logging. There are two default log4j2 configurations:
* `log4j2.properties` console/line based logger and it is the default
* `log4j2-json.properties` JSON structured logging
  
To choose the JSON structured logging by using setting: `-Dlog4j.configurationFile=log4j2-json.properties`
A module that wants to generate log4J2 logs in a different format can create a `log4j2.properties` file in the /resources directory.

### Logging for incoming and outgoing requests
By default, logging for incoming and outgoing request enabled. Module could disable it by setting: 
* `folio.logging.request.enabled = false`
* `folio.logging.feign.enabled = false`

Also, it is possible to specify logging level:
`none` - no logs
`basic` - log request method and URI, response status and spent time
`headers` - log all that `basic` and request headers
`full` - log all that `headers` and request and response bodies

***Note:*** *In case you have async requests in your module (DeferredResult, CompletableFuture, etc.) then you should disable default logging for requests.* 
#### Log examples:
* basic:
```text
18:41:18 [<requestId>] [<tenandId>] [<userId>] [<moduleId>] INFO  LoggingRequestFilter ---> PUT /records-editor/records/c9db5d7a-e1d4-11e8-9f32-f2801f1b9fd1 null
18:41:19 [<requestId>] [<tenandId>] [<userId>] [<moduleId>] INFO  LoggingRequestFilter <--- 202 in 753ms
```
* headers:
```text
18:44:23 [<requestId>] [<tenandId>] [<userId>] [<moduleId>] INFO  LoggingRequestFilter ---> PUT /records-editor/records/c9db5d7a-e1d4-11e8-9f32-f2801f1b9fd1 null
18:44:23 [<requestId>] [<tenandId>] [<userId>] [<moduleId>] INFO  LoggingRequestFilter x-okapi-url: http://localhost:50017
18:44:23 [<requestId>] [<tenandId>] [<userId>] [<moduleId>] INFO  LoggingRequestFilter x-okapi-tenant: <tenandId>
18:44:23 [<requestId>] [<tenandId>] [<userId>] [<moduleId>] INFO  LoggingRequestFilter x-okapi-request-id: <requestId>
18:44:23 [<requestId>] [<tenandId>] [<userId>] [<moduleId>] INFO  LoggingRequestFilter x-okapi-user-id: <userId>
18:44:23 [<requestId>] [<tenandId>] [<userId>] [<moduleId>] INFO  LoggingRequestFilter content-type: application/json; charset=UTF-8
18:44:23 [<requestId>] [<tenandId>] [<userId>] [<moduleId>] INFO  LoggingRequestFilter ---> END HTTP
18:44:24 [<requestId>] [<tenandId>] [<userId>] [<moduleId>] INFO  LoggingRequestFilter <--- 202 in 786ms
```
* full:
```text
18:46:17 [<requestId>] [<tenandId>] [<userId>] [<moduleId>] INFO  LoggingRequestFilter ---> PUT /records-editor/records/c9db5d7a-e1d4-11e8-9f32-f2801f1b9fd1 null
18:46:17 [<requestId>] [<tenandId>] [<userId>] [<moduleId>] INFO  LoggingRequestFilter x-okapi-url: http://localhost:53146
18:46:17 [<requestId>] [<tenandId>] [<userId>] [<moduleId>] INFO  LoggingRequestFilter x-okapi-tenant: <tenandId>
18:46:17 [<requestId>] [<tenandId>] [<userId>] [<moduleId>] INFO  LoggingRequestFilter x-okapi-request-id: <requestId>
18:46:17 [<requestId>] [<tenandId>] [<userId>] [<moduleId>] INFO  LoggingRequestFilter x-okapi-user-id: <userId>
18:46:17 [<requestId>] [<tenandId>] [<userId>] [<moduleId>] INFO  LoggingRequestFilter content-type: application/json; charset=UTF-8
18:46:17 [<requestId>] [<tenandId>] [<userId>] [<moduleId>] INFO  LoggingRequestFilter Body: {"parsedRecordId":"c9db5d7a-e1d4-11e8-9f32-f2801f1b9fd1","parsedRecordDtoId":"c56b70ce-4ef6-47ef-8bc3-c470bafa0b8c","suppressDiscovery":false}
18:46:17 [<requestId>] [<tenandId>] [<userId>] [<moduleId>] INFO  LoggingRequestFilter ---> END HTTP
18:46:18 [<requestId>] [<tenandId>] [<userId>] [<moduleId>] INFO  LoggingRequestFilter <--- 202 in 714ms
18:46:18 [<requestId>] [<tenandId>] [<userId>] [<moduleId>] INFO  LoggingRequestFilter Body: 
18:46:18 [<requestId>] [<tenandId>] [<userId>] [<moduleId>] INFO  LoggingRequestFilter <--- END HTTP
```