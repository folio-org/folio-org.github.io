---
layout: null
---

* Start Date: 10/09/2023
* Contributors:
  * [Craig McNally](cmcnally@ebsco.com)
  * [Vince Bareau](vbareau@ebsco.com)
* RFC PRs:
  * PRELIMINARY REVIEW: https://github.com/folio-org/rfcs/pull/14
  * DRAFT REFINEMENT: https://github.com/folio-org/rfcs/pull/22
  * PUBLIC REVIEW: https://github.com/folio-org/rfcs/pull/29
  * FINAL REVIEW: https://github.com/folio-org/rfcs/pull/34
* Outcome: ACCEPTED

# Application Formalization

## Summary
It is proposed that an Application be defined as the minimal but complete set of elements which together are intended to deliver a specific solution to Folio. The intention is to group together all the closely related components which will need to evolve together, but independently of other parts (i.e. other applications) of Folio.

## Motivation
The existing Folio project lacks a formal definition of an Application structure. A consequence is that Folio is stuck in a mode of monolithic releases which are ever increasing in size.  There have also been repeated complaints that the setup and management of Folio can be difficult due to the number modules involved.

## Scope
* Application composition
* Application versioning
* Application dependencies
* Application definition/descriptors
* Backward compatibility with Folio instances not adopting Applications
* Application management and deployment are ***out of scope***
* Application Stores and Marketplaces are ***out of scope***
* Application-specific UI bundles is ***out of scope***
* How movement of modules between Applications will work is ***out of scope***
* How bounded contexts and cross-module database access could be introduced is ***out of scope***

## Detailed Explanation/Design

### Terminology
* Application:  The minimal but complete set of elements which together are intended to deliver a specific solution to Folio.
* Bounded context:  The boundary of the microservice.  It "owns" the storage for the service.

### Specifics

#### Application Composition
Applications can be thought of as vertical slices of functionality.  As such, they're are comprised of a combination of the following:
* Backend Modules 
* Edge Modules 
* UI Modules 
* UI Plugins 

Applications will typically be made up of multiple components spanning all or several of these categories.  However, that's not a requirement.  In fact, in it's simplest form, it's possible for an application to be comprised of a single module from any of the categories listed above.

An important concept introduced by the formalization of Applications, is that Applications become the delivery mechanism for the modules they contain. Therefore, if a new version of a particular module is required, then it follows that the new version of the entire Application must be installed. It then also follows that a given version of a Module must belong to one and only one Application. To do otherwise is possible, but would quickly lead to dependency and version management challenges.  This restriction is enforced by the Application Manager and/or Folio Application Registry (FAR), both of which are out of scope for this RFC.  It is recognized that there must be accommodations to allow refactoring or consolidation of Applications, which could involve moving of particular Modules from one Application to another.

#### Application Versioning
* Applications must maintain their own versioning which is independent of the versioning of their components. The components which comprise Applications already have their own independent versioning which would still need to remain in effect.
* Applications have versioning separate from interface versioning
  * Application compatibility is determined at the Application level
  * This allows Applications to have independent development lifecycles.
