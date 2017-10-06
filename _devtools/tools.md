---
layout: devtools
title: Tools
heading: Tools
permalink: /devtools/tools/
---

<!-- ../../okapi/doc/md2toc -l 2 -h 3 setup.md -->

Developers will probably want to explore the whole FOLIO system, so would need a local instance of Okapi and
[server-side](/source/serverside) modules,
and the [client-side](/source/clientside) Stripes toolkit.

Note that some parts of the development environment could be handled using
[folio-ansible](https://github.com/folio-org/folio-ansible) (virtual machines using Vagrant and Ansible).

Otherwise the development environment would need the following fundamental tools:

* Apache Maven (3.3+) and Java (8+) -- For building and deploying Okapi and some server-side modules.
* Node.js (6+) -- For Stripes and for some modules.
* Docker -- Recommended method for deployment.

As each FOLIO component can utilise whatever suite of appropriate tools, refer to its requirements and notes to assist with setup.

## Minimum Versions

Occasionally it becomes necessary to specify minimum versions of some tools:

* Java: [1.8.0-101](/devtools/troubleshooting#missing-certificate-authority-for-lets-encrypt)

## Other Tools

* PostgreSQL -- For running an external database to support storage modules.
This will enable faster startup and operations during development.
Note that this is not required to be installed for running modules using the "embed_postgres" option.
