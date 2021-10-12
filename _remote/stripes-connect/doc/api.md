---
layout: null
---

# The Stripes Connect API

&copy; Index Data, 2016-2020.

<!-- md2toc -l 2 api.md -->
* [Introduction](#introduction)
    * [Note](#note)
* [The Connection Manifest](#the-connection-manifest)
    * [Resource types](#resource-types)
        * [Local resources](#local-resources)
        * [REST resources](#rest-resources)
        * [Okapi resources](#okapi-resources)
    * [Example manifest](#example-manifest)
    * [Path interpretation](#path-interpretation)
        * [A note on terminology](#a-note-on-terminology)
        * [Overview](#overview)
        * [Text substitution](#text-substitution)
        * [Fallbacks](#fallbacks)
        * [Example path](#example-path)
        * [Functional paths and parameters](#functional-paths-and-parameters)
* [Connecting the component](#connecting-the-component)
* [Using the connected component](#using-the-connected-component)
    * [Mutators](#mutators)
    * [Error handling](#error-handling)
        * [Catching rejected promises](#catching-rejected-promises)
        * [Detecting failed mutations](#detecting-failed-mutations)
* [Appendices: for developers](#appendices-for-developers)
    * [Appendix A: how state is stored](#appendix-a-how-state-is-stored)
    * [Appendix B: unresolved issues](#appendix-b-unresolved-issues)
        * [One vs. Many](#one-vs-many)
        * [Metadata](#metadata)
        * [Object counts](#object-counts)
    * [Appendix C: worked-through example of connected component](#appendix-c-worked-through-example-of-connected-component)
    * [Appendix D: walk-through of state-object changes during a CRUD cycle](#appendix-d-walk-through-of-state-object-changes-during-a-crud-cycle)



## Introduction

Stripes Connect is one of the most important parts of the Stripes
toolkit for building FOLIO UIs. It provides the connection between the
UI and the underlying services -- most usually, Okapi (the FOLIO
middleware), though other RESTful web services are also supported.

A Stripes UI is composed of
[React](https://facebook.github.io/react/)
components. (You will need to learn at least the basics of React in
order to use Stripes.) Any component may use the services of Stripes
Connect to automate communication with back-end services. A component
that does this is known as a "connected component".

In order to take advantage of Stripes Connect, a component must do two
things: declare a _manifest_, which describes what data elements it
wants to manage and how to link them to services; and call the
`connect()` method on itself.


### Note

This document describes an API that is still in motion. The present
version of the code implements something similar to this, but not
identical. Further changes are likely.



## The Connection Manifest

The manifest is provided as a static member of the component class. It
is a JavaScript object in which the keys are the names of resources to
be managed, and the corresponding values are objects containing
configuration that specifies how to deal with them:

        static manifest = {
          'bibs': { /* ... */ },
          'items': { /* ... */ },
          'patrons': { /* ... */ }
        };

Each resource is a piece of data -- perhaps a single string, perhaps a
set of structured records. The values of all resources are available
to components as the `resources` property -- in this case,
`this.props.resources.bibs` etc.

### Resource types

Each resource's configuration has several keys. The most important of these is `type`,
which determines how the associated data is treated. Currently, three
types are supported:

* `local`: a local resource (client-side only), which is not persisted
  by means of a service.
* `okapi`: a resource that is persisted by means of a FOLIO service
  mediated by Okapi.
* `rest`: a resource persisted by some RESTful service other than
  Okapi.

(In fact, the `okapi` type is merely a special case of `rest`, in
which defaults are provided to tailor the RESTful dialogues in
accordance with Okapi's conventions.)


#### Local resources

A local resource needs no configuration items -- not even an explicit
`type`, since the default type is `local`. So its configuration can
simply be specified as an empty object:

        static manifest = {
          'someLocalResource': {}
        }


#### REST resources

REST resources are configured by the following additional keys in
addition to `'type':'rest'`:

* `root`: the base URL of the service that persists the data.

* `path`: the path for this resource below the specified root. The
  path consists of one or more `/`-separated components. See
  [the **Path Interpretation** section](#path-interpretation) below
  for details on how this is handled.

* `params`: A JavaScript object containing named parameters to be
  supplied as part of the URL. These are joined with `&` and appended
  to the path with a `?`.
  The root, path and params together make up the URL that is
  addressed to maintain the resource.

* `limitParam`: the name of the parameter controlling the number of results per
  request.

* `offsetParam`: the name of the parameter controlling the number of results to
  skip.

* `headers`: A JavaScript object containing HTTP headers: the keys are
  the header names and the values are their content.

* `records`: The name of the field in the returned JSON that contains
  the records. Typically the JSON response from a web service is not
  itself an array of records, but an object containing metadata about
  the result (result-count, etc.) and a sub-array that contains the
  actual records. The `records` item specifies the name of that
  sub-array within the top-level response object.

* `recordsRequired`: The maximum number of records to fetch. If further records
  are available, multiple requests will be made until this count is satisfied
via limitParam/offsetParam.

* `perRequest`: How many records to fetch per request (via limitParam).

* `pk`: The name of the key in the returned records that contains
  the primary key. (Defaults to `id` for both REST and Okapi
  resources.)

* `clientGeneratePk`: a boolean indicating whether the client must
  generate a "sufficiently unique" primary key for newly created
  records, or must accept one that is supplied by the service in
  response to a create request. Default: `true`.

* `fetch`: a component that adds a new record to an end-point would usually not
  need to pre-fetch from that resource. To avoid that, it can set this to
  false. If set to a function, it will be passed the current props of the
  connected component and the return value used to determine if the resource
  should be fetched. Default: `true`.

* `accumulate`: A boolean indicating whether to return a GET value on the
  resource, which allows it to be used in code that expects to receive a
  promise. Default: `false`.

* `abortable`: A boolean indicating whether given resource can be
  aborted manually by calling `resource.cancel()`. Default `false`.

* `abortOnUnmount`: A boolean which can be used to control if the given pending
  resource should be aborted during component unmount. Default `false`.

* `permissionsRequired`: A string (or an array of strings) indicating the list
  of permissions required for the given resource to be fetched.

* `shouldRefresh`: An optional function which can be used to indicate if the
given resource should be refreshed when another resource is mutated. The function is passed
the `resource` itself and the refresh `action`. The `action` contains the standard `type`, `meta`,
etc fields. The `action.meta` additionally contains an `originatingActionType` string
that contains the action type that resulted in this refresh request. Eg, `@@stripes-connect/DELETE_SUCCESS`.

* `resultOffset`: A number, interpolated string, or function indicating what offset
  into the results list should be fetched. This is an optional workflow that allows
  fetching of just the next page rather than re-requesting all pages. Note that this
  workflow is not supported for infinite-scroll due to the risk of out-of-order pages.
  For example, a `MultiColumnList` tied to a resource using `resultOffset` should have
  its `pagingType` prop set to `click` rather than `scroll`.

In addition to these principal pieces of configuration, which apply to
all operations on the resource, these values can be overridden for
specific HTTP operations: the entries `GET`, `POST`, `PUT`, `DELETE`
and `PATCH`, if supplied, are objects containing configuration (using
the same keys as described above) that apply only when the specified
operation is used.

Similarly, the same keys provided in `staticFallback` will be used when
dynamic portions of the config are not satisfied by the current state
-- see [below](#text-substitution-and-fallback).


#### Okapi resources

Okapi resources are REST resources, but with defaults set to make
connecting to Okapi convenient. In particular, default headers are set
appropriately for the `GET`, `POST`, `PUT` and `DELETE` operations.

(Also, special-case code that understands Okapi-specific state and
configuration ensures that the correct tenant-ID is sent with each
request, and that the `root` is defaulted to a globally-configured
address pointing to an Okapi instance.)


### Example manifest

This manifest (from the Okapi Console component that displays the
health of running modules) defines two Okapi resources, `health` and
`modules`, providing paths for both of them that are interpreted
relative to the default root. In the modules response, the primary key
is the default, `id`; but in the health response, it is `srvcId`, and
the manifest must specify this.

        static manifest = Object.freeze({
          health: {
            type: 'okapi',
            pk: 'srvcId',
            path: '_/discovery/health'
          },
          modules: {
            type: 'okapi',
            path: '_/proxy/modules'
          }
        });

(It is conventional to freeze manifests -- making them immutable -- to
document and enforce the fact that they do not change once
created. See [Thinking in Stripes](https://github.com/folio-org/stripes/blob/master/doc/dev-guide.md#thinking-in-stripes).)


### Path interpretation

#### A note on terminology

Since we will be talking a lot about URLs in this section, to avoid
confusion we must introduce little bit of terminology. We use _UI URL_
to refer to the URL of the user interface, which the human user can
see in the URL bar of the browser -- for example,

> `http://ui.folio.org:3000/users?query=price&sort=Name&filterActive=true`

And we use _back-end URL_ to refer to the URLs of resources provided
by back-end services such as Okapi, which the UI itself invokes, and
which are not visible to the human user -- for example,

> `http://okapi.folio.org:9130/users?query=title=(username="price*" or personal.first_name="price*" or personal.last_name="price*") and active=true sortby personal.last_name personal.first_name`

The purpose of the `path` in a manifest resource (in conjunction with
the `root`) is to specify how the back-end URL is generated.

#### Overview

The strings provided as `path`s in manifests can sometimes be simple
constants, such as `_/proxy/modules` or `item-storage/items`.
(Such constant paths are often used as part of a `staticFallback`.)

However, more often the precise path varies with aspects of the state,
such as components of the UI URL's path or query, or the values of
local resources. This state-dependent path construction can be
expressed in two ways: most often by substituting values directly into
a template string; and when the requirements are complex, by
calling a function to construct the string from the state.

#### Text substitution

The four different kinds of state can be substituted into path
strings using four different but related syntaxes:

* `:{name}` -- interpolates the value of the named path-component from
  the UI URL, as extracted by React Router. For example, if the React
  Router path is `/view/:userid` then the path for accessing the
  back-end web-service can be expressed as `users/:{userid}` Then when
  the UI is being accessed as (for example)
  `http://ui.folio.org:3000/users/view/45`, the path will be resolved as
  `users/45`.

* `?{name}` -- interpolates the value of the named query parameter
  from the UI URL. For example, if the path is expressed as
  `item-storage?query=?{q}` and the UI is accessed at
  `http://ui.folio.org:3000/items?q=water`, the path will be resolved as
  `item-storage?query=water`.

* `%{name}` -- interpolates the value of the named local resource (see
  [above](#local-resources) on local resources). In general, the
  approach here is to store state in a local resource rather than in
  React-component state. Given a local resource `sortOrder`, this can
  be done using something along the lines of
  `this.props.mutator.sortOrder.replace('title')`, most likely from an
  event hander. The state can then be used in a path such as
  `item-storage?query=?{q} sortby %{sortOrder}`.

* `${name}` -- recognised as a synonym of `%{name}` to ease transition
  from this older syntax, but this is deprecated and **should not be
  used in new code**.

* `!{name}` -- interpolates the value of the named property from the
  present React component. For example, if the path is
  `perms/users/!{user.username}/permissions` and the component has a
  `user` prop which is an object containing a `username` field with
  value `fred`, the path will be resolved as
  `perms/users/fred/permissions`.

#### Fallbacks

In general, all the nominated pieces of state -- UI URL
path-components, UI URL query parameters, local state and props -- must be
present in order for these textual substitutions to be performed. If
something is missing -- for example, when the path
`item-storage?query=?{q}` is evaluated in a context where the UI URL
does not have a query parameter `q` -- then substitution fails, and
the path from the `staticFallback` part of the configuration is used
if present. If not, no action is taken until the necessary information
is available.

However, extended syntax, modelled on [that of the BASH shell](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html),
may be used with any of the three kinds of substitution to provide a
fallback value, used when the state is missing:

* `:{name:-val}` yields the value of the named UI URL path-component
  if any, or the constant `val` if it is undefined.

* `?{name:-val}` yields the value of the named UI URL query parameter
  if any, or the constant `val` if it is absent.

* `%{name:-val}` yields the value of the named local resource
  if any, or the constant `val` if it is undefined.

* `!{name:-val}` yields the value of the named component property
  if any, or the constant `val` if it is undefined.

This syntax is useful for providing a default search-term, default
sort-order, etc.

In addition, further BASH-like syntax allows a value to be provided
only if the names path-component, query parameter or local resource
_does_ exist: `%{name:+val}` yields either the constant `val` or an
empty string, according as `%{name}` is or is not defined.

#### Example path

Putting these facilities together, the following `path` could be
defined for the `items` resource in a UI module for inventory
management:

> `item-storage/items?query=(author=?{q:-}* or title=?{q:-}*) ?{sort:+sortby} ?{sort:-}`

This consults two query parameters of the UI URL, each of them
twice. The `q` parameter contains a search term and `sort` the name of
the CQL field to sort the results by.

`?{q}` appears twice because the `query` parameter of the back-end URL
contains a CQL query that searches for the term in both the `author`
and `title` fields. In both cases, an empty fallback value is
specified (`?{q:-}`): this works because the query is followed by a
wildcard character (`*`) in both cases, so that when the query itself
is empty the whole search-term becomes `*`.

`?{sort}` appears twice: once to generate the `sortby` keyword that
introduces the optional sorting clause in CQL, and once to interpolate
the sort criterion itself. When no sort criterion is specified, the
`sortby` keyword is not included at all, since it is generated as a
fallback value that is active only when the `sort` query parameter is
present (`{sort:+sortby}`). Similarly, the value itself falls back to
an empty string, so that there is no sorting clause at all in the
generated path when no sorting parameter is provided in the UI URL.

#### Functional paths and parameters

When the power and flexibility of text substitution and fallbacks are not
sufficient for expressing how to build the back-end URL, arbitrary
JavaScript can be used instead. If the value of a resource's `path`,
or one of its `params` or `headers` is a function rather than a string, then
that function is invoked whenever a path is needed. It is passed five
parameters (though most functions will not use them all):

* An object containing the UI URL's query parameters (as accessed by
  `?{name}`).

* An object containing the UI URL's path components (as accessed by
  `:{name}`).

* An object containing the component's resources' data (as accessed by
  `%{name}`).

* The logger object in use by stripes-connect.

* The entire set of props of the component using stripes-connect
  (which of course contains redundant copies of much of the rest of
  the information passed in).

The function must return a string to use as the path, or `null`
if it is unable to do this because a required piece of state is
missing. In the latter case, the path from `staticFallback` will be
used if it is defined.

So the function would usually be defined along these lines:

        static manifest = Object.freeze({
          users: {
            type: 'okapi',
            path: (queryParams, pathComponents, resourceData) => {
              if (queryParams.x) return `users/%{queryParams.x}`;
              return undefined;
            }
          }
        });

Similarly, the entire `params` and `headers` objects can be replaced by a
function that takes the above arguments and returns, instead of a string,
an object to map to the parameters to be sent with requests. Or null if
it lacks necessary information.



## Connecting the component

React components are classes that extend `React.Component`.  Instead
of using a React-component class directly -- most often by exporting
it -- use the result of passing it to the `connect()` method of
Stripes Connect.

For example, rather than

        export class Widget extends React.Component {
          // ...
        }

or

        class Widget extends React.Component {
          // ...
        }
        export Widget;

use

        import { connect } from 'stripes-connect';
        class Widget extends React.Component {
          // ...
        }
        export connect(Widget, 'stripes-module-name');

(At present, it is necessary to pass as a second argument the name of
the Stripes module that contains the connect component. We hope to
remove this requirement in future.)

When a parent component is connecting one of its children, it may use the
curried form of `connect`, provided on the `stripes` prop, which implicitly
passes the module name to connect:

        constructor(props) {
          super();
          this.connectedWidget = props.stripes.connect(Widget);
        }

Because the resource object is global to the module, if the same component
will be used repeatedly to retrieve a different value for each item on a list,
e.g. when connecting `<LoanDetails>` repeatedly to retrieve the details of
multiple loans, it is necessary to provide the `dataKey` option with a unique
value for each connected instance:

        constructor(props) {
          super();
          this.connectedLoans = this.props.IDs.map(id => props.stripes.connect(LoanDetails, { dataKey: id }));
        }

        render() {
          return (
            <div>
              {this.connectedLoans.map(comp => <comp stripes={this.props.stripes} />)}
            </div>
          );
        }

## Using the connected component

When a connected component is invoked, two properties are passed to
the wrapped component:

* `resources`: contains the data associated with the resources in the
  manifest, as a JavaScript object whose keys are the names of
  resources. This is null if the data is pending and has not yet been
  fetched.

* `mutator`: a JavaScript object that enables the component to make
  changes to its resources. See below.



### Mutators

The `mutator` is an object whose properties are named after the
resources in the manifest. The corresponding values are themselves
objects -- one per resource.


#### REST and Okapi resources

Each resource's mutator object has keys that are HTTP methods: the
corresponding values are methods that perform the relevant CRUD
operation using HTTP, and update the internal representation of the
state to match. A typical invocation would be something like
`this.props.mutator.users.POST(data)`.

The mutator methods optionally take a record as a parameter,
represented as a JavaScript object whose keys are fieldnames and whose
values contain the corresponding data. These records are used in the
obvious way by the POST, PUT and PATCH operations. For DELETE, the
record need only contain the `id` field, so that it suffices to call
`mutator.tenants.DELETE({ id: 43 })`.

The POST, PUT and DELETE mutators optionally take a second `options` parameter.
Currently the only option available is `silent`. The silent option can be used
to indicate that the given mutation should not cause refresh on any corresponding
resources. This is particually helpful when running multiple mutations in a batch
mode when only the last mutation should actually cause the refresh to happen.
Example usage: `mutator.tenants.DELETE({ id: 43 }, { silent: true })`.

For the GET mutator method, i.e. when passing `accumulate: true` in the
manifest, provide an updated `params` argument rather than an updated record, e.g.

    const query = `query=username=^${username}`;
    mutator.users.GET({ params: { query } })
      .then(records => { ... });


#### Local resources

Local resources provide a mutator object with two functions, `update` and
`replace`. The `replace` mutator will replace the current value of the local
resource with a new one. `update` only works on object values and will do a
shallow merge of properties from the new object onto the old one eg. following
the semantics of `Object.assign({}, oldValue, newValue)`.


### Error handling

HTTP errors are caught and processed by Stripes Connect, leaving information in its internal state. By default, these errors are then reported in an `alert()` via a Redux observer in Stripes Core, to ensure that they are noticed during development. Since errors at this low level are unusual events in production code, the use of an alert-box is often also also suitable in production, so often no explicit error-handling is necessary.

But applications can instead elect to be responsible for their own error-handling. To disable the alert-box for a particular resource, add a `throwErrors: false` property to that resource's object in the manifest.

When doing this, there are two ways to catch the errors for handling or reporting.


#### Catching rejected promises

Mutators return promises which can be interrogated using `.then` and `.catch` as usual. Consider [the following code (from the Course Reserves module)](https://github.com/folio-org/ui-courses/blob/5f9a5b05d8bc890e04a5b437540eedcf5140eb15/src/components/ViewCourse/sections/AddReserve.js#L45-L54): a new reserve is created by a POST to the `reserves` resource, which has `throwErrors: false`. Whether the operation succeeds or fails, the user is notified via a suitable callout:

```
this.props.mutator.reserves.POST({ courseListingId, copiedItem: { barcode } })
  .then(addedRecord => {
    this.showCallout('success', `Added item "${addedRecord.copiedItem.title}"`);
  })
  .catch(exception => {
    exception.text().then(text => {
      this.showCallout('error', `Failed to add item ${barcode}: ${text}`);
    });
  });
```


#### Detecting failed mutations

Alternatively, application code can inspect the resource' `failedMutations` to notice when something has gone wrong. The usual approach is to notice when a _new_ failed mutation has appeared and report that. One way to do this is using the `componentDidUpdate` lifecycle method to compare the `failedMutations` of the previous and present properties:

```
componentDidUpdate(prevProps) {
  const { failedMutations } = this.props.resources.reserves;
  const prev = prevProps.resources.reserves.failedMutations;
  if (failedMutations.length > prev.length) {
    console.log('componentDidUpdate: new failure mutations:', failedMutations.slice(prev.length));
  }
}
```

Either of these approaches can be used, as best suits the architecture
of the specific application.



<br/>
<br/>
<hr/>

## Appendices: for developers

These sections are only for developers working on Stripes
itself. Those working on _using_ Stripes to build a UI can ignore them.


### Appendix A: how state is stored

* All state is stored in a single branching structure, the _Redux
  store_. (Module creators should not need to know about details of
  Redux, and especially not about reducers, but this idea of a single
  state store is important nevertheless.)

* Data in this state structure consists of _resources_, each named by
  a string.

* Rather than each module having its own namespace within the
  structure, all modules' data is kept together in a single big
  table.

* To avoid different modules' same-named data from clashing, the code
  arranges that the keys in this table are composed of the module name
  and the resource name separated by an underscore:
  _moduleName_`_`_resourceName_

  * XXX In fact, the code that does this is the `stateKey()` methods of
    the various resource-types. That means (A) we need to be very
    careful that new resource-types also remember to do this; and (B)
    we probably made a mistake, and this should instead by done at a
    higher level in `stripes-connect/connect.js`.

* A component's resource names are defined by the keys in its _data
  manifest_. The value associated with each key is tied to the
  resource specified by its parameters -- for example, the `root` and
  `path` of a REST resource. In general, that value is a list of
  records: some components will deal only with a single record from
  that list.

  * XXX For example, `PatronEdit.js` deals only with a single record;
    but it works with the `patrons` resource, which is a list of
    records, and picks out the one it wants by using
    `patrons.find((p) =>  { return p._id === patronid })`.
    If I have understood this correctly, it looks like a grotesque
    inefficiency that will quickly become unworkable as we start to
    use large patron databases.

* In general, a Stripes module contains multiple connected
  components. The data manifest is specific per-component. Components
  may communicate with each other, or share cached data, by using the
  same data keys. It is the module author's responsibility to avoid
  inadvertent duplication of keys between unrelated components.

* Some components may exist in multiple simultaneous instances: for
  example, a list-of-records component may be designed such that a
  user may pop up a more than one full-record component to see the
  details of several records at once. In this case, the state keys are
  different because the records' IDs are included (due to the manifest
  path being of the form `/patrons/:patronid`, containing a
  placeholder.)

* For local resources, which are not persisted via a REST service such
  as Okapi, some means must be established whereby each individual
  datum is individually addressable. Only then can multiple instances
  of the same component that uses local storage co-exist.

  * For this reason, it may be worthwhile to prioritise the
    development of a page that has two instances of the Trivial
    module, and see that they can each maintain their own data.

  * Also to be done: a simple implementation of search preferences, as
    a model for how two components (SearchForm and SearchPrefernces)
    can deliberately share data.


### Appendix B: unresolved issues

#### One vs. Many

Right now there is no clear standard as to what data is returned by
Okapi services -- for example, a single record by `id` yields a single
record; but a query that matches a single record yields an array with
one element.

#### Metadata

We use the Redux Crud library to, among other things, generate
actions. It causes a number of compromises such as our needing to
clear out the Redux state at times, because it is designed for a
slightly different universe where there is more data re-use.

As part of that, it prefers to treat the responses as lists of records
that it can merge into its local store which makes having a top level
of metadata with an array property `patrons` or similar a bit
incompatible.

We currently pass it a key from the manifest (`records`) if it needs
to dig deeper to find the records. But that means we just discard the
top level metadata. It may soon be time to reimplement Redux Crud
ourselves and take full control of how data is being shuffled
around. Among other things, it would give the option to let our API be
more true to intent and transparently expose the data returned by the
REST request.

#### Object counts

Can we get a count of holds on an item? How does that API work and
does our above system mesh with it well enough to provide a pleasant
developer experience?


### Appendix C: worked-through example of connected component

This is in the separate document
[A component example: the PatronEdit component](https://github.com/folio-org/stripes-core/blob/master/doc/component-example.md)


### Appendix D: walk-through of state-object changes during a CRUD cycle

XXX To be written

These images may be useful:
* https://files.slack.com/files-pri/T047C3PCD-F2L37S7C2/pasted_image_at_2016_10_06_11_13_am.png
* https://files.slack.com/files-pri/T047C3PCD-F2L2RAH5E/pasted_image_at_2016_10_06_11_15_am.png
* https://files.slack.com/files-pri/T047C3PCD-F2L2WSHA4/pasted_image_at_2016_10_06_11_31_am.png
