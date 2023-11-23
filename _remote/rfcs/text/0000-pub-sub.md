---
layout: null
---


- Start Date: 2019-06-20
- Contributors:
  - [Taras Spashchenko](taras_spashchenko@epam.com)
- RFC PR: https://github.com/folio-org/rfcs/pull/2
- Outcome: ACCEPTED

# PubSub support in FOLIO (module implementation)

## Summary
This RFC proposes to add event-driven architecture capabilities to the FOLIO platform. Specifically, it is a general purpose publisher-subscriber (`pubsub`) implementation.

## Motivation

The Folio Platform consists of a set of microservices which are organized around a central proxying API Gateway. Folio modules implement these microservices through RESTful API interfaces. In order to implement complex library workflows it is necessary to distribute the work to individual modules to perform the specialized tasks.

The approach described here is to provide a messaging system whereby modules publish relevant data when ready, for other modules to consume and do their part. Modules which participate in a particular workflow can subscribe to the relevant messages. The advantage of this particular solution is that it fits well with the microservices architecture and preserves the independence of the modules. Each module plays its part but remains unaware of any role played by other modules. It does not require a centralized workflow controller.

## Detailed Explanation/Design

### Requirements
#### Functional Requirements
- A business module (back-end) can define a set of events it can send (publish). It can also declare and receive (subscribe to) event of different types.

- An “Event Descriptor” must be provided to define new event types.
  1. The event definition produces a unique “Event Type”
  2. The “Event Descriptor” must have a detailed description for the event type and payloads which can be received within events of this type.
  3. “Event Descriptor” does not support versioning. To update an existing event declaration, a new "Event Type" must be defined with a new "Event Descriptor". However, it is recommended that the updated "Event Type" maintain the same name followed by an incremented version number suffix. The description field of the new event type should be used to explain the difference between the two related “Event Descriptors”. 
  4. The “Event Descriptor” must define a default time-to-live (TTL) for events of this type.
  5. The “Event Descriptor” can optionally define data structure definitions or schemas for an event payload.
  6. The “Event Descriptor” can optionally define events as “Signed” of “Unsigned” (not in scope of MVP, but the basis for that must be provided). “Signed” means that all events of this event type must be digitally signed by the publisher.

- Each instantiated event must contain at least a UUID and an "Event Type". A payload for the event is optional and can be of any type of serializable data and it is up to a publisher and a consumer to agree on the data structures they want to exchange. If an event descriptor contains data structure definitions or schemas, they can be used for validation, marshalling/unmarshalling.

- It should be possible to notify a publisher that there are no subscribers for an event type it is trying to send. It could be included in a response to an event publishing call.

- Time to live (TTL) must be set up for each event sent. It optionally allows a publisher to provide a callback endpoint or an error “Event Type” to be notified that despite the fact that there are subscribers for such an event type no one has received the event within the specified period of time. If a TTL is not explicitly specified for an event, the default TTL for the event type will be used.

- Cross tenant events exchange is assumed in the future, but not in the scope of MVP (v1).

- Integration with external/third party systems should be allowed (not in scope of MVP, but the basis for that must be provided)

### Target Solution Architecture

#### Solution Overview
- A new module is introduced, `mod-pubsub`. It is responsible for maintaining the registrations of event types and for coordinating distribution of events to the appropriate subscribers. Folio modules may publish events and/or subscribe to events of specific event types. It is the responsibility of publisher modules to define the event types that they will provide, which is accomplished through the use of an event descriptor. Note that it is possible for multiple publishers to register for the same event type. However, the event type may only be defined once. Subscribing modules will register themselves to specific event types by providing a URI that will be invoked by the event manager when pushing events of matching event types.  Event subscription is done on a per tenant basis.

- The `mod-pubsub` module is also responsible for maintaining a trail of activities: event publication; subscription distribution; errors; non-delivery; etc. By using the correlationID embedded in events it is possible to reconstruct the sequence of operations that form a particular workflow.

- By configuring specific event subscriptions for each tenant it is possible to implement specific cases of inter-app coordination.

- The `mod-pubsub` module is implemented using a message queue (Kafka) which will provide the necessary persistence.

