---
layout: source
title: Overview
heading: Source Code
permalink: /source/index/
---

The FOLIO platform consists of both server-side and client-side components, and
will grow to include library services that run on the platform as modules.
Some sample modules are located in
[folio-sample-modules](https://github.com/folio-org/folio-sample-modules).

Several repositories in the [folio-org GitHub
organization](https://github.com/folio-org) host the core project code.
Third-party modules may be hosted elsewhere.

A good starting point for understanding the FOLIO code is
[Okapi](https://github.com/folio-org/okapi) -- specifically the
[Okapi Guide and Reference](https://github.com/folio-org/okapi/blob/master/doc/guide.md), which
introduces the concepts and architecture of the FOLIO platform, and includes
installation instructions and examples.  Okapi is the central hub for
applications running on the FOLIO platform and enables access to other modules
in the architecture.

The FOLIO system is made up of the code in several GitHub repositories.
Each repository contains the code for a single well-defined element of the
system. These repositories fall into three categories:

- _server-side elements_ that provide services and the
  infrastructure that they run on;
- _client-side elements_ that provide a
  framework for using those services from a Web browser;
- and a few that fall into neither of these categories.

**PLEASE NOTE** that this is a technology preview following the [release early,
release often](https://en.wikipedia.org/wiki/Release_early,_release_often)
philosophy.  **We want your feedback** in the form of pull requests and filed
issues and general discussion via the
[collaboration tools](/community/).

