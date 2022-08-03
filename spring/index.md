---
layout: page
title: Spring-Way overview
permalink: /spring-way/
menuInclude: yes
menuLink: yes
menuTopTitle: Spring-Way
menuTopIndex: 4
menuSubTitle: Spring-Way overview
menuSubIndex: 1
---
## Spring-Way

Spring-Way should be considered the primary choice as RAML Module Builder is no longer being extended with new functionality and is in maintenance mode only.

The Spring Way defines the module’s development approach for FOLIO platform using the Spring framework and Spring projects. It consists of:
- a lightweight [FOLIO Spring Base library](https://github.com/folio-org/folio-spring-base) containing the basic functionality and main dependencies required for developing FOLIO modules using the Spring framework;
- a set of approved Spring projects could be used in FOLIO;
- a [template repository](https://github.com/folio-org/mod-spring-template) that must be used to start a new spring-based FOLIO module.

The list of approved Spring projects to be used in FOLIO:
- Spring Framework [https://spring.io/projects/spring-framework](https://spring.io/projects/spring-framework) that includes:
  - Core technologies: dependency injection, events, resources, i18n, validation, data binding, type conversion, SpEL, AOP.
  - Testing: mock objects, TestContext framework, Spring MVC Test, WebTestClient.
  - Data Access: transactions, DAO support, JDBC, ORM, Marshalling XML.
  - Spring MVC and Spring WebFlux web frameworks.
  - Integration: remoting, JMS, JCA, JMX, email, tasks, scheduling, cache.
- Spring Boot [https://spring.io/projects/spring-boot](https://spring.io/projects/spring-boot)
- Spring Data JPA [https://spring.io/projects/spring-data-jpa](https://spring.io/projects/spring-data-jpa)
- Spring for Apache Kafka [https://spring.io/projects/spring-kafka](https://spring.io/projects/spring-kafka)
- Spring Batch [https://spring.io/projects/spring-batch](https://spring.io/projects/spring-batch)

A detailed description of the functionality provided by folio-spring-base java library you can find on [https://github.com/folio-org/folio-spring-base](https://github.com/folio-org/folio-spring-base) page.

Please find a step-by-step guide on how to create a new FOLIO Spring based module at [https://github.com/folio-org/mod-spring-template](https://github.com/folio-org/mod-spring-template).

An example of the module based on folio-spring-base could be found at [https://github.com/folio-org/folio-sample-modules/tree/master/mod-spring-petstore](https://github.com/folio-org/folio-sample-modules/tree/master/mod-spring-petstore).

Spring-based folio modules must follow best practices for spring boot applications. The [folio-spring-base](https://github.com/folio-org/folio-spring-base) has been intentionally designed to provide the minimum of FOLIO specific functionality. The Spring projects should be used to cover the common functionality like DB connection, integration with Kafka, Elasticsearch, etc.

It is highly recommended to use only community approved Spring projects in the FOLIO backend modules.
If you need to use the Spring project that is not still used in FOLIO please discuss that with the community first.

The database that is used in FOLIO for general persistence tasks is PostgreSQL. If you need to use different storage for your functionality, please discuss it with the community first.

Here are the links to some production backend modules based on the folio-spring-base. You can check various details of implementations there.

- [https://github.com/folio-org/mod-tags](https://github.com/folio-org/mod-tags)
- [https://github.com/folio-org/mod-password-validator](https://github.com/folio-org/mod-password-validator)
- [https://github.com/folio-org/mod-quick-marc](https://github.com/folio-org/mod-quick-marc)
- [https://github.com/folio-org/mod-inn-reach](https://github.com/folio-org/mod-inn-reach)
- [https://github.com/folio-org/mod-search](https://github.com/folio-org/mod-search)