#### High-level solution structure
There is a global FOLIO interface `pubsub` defined in the scope of this solution which provides APIs to ensure the functioning of the subsystem:
- API for event type registration by publishers and subscribers. This API must be called by back-end modules.
  - `POST /pubsub/eventtypes` - to register an event type 
  - `DELETE /pubsub/eventtypes` - to remove event type registration
  - `POST /pubsub/eventtypes/declare/publisher` - to declare a publisher for a set of event types
  - `DELETE /pubsub/eventtypes/declare/publisher` - to remove publisher declaration
  - `POST /pubsub/eventtypes/declare/subscriber` - to declare a subscriber for a set of event types
  - `DELETE /pubsub/eventtypes/declare/subscriber` - to remove subscriber declaration
- API to retrieve existing registered event types.
  - `GET /pubsub/eventtypes` - returns all registered event types
  - `GET /pubsub/eventtypes/{EVENT_TYPE}` - returns an event descriptor for a particular event type
- API to retrieve the registered subscriptions for a specified tenant and event type
  - `GET /pubsub/eventtypes/{EVENT_TYPE}/subscribers` - returns all subscribers of the event type provided in the path variable
  - `GET /pubsub/eventtypes/{EVENT_TYPE}/publishers` - returns all publishers of the event type provided in the path variable
- API used by publishers to send events. This API must be called by back-end modules which act as publishers
  - `POST /pubsub/publish`
- API to retrieve the activity history performed by the event manager. A correlationID can optionally be provided to limit context.
  - `GET /pubsub/history`
  - `GET /pubsub/history?corellationId={corellationId}`

It is allowed for publishers to provide callback URLs to receive feedback from `mod-pubsub` module in cases when:
- Subscriber did not receive an event within the specified period of time.
- All subscribers deleted their subscriptions on a particular event type registered by this publisher.
 

