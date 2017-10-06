---
layout: guidelines
title: Git and Branches
heading: Git and Branches
permalink: /guidelines/contrib-code/
---

For all FOLIO code repositories, we are trying to follow
[GitHub Flow](https://guides.github.com/introduction/flow/).

In short, the master branch is always the head of latest development. Anything
merged into master should be of such good quality that at any time a snapshot
from master passes all tests, and can be deployed. That is not to say that it
will be free of bugs; we are not superhuman.

All real work should be done in feature branches. It is still OK to make a
small trivial change directly in the master. Stuff like editing the README.

People who do not have direct write permissions will need to "fork" the
relevant repository. See the GitHub notes about
[working with forks](https://help.github.com/articles/working-with-forks/).

