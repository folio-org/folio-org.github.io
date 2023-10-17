---
layout: null
---

# Folio RFCs

For process overview, please see https://wiki.folio.org/display/TC/RFC+Process

## Getting started

* Fork the official RFC repo at https://github.com/folio-org/rfcs . This is usually only needed once for any number of RFCs to be submitted.
* Create a file in the text directory at the top of the forked repo. It should follow the template defined here. Ensure that the file is named appropriately, taking note of the sequence numbers of existing RFCs.
* Fill in the RFC. Put care into the details: RFCs that do not present convincing motivation, do not demonstrate understanding of the impact of the design, or are disingenuous about the drawbacks or alternatives tend to be poorly-received.
* In the forked repo on GitHub, create a PR comparing the branch where edited file is located to the master branch of the official RFC repo. Ensure the name of the pull request has the name of the RFC phase at the beginning. e.g. "[DRAFT REVIEW] Java 17" or "DRAFT REVIEW | Java 17"
* As a pull request the RFC will receive design feedback from the larger community, and the author should be prepared to revise it in response.
* The Technical Council will assign one or more reviewers to the RFC pull requests and the feedback process will begin. See the wiki for more details: https://wiki.folio.org/display/TC/RFC+Process 
  

## The RFC Lifecycle

The following states represent the lifecycle of the RFC. The states are implemented as “Labels” on the GitHub pull request corresponding to the RFC draft.

* **Submitted**: initial state of RFC when submitted by their authors
* **Under Review**: RFC has been assigned to one or more reviewers
* **In Final Review**: RFC is in the final review period
* **Accepted**: RFC has been accepted but is not yet ready for implementation.
* **Active**: RFC has been accepted and is now ready for implementation
* **Rejected**: RFC has been rejected and is now effectively closed.


**Folio’s RFC process owes its inspiration to the [Ember] and [Rust] RFC processes.**

[Ember]: https://github.com/emberjs/rfcs
[Rust]: https://github.com/rust-lang/rfcs