There is a set of requirements that must be followed by a module to provide “Subscriber endpoints” to consume events. The basic set of requirements:
- HTTP Method - POST
- A set of required HTTP header. [_To be defined further if it is needed._]
- A payload structure - JSON which represents an event. See [Event data structure](#Event data structure) 

Reference implementations should be provided that allow a back-end module to become a publisher or a subscriber respectively to simplify development.
  
A dedicated module, `mod-pubsub`, must implement and encapsulate all logic related to event sending and delivery. All interactions between this module and back-end business modules will be done via HTTP.

#### Registration

Each module which acts as a publisher or a subscriber must contain a configuration or property with a set of event types it deals with. Publishers should provide event descriptors. For subscribers, it is enough to specify event types together with endpoints for event delivery. Details of that configuration must be defined further.

##### Event Type registration 
The set of event descriptors will be registered by a publisher at the time when the module is enabled for a tenant. To do that the publisher must call `pubsub` API for event type registration. The payload for that call is a set of event descriptors which define events this particular module is able to publish.

At this stage it is possible to check if another module has already been registered as a publisher for the same event descriptors.

It is worth mentioning that at this stage only event descriptors will be registered. To allow a module to publish events further steps optionally should be taken.

![Event type registration diagram](http://www.plantuml.com/plantuml/png/TP4nJyCm48Lt_ufJ9nWgTKPL9nZO4B01myM-D2SSsxBF5VttN1nQXL8YPOZFxxltNeJ54pmSA0Z8CL61J7ikab4u1cEmIWnrx2Z3QjljtZQRpSVAc8HPs792bQt6wDRRL3lFPQ2yMm4MICROw3tP2LFcEtgbrAwDoP4nwnsaEq3GMLKJhCS1Eq_kFVGnwq3qEuWn-nnhMfZyxH7qIJ33dWcT2Wi9n1weAHmLcpb9p4N1EOvwmSRGyxvU4jJMn9ZW6dXU-DfQkVaFUTlKAZphdp0NkhORWmCxaFs45izdDNlyoKAPt79Xew8Nu1uSzxtETVG7saWo41GSJpjRG_Ibq0PPsDE27iC1FPzMtPz9SmglnaDixNYsCk5hS9UObl95HLTImXJIS_W4YStO_7ElE5csE-21e2CAYpPcHxfzUhy1)

##### Subscriber registration
A back-end module can register event types it can consume at the time when the module is enabled for a tenant. To do that it must call the `pubsub` API for registration. The payload for that call is a set of event types augmented with endpoints provided by this module. These endpoints will be used to deliver events of respective types.

##### Publisher registration
When a module is up and running and is enabled for a tenant, a tenant administrator can define types of events which must (or must not) be published by this module in scope of this tenant (subscribe a tenant to event types) using either UI Admin console/Settings Page or HTTP requests to `pubsub` endpoint for bulk operations. 

It is suggested that by default all event types are activated for a tenant.

##### Cancellation of registration
When a module is disabled for a tenant whether it is a publisher or a subscriber the module must unregister event types it deals with by calling the API provided by `pubsub`.

##### mod-pubsub responsibilities
The `mod-pubsub` must keep track of registered event types, publishers and subscribers which are able to send and receive events of those types.


#### Data structures
##### Event descriptor data structure
Name | Type
--- | ---
Event type | String - not UUID, should be human readable
Description | String
Default TTL | Period (1 minute, 1 hour, 1 day, 1 week, etc.)
Signed event | Boolean (true/false)

##### Event data structure
Name | Type
--- | ---
Event ID | UUID 
Event type | String
Metadata | A set of named attributes <table><tr><td>Tenant ID</td><td>String</td><td>Required</td></tr><tr><td>Event TTL</td><td>Period</td><td>Required</td></tr><tr><td>CorrelationID (could be used to track related events)</td><td>UUID</td><td>Optional</td></tr><tr><td>Original event ID</td><td>UUID</td><td>Optional</td></tr><tr><td>Publisher callback</td><td>endpoint or event name</td><td>Optional</td></tr></table> 
Event payload | Arbitrary JSON (String representation)

#### Event publishing
There is a high-level sequence diagram below which represent the event publishing flow.

![Event publishing diagram](http://www.plantuml.com/plantuml/png/fLHTRzem57tFhxYY3zqYYdX67LBNqMbIsw4jsWlbmOblWZTZP_u0HUgFttKI4g0C8HKfiXFEFJu-zzXEE8amsw1oKFfK2hiIge3Iw0ojfMaKCU-qykiK3Gnkq-bYF1ul1r5KCkD49af6bOErvZUtRJsQwG2OXJAACYqbPavePHiCGQnFwx-HOqGiS3E5SW9pWqI8m1HW8uPLKZFU0UxrkjHs3w3JtqGTHONHlZox0w0VqIokIFduuM59XBJu1E9uCVirUqwMSJoXUHpN94bLuX2Uq37E71l2l14InmIhgQWMTXJtAyp-WCZ1hOI5pW2W5uE5i0uDyXV552S4jieThH0GZ9pPC8SSScs0WKC2kdeD9XqaL730gBJROwrndPxMnKlXYwjdjgcMxIxkE6-bILq0ZQPgTYh9yEIDxa3SQJybO_P_-DkjlazJHdb84ImUinqqgCPUMqYInvqYoiT6y5rpB996u9Wp7vmFi9oYLerEaiwzsskdK4w7rnVb5KSZgpP-WTvSXo1OxKs6yC7fKcH3-ElHKyJGPQEFPqG7f_h-GP3PsqYdo6P6qA6q7KKRcd2Aw57w96ZFxk-6gGANJSzwIrTqE5D4LPiAM-5Mi6L6qQxiw1JD9LthElUpbrIhp3MPTehrgo49vxMzJqsxR1Z34qaiTjzUFy6ZK1Z6S1l0Q_CLVf3nTyReBSs_AMgBOf8IAANj867v3lF4A1lqX41GvWqJ4dGEpINOD5CuWNtr5-r2SpzBZnr9UwQxl4jv3D-NDQCnnCQMTESYK3BxA-Ieh6b_NtbyWsPQvSAiMRY-3sDmp5JtwaAYWvVNO3sqply3)

#### Event delivery
There is a high-level sequence diagram below which represent the event delivery flow.

![Event delivery diagram](http://www.plantuml.com/plantuml/png/nLPDJnj13Btlhx32WJQ22AweHOgWQYjH3f0RuJ3PSR8Z9fxjp6peIldnzUntabL80r8Fa6JNVlPxzjZZbTS8trP87YHgjKARGsfDZCufMaIHoBoXR3b32uCli-kdYukBvq4KdQR2UXMhLB3ZO6da-PSqcsdb4hJN0n0EqYYAZTOOUsN8bJPiuh9PyHebHj4k2BzsiLKSxdnSuhZBlMQZqQYoa_lXxYipwWkxctj4nYCOrgD85M0u76iDBQ03Yp6oO811FKPMoqnxGMWof_FXC4AI452YzNeTCGYSNmUiAtX0RnLxWQ3I6URMBC4d21b9j3fdwQV4PLWf_daQGZcJsHZXapUfYi_WTuOPdW7wUFHvIcFj3CGcqn9c27DbaR_aMu1GustayeYXH20skKtfDL5n0i9oabp1bV0CEJSM17Wa5cvAuPTFbAie-3pbYXRGJoVtOfK_Ln76KbOcsYo0FstERQKzJ5XlB4AGwGPdiG6wETua6B-K6Ap5P79NM0I8id4v1zOPy4yQc1Sljo4UqCK9oanNvMgQdPagpqJ30v5l-hxDep3L3jj4jfDOM9EbC7OvnSsp9W1dbrx1lV5gddCAJHT25WvVqHxMiimnbsScM8EgX7BK9ahzX6-vhjp0eGMAf8zYnjW5kxPItVxlRuoePLqUcP2y0sysVHahHSkEI_RVEJfridowDn8tdFbtYqZFpDDT5ZH36LkU8P3eX6hSwspP3KvkXNrv57ffg7dFZxlWXJ2J1ZNXgJ3ZL_MXbyVekQyVGlYIqWz1KdSgnmE9ZHDhg52dj_8IE_GEL4yUfvxiLq_-N_KaL9JUgvxiLM-_adISajIl9465kKrbm-GVnEOv8kkTZlsiwTZni2tGxjX-JT27aIRO7ONpOAWxHgOKycrItIHRROd3kkWZ1ryrz3g1mu9vEtZ_fZfeMxrtOnrnclPlhdtdxICts7Oh7LpGOnXNSS9dLFpJkAWVhh_2dUBcvCy9NsPWNJxbIaWOCujN_lwJF5eIzLQhJKBynkQNKEJvhn00l1LAWvb3UVajpx_o2bllM-F35kt6kQdrAiP8AsjOe-5UsGYxXH66GWEoTQqFOw0zU7nV9BufBaMudpDCGAt4YFu2)

#### Security
Calls to the `pubsub` can be done either on behalf of a user or a backend module if this is a result of the processing of another event. While all calls from `mod-pubsub` to subscribers will be done on behalf of the `pubsub`. For these cases we can’t use or apply permissions granted to a user, because these calls don't have user context and could be treated as “System” or “Internal”. Since FOLIO Platform currently does not provide such type of users (a System/Internal level user) it makes sense to create an ordinary user that will be assigned to the `pubsub` to perform all actions on behalf of that. Also, it means that all data required by OKAPI to be provided in the HTTP headers must be transferred as attributes in the metadata section of an event payload (X-Okapi-Tenant, etc.). The drawback of this approach is that the dedicated user can be accidentally deleted by a FOLIO administrator. Also, it is allowed to login from UI using that user’s credentials.

The `mod-pubsub` module should be able to obtain a JWT token from mod-authtoken on behalf of that “technical” user as well. It could be done when the module is enabled for a tenant. Time-to-live for such a token should be quite long enough.

A special set of FOLIO permissions should be defined to allow to publish and deliver events.

#### Implementation notes
The `pubsub` implementation (`mod-pubsub`) must have its own persistent storage to store all registered event descriptors with publishers and subscribers linked to them.

A dedicated git repository can be used to store event descriptors and it must be added as a git submodule to a back-end module’s repositories. It will allow to manage event descriptors easily.

## Risks and Drawbacks
This RFC introduces the new functionality to the FOLIO platform, that leads to the increasing platform complexity.

Also, it adds a dependency on the third-party platform (Kafka). But having that behind the `mod-pubsub` allows substituting messaging vendor with a minimal impact on the FOLIO platform.

Some HTTP calls overhead will be present because all interactions between `mod-pubsub`, publishers and subscribers will be done via the HTTP protocol through the OKAPI module. 

## Rationale and Alternatives
It could be possible to implement `pubsub` functionality in the scope of OKAPI, but this will unnecessarily increase the complexity of the OKAPI module, which is currently quite complex. However, such an implementation may not be sufficiently feature rich.

As an alternative, it is possible to use a messaging platform (Kafka, RabbitMQ) directly without a proxy module. But it will add an explicit dependency on the selected messaging engine. 
Also, it forces to add some boilerplate code snippets to all modules which need to deal with publisher-subscriber functionality, or at least it will require to create some sort of shared library to be used by backend modules.
But since FOLIO is a language agnostic platform it will also have its limitations.
  

## Unresolved Questions

Now the least developed area is questions related to the security, permissions, receiving JWT tokens, etc. 
