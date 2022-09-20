---
layout: null
---

# mod-spring-template

Copyright (C) 2022 The Open Library Foundation

This software is distributed under the terms of the Apache License,
Version 2.0. See the file "[LICENSE](LICENSE)" for more information.

The blueprint module that could be used as a template for FOLIO Spring-based backend modules.

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
- [How-to guide](#how-to-guide)
- [Instrumentation](#instrumentation)
  - [Spring Boot Actuator and Metrics](#spring-boot-actuator-and-metrics)
    - [How to setup Spring Boot Actuator and Endpoints](#how-to-setup-spring-boot-actuator-and-endpoints)
    - [How to setup Metrics and Prometheus](#how-to-setup-metrics-and-prometheus)
    - [Important Metrics](#important-metrics)
- [Logging](#logging)
- [Monitoring](#monitoring)
  - [Monitoring and Management over JMX](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html#actuator.jmx)
  - [Monitoring and Management over HTTP](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html#actuator.monitoring)
- [Kafka](#kafka)
  - [How to setup and integrate with Spring Boot & Kafka](#how-to-setup-and-integrate-with-spring-boot--kafka)
- [Notes](#notes)

## Introduction

This is the blueprint module that should be used as a template for FOLIO Spring-based backend modules.
It provides the initial configuration and common data schemas used by the FOLIO platform.

## How-to guide
This guide shows how to create a new folio backend module using the mod-spring-template engine

1. Clone the mod-spring-template repository from the github https://github.com/folio-org/mod-spring-template
2. Rename the folder containing the project following FOLIO naming conventions and delete the git related folder .git
3. Edit the pom.xml and provide valid values for tags
  - artifactId
  - name
  - version
  - description
4. Edit the Dockerfile and provide the correct value for APP_FILE environment variable.
5. Add OpenAPI specification file with the API provided by this new module into the src/main/resources/swagger.api folder
6. Edit the pom.xml and uncomment the usage of org.openapitools plugin.
7. Edit *DeploymentDescriptor-template.json* & *ModuleDescriptor-template.json* providing correct APIs that the module provides and a set of permissions it requires.
8. Add a main class that represents the SpringBoot application. @SpringBootApplication annotation is a must to mark the main class as a SpringBoot application. Add @EnableFeignClients to activate feign client processing to call other modules and services.
9. Add Entity classes in the entity package which will map to the tables in your database.
   ```java
    @Entity
    @Data
    public class EntityName {
       @Id
       @GeneratedValue(strategy = GenerationType.AUTO)
       @Column(updatable = false)
       private UUID id;

       // Entity fields

       // Getter/Setter methods
    }
   ```
10. To access database from Spring, create repository interfaces in repository package.
    ```java
    @Repository
    public interface RepositoryName extends JpaRepositry<T, ID> {
       // Methods to read/write data to database
    }
    ```
    where:
    T: Domain type that repository manages (Generally the Entity/Model class name)
    ID: Type of the id of the entity that repository manages (Generally the wrapper class of your @Id that is created inside the Entity/Model class)

    For more information, follow:
  * [Spring Data JPA - Reference Documentation](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/)
  * [Accessing Data with JPA](https://spring.io/guides/gs/accessing-data-jpa/)
11. DB objects(tables/columns) should be created by Liquibase and should not be created automatically by the Spring Data/Hibernate thats why in your configuration file (application.properties/application.yml), set this property to "none":
    ```yaml
    spring:
      jpa:
        hibernate:
          ddl-auto: none
    ```
12. Configure Liquibase by adding application.yml with below liquibase properties
    ```
    spring:
      liquibase:
        enabled: true
        change-log: <PATH to change-log master file>
    ```
13. Provide correct values to the application.properties file.
    1. Add maven plugin to support the OpenAPI generator project.
       <br /><br /><b>Usage</b>
       <br />Add to your build->plugins section (default phase is generate-sources phase)
    ```
       <plugin>
       <groupId>org.openapitools</groupId>
       <artifactId>openapi-generator-maven-plugin</artifactId>
       <!-- RELEASE_VERSION -->
       <version>6.1.0</version>
       <!-- /RELEASE_VERSION -->
        <executions>
           <execution>
               <goals>
                   <goal>generate</goal>
               </goals>
               <configuration>
                   <inputSpec>${project.basedir}/src/main/resources/api.yaml</inputSpec>
                   <generatorName>Spring</generatorName>
                   <configOptions>
                      <sourceFolder>src/gen/java/main</sourceFolder>
                   </configOptions>
               </configuration>
           </execution>
       </executions>
      </plugin>
    ```
    Followed by:
    ```
    mvn clean compile
    ```
    2. <b>Configuring map structures</b>
       <br />For configuring options documented as a map above, the key/value options may be configured as free-form nodes under these options.
       <br />This takes the format:
    ```
        <configuration>
            <option>
               <key>value</key>
            </option>
        </configuration>
    ```
14. To add Feign Client support:
  * Add ```@EnableFeignClients``` annotation to the main class.
```java
  @SpringBootApplication
  @EnableFeignClients
  public class Application {
    public static void main(String[] args) {
      SpringApplication.run(Application.class, args);
    }
  }
```
  * Create a feign client package and add a feign client interface
```java
@FeignClient(name = "stores", url="", configuration = FeignClientConfig.class)
public interface StoreClient {
  @GetMapping("/stores/{storeId}")
  JsonNode getStore(@RequestParam String storeId);

  @PostMapping("/stores")
  JsonNode createStore(@RequestBody Object store);
}
```
  * FeignClientConfig is a configuration class where you can create beans of Decoder, Encoder, Logger, Contract, Feign.Builder and Client to override default beans created by Spring Boot. You can also create beans of Logger.Level, ErrorDecoder and RequestInterceptor to include these features.
  * For detailed information, follow this [Feign Client Documentation](https://docs.spring.io/spring-cloud-openfeign/docs/current/reference/html/)
15. run mvn clean package to check that the build process completes successfully.
16. The skeleton for your new module is ready for further business functionality development.
17. Generated API controllers and DTOs will ****be stored in the **target/generated-sources/src/main/java** folder. The content of that folder will be automatically included in the list of source folders.
18. Note that the default implementation for TenantAPI is already provided by the folio-spring-base library. If you need to customize it or provide your own implementation please reach https://github.com/folio-org/folio-spring-base#custom-_tenant-logic for details.

# Instrumentation
## Spring Boot Actuator and Metrics
- Spring Boot Actuator module helps you monitor and manage your Spring Boot application by providing production-ready
  features like health check-up, auditing, metrics gathering, HTTP tracing etc. All of these features can be accessed
  over JMX or HTTP endpoints.
- Actuator also integrates with external application monitoring systems like [Prometheus](https://prometheus.io/)
- Spring Boot Actuator has many [capabilities](https://www.baeldung.com/spring-boot-actuators)

### How to setup Spring Boot Actuator and Endpoints
1. To add spring-boot-actuator to a spring boot application following dependency must be added -
````<dependency>
   <groupId>org.springframework.boot</groupId>
   <artifactId>spring-boot-starter-actuator</artifactId>
   </dependency>
````
2. Actuator creates several so-called endpoints that can be exposed over HTTP or JMX to let you monitor and interact with your application.
   For example, There is a /health endpoint that provides basic information about the application’s health. The /metrics endpoint shows several useful metrics information like JVM memory used, system CPU usage, open files, and much more.
3. An actuator endpoint can be enabled or disabled by setting the property management.endpoint.<id>.enabled to true or false in the application.yml file (where id is the identifier for the endpoint).
4. To expose an actuator endpoints over HTTP and JMX can be set in application.yml file as
````management:
   endpoints:
   web:
   exposure:
   include: info,health,env,httptrace
````
5. For more information about various endpoints [(click here)](https://docs.spring.io/spring-boot/docs/current/actuator-api/htmlsingle/#overview) supported by spring boot actuator.

### How to setup Metrics and Prometheus
1. Add the dependency for micrometer-prometheus as shown below
````
   <dependency>
   <groupId>io.micrometer</groupId>
   <artifactId>micrometer-registry-prometheus</artifactId>
   </dependency>

````
2. Expose the metrics and prometheus endpoints as shown
````management:
   endpoints:
   web:
   exposure:
   include: info,health,env,httptrace,metrics,prometheus
````
3. There is an option to setup prometheus locally to view the metrics. [Download](https://prometheus.io/download/) the prometheus server. Edit the prometheus.yml file to provide the -
1. Alert manager configuration
2. Metrics path
3. Targets

*As an example for local prometheus.yml file*
````
# my global config
global:
scrape_interval: 15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
# scrape_timeout is set to the global default (10s).

# Alertmanager configuration
alerting:
alertmanagers:
- static_configs:
- targets: ["localhost:9090"]
# - alertmanager:9093

# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
# - "first_rules.yml"
# - "second_rules.yml"

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
# The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
- job_name: "prometheus"

#Metrics info needed for memory,
#cpu
#DB connection

    metrics_path: '/admin/prometheus'
    # scheme defaults to 'http'.

    static_configs:
      - targets: ["localhost:8081"]

````
4. Run the local prometheus server and as per the above example hit the http://localhost:9090/graph to see various metrics for the targeted application.

### Important Metrics
1. CPU Usage - The metric used here is “node_cpu_seconds_total”. This is a counter metric that counts the number of seconds the CPU has been running in a particular mode. The CPU has several modes such as iowait, idle, user, and system. Because the objective is to count usage, use a query that excludes idle time:

   ``sum by (cpu)(node_cpu_seconds_total{mode!="idle"})``

   The sum function is used to combine all CPU modes. The result shows how many seconds the CPU has run from the start. To tell if the CPU has been busy or idle recently, use the rate function to calculate the growth rate of the counter:

   ``(sum by (cpu)(rate(node_cpu_seconds_total{mode!="idle"}[5m]))*100``

   The above query produces the rate of increase over the last five minutes, which lets you see how much computing power the CPU is using. To get the result as a percentage, multiply the query by 100.
2. Memory Usage - The following query calculates the total percentage of used memory:

   ``node_memory_Active_bytes/node_memory_MemTotal_bytes*100``

   To obtain the percentage of memory use, divide used memory by the sum and multiply by 100.

   Free Disk - You need to know your free disk usage to understand when there needs to be more space on the infrastructure nodes. Again, the same memory usage method is used here, but with different metric names.

   ``node_filesystem_avail_bytes/node_filesystem_size_bytes*100``
3. DB Usage - For the DB usage metrics Grafana can be used with PostgresSql or Postgres Exporter with Prometheus. [Click here](https://fatdba.com/2021/03/24/how-to-monitor-your-postgresql-database-using-grafana-prometheus-postgres_exporter/)
   Various pg metrics are present which can be further used to analyze the usage of DB with the application.
   Postgress Exporter can be installed from [here](https://github.com/prometheus-community/postgres_exporter)

## Kafka
### How to setup and integrate with Spring Boot & Kafka

1. Install Apache kafka from [here](https://www.apache.org/dyn/closer.cgi?path=/kafka/3.2.1/kafka_2.13-3.2.1.tgz)
2. Unzip the tgz file and tar file
3. If you have windows machine run the following commands :

````
# Start the ZooKeeper service
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties

# Start the Kafka broker service
.\bin\windows\kafka-server-start.bat .\config\server.properties

````

4. If you have linux machine run the following commands :

````
# Start the ZooKeeper service
./bin/zookeeper-server-start.sh ./config/zookeeper.properties

# Start the Kafka broker service
./bin/kafka-server-start.sh ./config/server.properties

````
5. Use kafka dependency :
````
    <dependency>
      <groupId>org.springframework.kafka</groupId>
      <artifactId>spring-kafka</artifactId>
      <version>${spring-kafka.version}</version>
    </dependency>
````

6. Use the following in application.yml file

````
spring:
  kafka:
    bootstrap-servers: ${KAFKA_HOST:localhost}:${KAFKA_PORT:9092}
    consumer:
      max-poll-records: 50
    security:
      protocol: ${KAFKA_SECURITY_PROTOCOL:PLAINTEXT}
    ssl:
      key-store-password: ${KAFKA_SSL_KEYSTORE_PASSWORD:}
      key-store-location: ${KAFKA_SSL_KEYSTORE_LOCATION:}
      trust-store-password: ${KAFKA_SSL_TRUSTSTORE_PASSWORD:}
      trust-store-location: ${KAFKA_SSL_TRUSTSTORE_LOCATION:}
    producer:
      acks: all
      properties:
        enable.idempotence: true
        max.in.flight.requests.per.connection: 5
        retries: 5
````

7. To create Topic either it can be done using shell or by creating Topic using java

````
### Using Shell :

/bin/kafka-topics.sh --create \
    --zookeeper <hostname>:<port> \
    --topic <topic-name> \
    --partitions <number-of-partitions> \
    --replication-factor <number-of-replicating-servers>

### Using Java

  @Bean
  public NewTopic generalTopic() {
     TopicBuilder.name(< topic name >)
      .partitions(< number of partition >)
      .replicas(< replication factor >)
      .build();
  }
````
8. To create Kafka Producer , Kafka Consumer and Kafka Template create a configuration file refer [here](https://github.com/folio-org/folio-sample-modules/tree/master/mod-spring-petstore/src/main/java/org/folio/petstore/configuration/KafkaConfiguration.java)
9. To send message use kafka template :

````
@Autowired
private KafkaTemplate<?, ? > KafkaTemplate;
....

KafkaTemplate.send(< topicName >, < key > , < data > );
````

10. To listen the message use kafka Listener :

````
@KafkaListener(
    topics = "< topic name >",
    concurrency = "< number of concurrency >",
    groupId = "< group ID >",
    containerFactory = "< bean of concurrentKafkaListnerFactroty >"
  )
  public void handlePetEvents(ConsumerRecord<?, ?> consumerRecord){ .. }
````

11. For testing the module container tests can be used , which require docker in the system .
12. Install docker from [here](https://docs.docker.com/desktop/install/windows-install/)
13. To write container test use testcontainers dependency
````
    <dependency>
      <groupId>org.testcontainers</groupId>
      <artifactId>kafka</artifactId>
      <version>${testcontainers.version}</version>
      <scope>test</scope>
    </dependency>
````
14. To run basic container test use the following template :

````
@SpringBootTest(classes = {...})
@Testcontainers
public class KafkaIntegrationTests {

  @Container
  private static KafkaContainer kafka = new KafkaContainer(DockerImageName.parse("confluentinc/cp-kafka:5.5.3"));

  // write tests

}
````

15. For more about Kafka and Spring boot refer [here](https://spring.io/projects/spring-kafka)

## Logging
See the logging configuration and usage from [here](https://github.com/folio-org/folio-spring-base#logging)
## Monitoring
The runtime framework via the `/admin` API exposes (as previously mentioned) some APIs to help monitor the service (setting log levels, DB information).
Some are listed below (and see the [full set](https://docs.spring.io/spring-boot/docs/2.7.3/actuator-api/htmlsingle/):

- `/admin/jstack` -- Stack traces of all threads in the JVM to help find slower and bottleneck methods.
- `/admin/memory` -- A jstat type of reply indicating memory usage within the JVM on a per pool basis (survivor, old gen, new gen, metadata, etc.) with usage percentages.
- `/admin/info` -- The info endpoint provides general information about the application.
- `/admin/env` -- The env endpoint provides information about the application’s Environment.
- `/admin/metrics` -- The metrics endpoint provides access to application metrics.
- `/admin/prometheus` -- The prometheus endpoint provides Spring Boot application’s metrics in the format required for scraping by a Prometheus server.
- `/admin/liquibase` -- The liquibase endpoint provides information about database change sets applied by Liquibase.
- `/admin/health` -- Returns status code 200 as long as service is up.



## Notes

A detailed description of the functionality provided by folio-spring-base java library you can find on https://github.com/folio-org/folio-spring-base page.

Spring-based folio modules must follow best practices for spring boot applications. The folio-spring-base has been intentionally designed to provide the minimum of FOLIO specific functionality. The Spring projects should be used to cover the common functionality like DB connection, integration with Kafka, Elasticsearch, etc.

It is highly recommended to use only community approved Spring projects in the FOLIO backend modules.
If you need to use the Spring project that is not still used in FOLIO please discuss that with the community first.

The database that is used in FOLIO for general persistence tasks is PostgreSQL. If you need to use different storage for your functionality, please discuss it with the community first.

Here are the links to some production backend modules based on the folio-spring-base. You can check various details of implementations there.

- https://github.com/folio-org/mod-tags
- https://github.com/folio-org/mod-password-validator
- https://github.com/folio-org/mod-quick-marc
- https://github.com/folio-org/mod-inn-reach
- https://github.com/folio-org/mod-search


### Spring projects used in FOLIO

- Spring Framework https://spring.io/projects/spring-framework that includes:
  - Core technologies: dependency injection, events, resources, i18n, validation, data binding, type conversion, SpEL, AOP.
  - Testing: mock objects, TestContext framework, Spring MVC Test, WebTestClient.
  - Data Access: transactions, DAO support, JDBC, ORM, Marshalling XML.
  - Spring MVC and Spring WebFlux web frameworks.
  - Integration: remoting, JMS, JCA, JMX, email, tasks, scheduling, cache.
- Spring Boot https://spring.io/projects/spring-boot
- Spring Data JPA https://spring.io/projects/spring-data-jpa
- Spring for Apache Kafka https://spring.io/projects/spring-kafka
- Spring Batch https://spring.io/projects/spring-batch

