---
layout: guidelines
title: Commit Messages
heading: Commit Messages
permalink: /guidelines/commitmessages/
---

Try to follow the commit message guidelines in
[https://chris.beams.io/posts/git-commit/](https://chris.beams.io/posts/git-commit/).
The key points are:
* Separate subject from body with a blank line
* Limit the subject line to 50 characters
* Capitalize the subject line
* Do not end the subject line with a period
* Use the imperative mood in the subject line
* Wrap the body at 72 characters
* Use the body to explain what and why vs. how

The last point is the most critical:
> A diff will tell you what changed, but only the commit message can properly tell you why.

Also consider mentioning relevant Issue identifiers (e.g. OKAPI-258).
This assists people to follow the reasons, and enables the issue tracker to
automatically link to the related commits.

