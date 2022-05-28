---
layout: page
title: Performance optimization
permalink: /guides/performance-optimization/
menuInclude: no
menuTopTitle: Guides
---

Some notes to assist with performance optimization.

## Call graphs with Giraffe

Giraffe is a tool for creating visualizations of Okapi logs such as call graphs.

Process a snippet of Okapi logfile. Highlight response times that meet a specified threshold.

[https://github.com/library-data-platform/giraffe](https://github.com/library-data-platform/giraffe)

## DB schema

[Explain DB schema and performance issues](/faqs/explain-database-schema/)

## Performance report

The [Monitoring and performance](/guides/automation/#monitoring-and-performance) section links to the daily performance reports.

Configuration is at the [https://github.com/folio-org/folio-perf-test](https://github.com/folio-org/folio-perf-test) repository.
This is a Jenkins pipeline using Apache JMeter to test FOLIO performance.

