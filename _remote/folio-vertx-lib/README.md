---
layout: null
---

# folio-vertx-lib

Copyright (C) 2021-2022 The Open Library Foundation

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

The [Vert.x OpenAPI](https://vertx.io/docs/vertx-web-openapi/java/) unlike
many OpenAPI implementations does not generate any code for you. Everything
happens at run-time. Only requests are validated, not responses.

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
public class MainVerticle extends AbstractVerticle {
  @Override
  public void start(Promise<Void> promise) {
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
    RouterCreator.mountAll(vertx, routerCreators)
        .compose(router ->
            vertx.createHttpServer(so)
                .requestHandler(router)
                .listen(port).mapEmpty())
        .<Void>mapEmpty()
        .onComplete(promise);
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
    return RouterBuilder.create(vertx, "openapi/myapi-1.0.yaml")
        .map(routerBuilder -> {
          handlers(vertx, routerBuilder);
          return routerBuilder.createRouter();
        });
  }

  private void handlers(Vertx vertx, RouterBuilder routerBuilder) {
    routerBuilder
        .operation("postTitles") // operationId in spec
        .handler(ctx -> {
          // doesn't do anything at the moment!
          ctx.response().setStatusCode(204);
          ctx.response().end();
        });
    routerBuilder
        .operation("getTitles")
        .handler(ctx -> getTitles(vertx, ctx)
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

## PostgreSQL

The PostgreSQL support is minimal. There's just enough to perform tenant
separation and most environment variables that are also recognized by RMB
such as `DB_HOST`, `DB_PORT`, `DB_USERNAME`, `DB_PASSWORD`, `DB_DATABASE`,
`DB_MAXPOOLSIZE`, `DB_SERVER_PEM`.

The class [TenantPgPool](core/src/main/java/org/folio/tlib/postgres/TenantPgPool.java) is
a small extension to the PgPool interface. The key method is `TenantPgPool.pool`
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
Example to get books:

```
 private Future<Void> getBooks(Vertx vertx, RoutingContext ctx) {
    RequestParameters params = ctx.get(ValidationHandler.REQUEST_CONTEXT_KEY);
    String tenant = params.headerParameter(XOkapiHeaders.TENANT).getString();
    PgCqlQuery pgCqlQuery = PgCqlQuery.query();
    RequestParameter query = params.queryParameter("query");
    pgCqlQuery.parse(query == null ? null : query.getString());
    pgCqlQuery.addField(new PgCqlField("cql.allRecords", PgCqlField.Type.ALWAYS_MATCHES));
    pgCqlQuery.addField(new PgCqlField("id", PgCqlField.Type.UUID));
    pgCqlQuery.addField(new PgCqlField("title", PgCqlField.Type.FULLTEXT));
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

[SonarQube analysis](https://sonarcloud.io/project/overview?id=org.folio%3Avertx-lib)

### Download and configuration

The built artifacts for this module are available.
See [configuration](https://dev.folio.org/download/artifacts) for repository access.
