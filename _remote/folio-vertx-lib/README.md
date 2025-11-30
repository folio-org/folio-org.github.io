---
layout: null
---

# folio-vertx-lib

Copyright (C) 2021-2025 The Open Library Foundation

This software is distributed under the terms of the Apache License,
Version 2.0. See the file "[LICENSE](LICENSE)" for more information.

## Introduction

[folio-vertx-lib](https://github.com/folio-org/folio-vertx-lib)
is a library for developing FOLIO modules based on Vert.x. This is a
library, not a framework, with utilities such as:

 * OpenAPI support
 * Tenant API 2.0 support
 * PostgreSQL utilities
 * CQL support

## Main Verticle

The [Vert.x OpenAPI](https://vertx.io/docs/vertx-openapi/java/) unlike
many OpenAPI implementations does not generate any code for you. Everything
happens at run-time. Only requests are validated, not responses.

The OpenAPI implementaion of Vert.x 5 does not allow external references - even
if they are local files [ref](https://vertx.io/docs/vertx-openapi/java/#_openapicontract).
If the OpenAPI spec in use has local file references the YAML must be preprocessed with the
openapi-deref-plugin. See the [openapi-deref-plugin](#plugin-openapi-deref-plugin) section
for details about handling external references in OpenAPI specifications.

Place your OpenAPI specification and auxiliary files somewhere in `resources`,
such as `resources/openapi`.

In the following example, we will
use OpenAPI spec
[books-1.0.yaml](mod-example/src/main/resources/openapi/books-1.0.yaml).
The code snippets shown are from:
[MainVerticle](mod-example/src/main/java/org/folio/tlib/example/MainVerticle.java)
,
[BookService](mod-example/src/main/java/org/folio/tlib/example/service/BookService.java)
and
[BookStorage](mod-example/src/main/java/org/folio/tlib/example/storage/BookStorage.java).

Unlike
[RMB](https://github.com/folio-org/raml-module-builder), you define
MainVerticle yourself - no fancy initializers - you decide.

Example:
```
public class MainVerticle extends VerticleBase {
  @Override
  public Future<?> start() {
    TenantPgPool.setModule("mod-mymodule"); // PostgreSQL - schema separation

    final int port = Integer.parseInt( // listening port
        Config.getSysConf("http.port", "port", "8081", config()));

    MyApi myApi = new MyApi(); // your API, construct the way you like
    // routes for your stuff, tenant API and health
    RouterCreator [] routerCreators = {
        myApi,
        new Tenant2Api(myApi),
        new HealthApi(),
    };
    HttpServerOptions so = new HttpServerOptions()
        .setHandle100ContinueAutomatically(true);
    // combine all routes and start server
    return RouterCreator.mountAll(vertx, routerCreators, "mod-mymodule")
        .compose(router -> vertx.createHttpServer(so)
            .requestHandler(router)
            .listen(port));
  }
}
```

## Your API

Your API must implement [RouterCreator](core/src/main/java/org/folio/tlib/RouterCreator.java)
and, optionally, [TenantInitHooks](core/src/main/java/org/folio/tlib/TenantInitHooks.java)
if your implementation has storage and that storage must be prepared for a
tenant.

With the API there is a corresponding OpenAPI specification.

The `RouterCreator` interface has just one method `createRouter` where you
return a Router for your implementation. Normally that's created for you by the
OpenAPI library, but you can also define it yourself.

For an OpenAPI based implementation it could look as follows:

```
public MyApi implements RouterCreator, TenantInitHooks {
  @Override
  public Future<Router> createRouter(Vertx vertx) {
    return OpenAPIContract.from(vertx, "openapi/myapi-1.0.yaml")
      .map(contract -> {
        RouterBuilder routerBuilder = RouterBuilder.create(vertx, contract);
        handlers(vertx, routerBuilder);
        return routerBuilder.createRouter();
      });
  }

  private void handlers(Vertx vertx, RouterBuilder routerBuilder) {
    routerBuilder
        .getRoute("postTitles") // operationId in spec
        .addHandler(ctx -> {
          // doesn't do anything at the moment!
          ctx.response().setStatusCode(204);
          ctx.response().end();
        });
    routerBuilder
        .getRoute("getTitles")
        .addHandler(ctx -> getTitles(vertx, ctx)
            .onFailure(cause -> {
              ctx.response().setStatusCode(500);
              ctx.response().end(cause.getMessage());
            }));
  }
}
```

To support tenant init, your module should implement `preInit` and `postInit`.

These methods takes tenant ID and
[tenant attributes object](core/src/main/resources/openapi/schemas/tenantAttributes.json).

The `preInit` job should be "fast" and is a way for the module to check if the
operation can be started.. ("pre-check"). The postInit should perform the
actual migration.

The Tenant2Api implementation deals with purge (removes schema with cascade).
Your implementation should only consider upgrade/downgrade. On purge,
`preInit` is called, but `postInit` is not.

## Plugin openapi-deref-plugin

The purpose of the openapi-deref-plugin is to de-reference `$ref` references in the OpenAPI
specification. The result is one YAML file with all resources embedded. If there are
only references to components inside the OpenAPI YAML file from the beginning, it is not
necessary to use this plugin.

If the OpenAPI specification is located in `resources/openapi` (recommended), then
the minimal way to use the plugin is to use:

```
  <plugin>
    <groupId>org.folio</groupId>
    <artifactId>openapi-deref-plugin</artifactId>
    <version>4.0.0</version>
    <executions>
      <execution>
        <id>dereference-books</id>
        <goals>
          <goal>dereference</goal>
        </goals>
        <phase>generate-resources</phase>
      </execution>
    </executions>
  </plugin>
```

The configuration has the following properties:

  * `input` : glob-path for input files to search. Default value is `${basedir}/src/main/resources/openapi/*.yaml`
  * `output` : output directory. Default value is `${project.build.directory}/classes/openapi`.

As an example if there are OpenAPI specs in test resources, the `extensions` list could be extended with:

```
  <execution>
    <id>dereference-echo</id>
    <goals>
      <goal>dereference</goal>
    </goals>
    <phase>generate-resources</phase>
    <configuration>
      <input>${project.basedir}/src/test/resources/openapi/*.yaml</input>
      <output>${project.build.directory}/test-classes/openapi</output>
    </configuration>
  </execution>
```

## PostgreSQL

The PostgreSQL support is minimal.
There's just enough to perform tenant and module separation.

The following environment variables are supported:

- `DB_HOST`
- `DB_PORT`
- `DB_USERNAME`
- `DB_PASSWORD`
- `DB_DATABASE`
- `DB_MAXPOOLSIZE`
- `DB_MAX_LIFETIME`
- `DB_RECONNECTATTEMPTS`
- `DB_RECONNECTINTERVAL`
- `DB_CONNECTIONRELEASEDELAY`
- `DB_SERVER_PEM`

These are also recognized by by RMB. Refer to the
[Environment Variables](https://github.com/folio-org/raml-module-builder#environment-variables)
section of RMB.

The class [TenantPgPool](core/src/main/java/org/folio/tlib/postgres/TenantPgPool.java) is
a small extension to the [Pool](https://vertx.io/docs/apidocs/io/vertx/sqlclient/Pool.html)
interface. The key method is `TenantPgPool.pool`
for constructing a pool for the current tenant. From that point, rest is plain
Vert.x pg client. However, the schema should be used when referring to tables, etc.
Use the `getSchema` method for that.

The `TenantPgPool.setModule` *must* be called before first use as is done in
MainVerticle example earlier.

To illustrate these things, consider a module that prepares a table in
tenant init.

```
  @Override
  public Future<Void> postInit(Vertx vertx, String tenant, JsonObject tenantAttributes) {
    if (!tenantAttributes.containsKey("module_to")) {
      return Future.succeededFuture(); // doing nothing for disable
    }
    TenantPgPool pool = TenantPgPool.pool(vertx, tenant);
    return pool.query(
            "CREATE TABLE IF NOT EXISTS " + pool.getSchema() + ".mytable "
                + "(id UUID PRIMARY key, title text)")
        .execute().mapEmpty();
  }
```

## CQL

For CQL support *all* fields recognized must be explicitly defined.
Undefined CQL fields are rejected.

Example definition:

```
    PgCqlDefinition pgCqlDefinition = PgCqlDefinition.create();
    pgCqlDefinition.addField("cql.allRecords", new PgCqlFieldAlwaysMatches());
    pgCqlDefinition.addField("id", new PgCqlFieldUuid());
    pgCqlDefinition.addField("title", new PgCqlFieldText().withFullText());
```

This definition can then be used in a handler to get books:

```
 private Future<Void> getBooks(Vertx vertx, RoutingContext ctx) {
    String tenant = TenantUtil.tenant(ctx);
    List<String> query = ctx.queryParam("query");
    PgCqlQuery pgCqlQuery = pgCqlDefinition.parse(query.isEmpty() ? null : query.get(0));

    TenantPgPool pool = TenantPgPool.pool(vertx, tenant);
    String sql = "SELECT * FROM " + pool.getSchema() + ".mytable";
    String where = pgCqlQuery.getWhereClause();
    if (where != null) {
      sql = sql + " WHERE " + where;
    }
    String orderBy = pgCqlQuery.getOrderByClause();
    if (orderBy != null) {
      sql = sql + " ORDER BY " + orderBy;
    }
    return pool.query(sql).execute().onSuccess(rows -> {
      RowIterator<Row> iterator = rows.iterator();
      JsonArray books = new JsonArray();
      while (iterator.hasNext()) {
        Row row = iterator.next();
        books.add(new JsonObject()
            .put("id", row.getUUID("id").toString())
            .put("title", row.getString("title"))
        );
      }
      ctx.response().putHeader("Content-Type", "application/json");
      ctx.response().setStatusCode(200);
      JsonObject result = new JsonObject().put("books", books);
      ctx.response().end(result.encode());
    }).mapEmpty();
  }
```

CQL queries of the form `FIELD=""` have a special meaning; they find all records where the named field is NOT NULL. (This behaviour is the same as in the old RAML Module Builder.) To search for records where the field is present but empty, the double-equal operator can be used: `FIELD==""`.

## Additional information

### Issue tracker

See project [VERTXLIB](https://issues.folio.org/browse/VERTXLIB)
at the [FOLIO issue tracker](https://dev.folio.org/guidelines/issue-tracker).

### Code of Conduct

Refer to the Wiki [FOLIO Code of Conduct](https://wiki.folio.org/display/COMMUNITY/FOLIO+Code+of+Conduct).

### API documentation

API descriptions:

 * [OpenAPI](core/src/main/resources/openapi/)
 * [Schemas](core/src/main/resources/openapi/schemas/)

Generated [API documentation](https://dev.folio.org/reference/api/#folio-vertx-lib).

### Code analysis

[SonarQube analysis](https://sonarcloud.io/project/overview?id=org.folio%3Afolio-vertx-lib)

### Download and configuration

The built artifacts for this module are available.
See [configuration](https://dev.folio.org/download/artifacts) for repository access.
