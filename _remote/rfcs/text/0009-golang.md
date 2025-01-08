---
layout: null
---


- Contributors:
  - [Jakub Skoczen](jakub@indexdata.com)
  - [Mike Taylor](mike@indexdata.com)
- RFC PRs: 
  - PRELIMINARY REVIEW: https://github.com/folio-org/rfcs/pull/25
  - DRAFT REVIEW: https://github.com/folio-org/rfcs/pull/27
  - PUBLIC REVIEW: https://github.com/folio-org/rfcs/pull/30
  - FINAL REVIEW: https://github.com/folio-org/rfcs/pull/33
- Outcome: ACCEPTED

# Add GO programming language to FOLIO Officially Supported Technologies

## Summary

With this RFC, we are proposing to evaluate the Go language through an incubation project and eventually extend the FOLIO Officially Supported Technologies [list](https://wiki.folio.org/display/TC/Officially+Supported+Technologies) with the [Go](https://go.dev/) programming language for backend development. 

## Motivation

We think that Go has compelling characteristics that make it a solid and safe choice for building enterprise applications and network services. 

Specifically for FOLIO development, we believe that Go will complement the list of already supported backend languages and that [many conscious decisions in the design of the language and its core library](https://go.dev/talks/2012/splash.article) make it well-suited for FOLIO microservices-inspired architecture and open, community-first collaborative project structure. 

## Detailed Explanation/Design

FOLIO backend module development has relied primarily on Java and most FOLIO backend modules, with a few exceptions, are written in Java. Java is a good fit for writing backend and web services with good performance and safety characteristics. But it can also lead to complex and highly layered codebases and impose a high-barrier of entry for full-stack developers. We believe Go possesses characteristics that address these challenges.

Go is a statically-typed, natively-compiled programming language with syntax based on the C family of programming languages (C, Java, C#, etc). Go has been created at Google by Rob Pike and Ken Thompson in 2007 to "[improve programming productivity in an era of multi-core, networked machines and large codebases](https://go.dev/solutions/google/)". Go, like Java, provides automatic memory management through the use of garbage collector but, compared to Java, has a simpler programming model with optional classes/OOP, no inheritance and no exceptions for regular error handling.

Thanks to its design, Go has a high level of familiarity for Java (and C#) developers. This includes both the language syntax and programming constructs, as well as the runtime characteristics. As previously mentioned, like Java, Go is a statically typed, compiled language with a garbage collector. While Go redefines some basic concepts like loops or conditionals (e.g there's no while loop in Go and the switch statement does not fall through) there are few paradigm-shifting concepts, with the concurrency model (there's no direct equivalent of Go's goroutines in Java) and more control over memory management (pointers and stack vs heap allocation) being some examples where the languages differ substantially.  This familiarity means that a Java programmer can become proficient with the Go language relatively quickly, for instance through the duration of a small development project, including idiomatic use of some of the constructs that differ from Java. Similarity to Java also means that the developer can “read” Go source code with limited prior knowledge of the language, referring only occasionally to the language documentation. 
 
The simplicity of Go stems from the fact that, unlike Java, it is not a multi-purpose tool. Go's main uses cases are web services and CLIs (command-line interfaces) which makes it a perfect fit for writing FOLIO backend modules. Being simpler than Java, the language is also easier to pick up by full-stack developers coming from scripting and web languages background like Node.js or Python. This can be a big advantage for small teams of few developers as the entire team can, effectively, be kept full-stack. With large Java codebases it’s not practical and developers in the team usually specialize in front-end or back-end programming. 

On the operational front, Go's characteristics make it a better fit than Java for building systems comprised of many small microservices. Go is compiled ahead-of-time (AOT) into a static binary which is a perfect fit for Docker containers. AOT compilation means that the resulting application has a visibly smaller memory footprint and faster startup times as compared to Java/vert.x, and orders of magnitude better as compared to Java/Spring based modules. Java provides AOT compilation capability through the GraalVM project, but porting existing Java projects to GraalVM involves substantial complexity and is not possible for certain frameworks like older Spring (including versions used by FOLIO project) and Grails due to the dynamic language features they require. 

From a sysops perspective, Go containers require less operational tuning compared to the JVM containers as they do not contain a stand-alone virtual machine that requires parametrization.

The Go language is widely used across the industry and open-source communities, especially in the areas related to web and microservices. Popular examples of large open-source projects created with Go include the [Kubernetes](https://github.com/kubernetes/kubernetes) container orchestration platform and the [Docker](https://github.com/docker) container runtime.

The Go project maintains a [list](https://go.dev/solutions/) of case-studies from commercial companies relying on Go in their products and general use-cases for the language.

According to [GitHub statistics](https://madnight.github.io/githut/#/pull_requests/2023/3), Go is the third fastest growing language (behind Python and Java) as measured by the number of new Pull Requests.

## Risks and Drawbacks

Introducing Go as one of the supported backend technologies involves the same general concerns as introducing any new technology into FOLIO. The biggest potential risk is the increased development and maintenance complexity as some new FOLIO backend modules will be created with Go which is not immediately well known to existing FOLIO backend developers that have primarily Java background. As explained in the previous section, however, this risk is contained because of the design of Go which, while being a different language, has many points of similarity to Java. It should be noted that while Go is an OOP language and supports both interfaces and generics, it doesn't support inheritance, only extension through composition is supported.

The top three challenges from the Go Developer Survey 2024 H1 are:

* Learning how to write Go effectively
* The verbosity of error handling
* The Go ecosystem is missing libraries of frameworks I need

Another drawback worth mentioning is that a subset of the shared library functionality used by Java modules must be implemented in the form of a shared Go library. The library can, however, be kept simple and include only the most fundamental functionality, similar to [folio-vertx-lib](https://github.com/folio-org/folio-vertx-lib).

Additionally, as history of FOLIO development shows, there exists high level of affinity between specific teams of developers and particular modules and domains. This affinity often results in siloing and can create barriers preventing wider collaboration between various development teams. This siloing exists even within Java-only usage in FOLIO (vert.x vs Spring) because of the high reliance on web programming frameworks. Development in Go has less or no reliance on frameworks -- for instance it's entirely possible to develop FOLIO modules with only Go standard library, Postgres client library and OpenAPI parser library. This more lightweight approach to development can ease some of the cross-module development barriers in FOLIO.

Another risk flagged during the RFC review is that the FOLIO community mostly has only has Java developers today and it might struggle to attract Go developers in the future and that would make supporting Go modules over the long term harder to achieve

## Rationale and Alternatives

As explained in the design section, Go is a programming language well-suited to writing backend web services and, as such, is a perfect fit for FOLIO's microservices-inspired architecture. It is also an increasingly popular language with community-driven open-source projects thanks to its simplicity and familiar syntax but without the performance tradeoffs typical to dynamic or scripting languages.

Go's excellent AOT compilation support puts it ahead of Java for building systems that comprise of many small, containerized workloads.

As such there's no direct alternative to Go available in the FOLIO ecosystem.

## Timing

We propose that Go be added as an incubating technology in Ramsons with the attempt to execute a pilot project. The pilot will serve as the technology preview to validate Go's fit for FOLIO backend development. While it might be a good idea to directly compare Java and Go by re-implementing an existing module it should be stressed that during the pilot phase, any new module written in Go will be considered strictly a proof-of-concept and there's no guarantee the module will remain a part of the FOLIO release. 

In the case Go is deemed unsuitable for FOLIO development, the PoC module developed in Go will be removed from future FOLIO versions, and Go will not be accepted as a supported technology.

In the case Go is deemed suitable for FOLIO backend development, it will be accepted to the official technology list starting from the Sunflower release.

We do not expect this RFC and Go's admission to the officially supported technology list to have any impact on release planning for Ramsons or Sumflower or cause any additional workload for development teams. Index Data DevOps will provide initial support with regard to the CI/CD pipelines to development teams wanting to build FOLIO modules in Go.

## Unresolved Questions
