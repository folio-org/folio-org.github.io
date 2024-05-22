---
layout: null
---

- Contributors:
  - [Julian Ladisch](julian.ladisch@gbv.de)
  - [Florian Gleixner](Florian.Gleixner@lrz.de)
- RFC PRs: 
  - PRELIMINARY REVIEW: https://github.com/folio-org/rfcs/pull/23
  - DRAFT REVIEW: https://github.com/folio-org/rfcs/pull/28
  - PUBLIC REVIEW: https://github.com/folio-org/rfcs/pull/28
  - FINAL REVIEW: TBD
- Outcome: (Leave this blank.  Will eventually be either ACCEPTED or REJECTED)


# Folio distributed vs. centralized configuration

## Summary

Drop mod-configuration module. Favour distributed configuration over centralized configuration, provide guidelines for storage of configuration values.

## Motivation

FOLIO relies on a tenant aware extendable microservice system. It is highly configurable and adoptable on all kind of requirements. FOLIO had no strict guidelines for developers, how and where to store the configuration values. This led to a situation where different approaches where developed by different developer teams.
This makes it difficult for implementers, administrators and users to configure the system appropriate, as they may have to search the documentation how to read or write these configuration values.
Basically there are two competing concepts where to store the values: distributed in the owning modules or centralized in a special module that offers a configuration store for other modules. There exist two solutions for centralized configurations: mod-settings and mod-configuration (deprecated, to be dropped).
This RFC shall give guidelines for developers, where configuration values shall be set.

## Detailed Explanation/Design

This RFC deals with configurations that configure the behaviour of the Folio tenant. Among all different kinds of configurations, this RFC does not deal with the following configurations, as their location and method to set/get them shall not be changed:

* Settings stored in Okapi's /_/env APIs.
* Settings stored in Infrastructure (Kubernetes / Rancher) config maps and secrets.
* Settings stored in module container environment variables.
* Settings stored in the stripes front-end (stripes.config.js, etc.)

### Use of mod-configuration will be discontinued after Ramsons release

mod-configuration is deprecated due to security problems since March 2022. It shall not be used any more to add new configuration variables. Modules still using mod-configuration have to move to other solutions after the Ramsons release.

### Distributed configuration is preferred

Distributed configuration means, that each module stores its configuration values itself, and offers API endpoints to query and store these values. Distributed configuration in a microservice architecture has some advantages:

* The modules can validate the values according to format and dependencies
* Modules do not depend on a configuration module, hence a better separation of microservices can be achieved
* Since all API endpoints have to be documented, a basic documentation of possible configuration variables is mandatory
* Configuration values can be cached, since no other module can change values.
* Access to configuration values can effectively controlled by permissions defined in the module.
* Write-only configuration values are possible, like for credentials. The module can offer other operators than reading values like comparing hashes (possible in central configuration too?)
* Modules can handle upgrade of configuration variable names or values during module upgrades more flexible

Even when there are also some drawbacks on distributed configuration, it is the preferred way to configure backend modules in FOLIO.

### When to use central configuration

mod-settings solves the security problems of mod-configuration. It is the preferred module if configuration variables shall be stored centrally. It is not recommended to develop specialized modules for other central configuration store.

Centralized configuration can only be used for either:

* Non-sensitive information, that are used by many modules or are completely independent of any module. One example are locale settings.
* Configurations that are specific to a user.

While these configurations can also be stored decentralized in a module, the developer can decide where these values shall be stored.

### Migration

See Timing Section below.

## Risks and Drawbacks

Migrations from old mod-configuration can fail, and therefore tenant upgrades may fail.
Distributed configuration requires more developer effort than central configuration.

## Rationale and Alternatives

Both central and distributed configurations were discussed. 
While pure central configuration offers easier access to the complete configuration of a tenant, this is not desireable since:
* it is an antipattern in a microservice architecture ([shared persistence/data ownership](https://arxiv.org/ftp/arxiv/papers/1908/1908.04101.pdf))
* validation of values is not possible
* differentiating configuration data and application data is not easy: are circulation rules configuration data or application data?

A pure distributed configuration has the following drawbacks:
* for centrally used configuration values, like locale settings, an owning module has to be found. It may not be intuitive finding out, which module holds these configurations.

Therefore a distributed configuration with some exceptions has been considered.

## Timing

Since most modules already store configuration values in a distributed way, only some cases need to be addressed.
For locale properties and other properties still residing exclusively in mod-configuration, the access to these properties has to be moved to the module (distributed configuration, preferred) or to the mod-settings (centralized configuration, not preferred) after the Ramsons release. Therefore a mod-configuration module offering only READ and DELETE APIs will run in Sunflower and the modules still using mod-configuration have to transfer their properties to mod-settings or to a distributed configuration. Migrated configurations in mod-configuration have to be deleted. This has to be done during module upgrades.
mod-configuration will be removed in the release following the Sunflower release.

## Unresolved Questions

None at the moment.