* The [semantic version](https://semver.org/) system is used for applications.

#### Application Dependencies
Formalizing Applications does not change the underlying module implementations.  This means modules which depend on interfaces provided by other modules continue to have those dependencies, and those dependencies may span Application boundaries.  However, the Application formalization rolls those interface dependencies up into Application dependencies, or dependencies on specific versions of applications. 

Example w/ many version omitted for clarity:
**app-foo-1.0.1**
* requires: 
  * `app-bar: ^1.0.0`
* modules:
  * `ui-foo`
    * requires interfaces: `foo`
  * `mod-foo`
    * provides interfaces: `foo`
    * requires interfaces: `foo-storage`, `bar`
  * `mod-foo-storage`
    * provides interfaces: `foo-storage`
    * requires interfaces: 

**app-bar-1.0.0**
* requires: 
  * `app-configuration: ~1.1.1`
* modules:
  * `mod-bar`
    * provides interfaces: `bar`
    * requires interfaces: `configuration`
  * `ui-bar`
    * requires interfaces: `bar`

**app-configuration-1.1.1**
* requires: 
* modules:
  * `mod-configuration`
    * provides interfaces: `configuration`
    * requires interfaces: 

In this scenario, in order for `app-foo-1.0.1` to be enabled for a tenant, `app-bar-1.X.X` and `app-configuraturation-1.1.X` would also need to be enabled for the tenant.  This is because `app-foo` depends on a compatible version (specified as `^`) of `app-bar-1.X.X`, and `app-bar` depends on an approximately equivalent version (specified as `~`) of `app-configuration-1.1.1`.  Exact versions and/or ranges can also be specified.  See the [node-semver documentation](https://github.com/npm/node-semver#advanced-range-syntax]) for details.

#### Application Descriptors
Similar to how modules are explicitly defind through module descriptors, applications are defined through application descriptors.  The application descriptor references module descriptors

**Application Descriptor Properties**
| Property            | Type         | Description                                                                          | Notes                    |
| ------------------- | ------------ | ------------------------------------------------------------------------------------ | ------------------------ |
| id                  | String       | Identifier for the application conforming to pattern: `{name}-{semantic version}`    | e.g. "app-orders-1.0.0"  |
| name                | String       | Name of the application                                                              | e.g. "app-orders"        |
| version             | String       | Version of the application                                                           | e.g. "1.0.0"             |
| description         | String       | Brief description of the application                                                 | e.g. "Application delivering orders functionality" |
| dependencies        | Dependency[] | List of dependencies on other applications                                           | See "Dependency Properties" table below            |
| modules             | ModuleId[]   | List of backend/edge modules comprising the application                              | See "ModuleId Properties" table below              |
| uiModules           | ModuleId[]   | List of UI modules comprising the application                                        | See "ModuleId Properties" table below              |
| moduleDescriptors   | ModuleDescriptor[] | Module descriptors for the backend/edge modules comprising the application     | Read-only. See [ModuleDescriptor Schema](https://github.com/folio-org/okapi/blob/master/okapi-core/src/main/raml/ModuleDescriptor.json) |
| uiModuleDescriptors | ModuleDescriptor[] | Module descriptors for the frontend modules/plugins comprising the application | Read-only. See [ModuleDescriptor Schema](https://github.com/folio-org/okapi/blob/master/okapi-core/src/main/raml/ModuleDescriptor.json) |
| metadata            | Metadata     | System-generated record metadata                                                     | Read-only. See [Metadata Schema] (https://github.com/folio-org/raml/blob/master/schemas/metadata.schema) |

**NOTE**: Module descriptors are not being retired or replaced.  As such, there's no need to duplicate all of the information in the module descriptor in the application descriptor.  Things like the launchDescriptors sections of module descriptors are not duplicated or moved to the application descriptor.

**Dependency Properties**
| Property | Type    | Description                                                          | Notes                            |
| ---------| ------- | -------------------------------------------------------------------- | -------------------------------- |
| id       | String  | Identifier for the module conforming to pattern: `{name}-{version}`  | e.g. "mod-orders-storage-13.5.0" |
| name     | String  | Name of the module                                                   | e.g. "mod-orders"                |
| version  | String  | Version of the module                                                | e.g. "13.5.0"                    |

**ModuleId Properties**
| Property | Type    | Description                                                          | Notes                            |
| -------- | ------- | -------------------------------------------------------------------- | -------------------------------- |
| id       | String  | Identifier for the module conforming to pattern: `{name}-{version}`  | e.g. "mod-orders-storage-13.5.0" |
| name     | String  | Name of the module                                                   | e.g. "mod-orders"                |
| version  | String  | Version of the module                                                | e.g. "13.5.0"                    |
| url      | String  | URL pointing to the module descriptor for this module                | e.g. "https://folio-registry.dev.folio.org/_/proxy/modules/mod-orders-storage-13.5.0" |

Example:
```
{
  "id": "app-gobi-0.0.1",
  "name": "app-gobi",
  "version": "0.0.1",
  "description": "Application facilitating the placement of orders via GOBI and other compatible vendors",
  "dependencies": [
    {
      "id": "app-orders-0.0.1",
      "name": "app-orders",
      "version": "^0.0.1"
    },
    {
      "id": "app-organizations-0.0.1",
      "name": "app-organizations",
      "version": "^0.0.1"
    }
  ],
  "modules": [
    {
      "id": "mod-gobi-2.6.0",
      "name": "mod-gobi",
      "version": "2.6.0",
	  "url": "https://folio-registry.dev.folio.org/_/proxy/modules/mod-gobi-2.6.0"
    }
  ],
  "uiModules": [
    {
      "id": "folio_gobi-settings-2.0.0",
      "name": "folio_gobi-settings",
      "version": "2.0.0",
	  "url": "https://folio-registry.dev.folio.org/_/proxy/modules/folio_gobi-settings-2.0.0"
    }
  ]
}
```
**N.B.** Full module descriptors and metadata have been omitted for readability reasons.

## Benefits
* Application formalization is the necessary first step in being able to create Application-level releases.
  * NOTE: How Application releases are packaged into a Folio release is the subject of a future RFC about Platforms.
* The system operator can focus on an Application (which is a "package") rather than the multitude of individual modules it contains. They'd work with the single Application instead of the individual parts of that Application (business logic module, storage module, UI module, plugins, etc.)
* Brings us closer to realizing the idea of having an application store/marketplace
* Application formalization facilitates the adoption of a formalized microservice bounded context (subject of a separate RFC: https://github.com/folio-org/rfcs/pull/20)

## Risks and Drawbacks
* Transition to Applications should be iterative
  * First pass is to create larger applications spanning multiple areas in order to satisfy dependencies
  * Subsequent passes will further break up these large applications into smaller, applications focused on a single area of functionality
* Since Applications are a vertical slice of functionality, better alignment/coordination between back-end and front-end development team members is required.
  * Reorganizing development teams around applications would help
* By latching onto the Application term, there may be confusion about terminology since that term currently means different things to different people.
  * It may help to proposed formal names for other things currently referred to as Applications (e.g. the icons that appear in the Folio toolbar)

## Rationale and Alternatives
Alternative approaches include:
* **Status quo** - Don't do anything and deal with monolithic releases, an ever-growing number of modules, and all the problems and challenges associated with those things.
* Releasing of coarser granularity packages of modules; e.g. platform-core, platform-minimal, platform-complete, etc.
* **Independent module release cycles** - Impractical due to how tightly coupled modules are to one another.   It also doesn't address the issue of system operators needing to manage an ever growing number of modules.

## Timing
* First in the sequence.  
* RFC Submission:  Early October '23

## Unresolved Questions
The following unresolved questions are not addressed here, but will be the addressed in other RFCs:
* How will Application management work?
* How will Application Descriptors be developed and maintained?
* How the Stripes UI will be updated as applications are enabled/disabled/upgraded?
