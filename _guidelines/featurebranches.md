---
layout: guidelines
title: Feature Branches
heading: Feature Branches
permalink: /guidelines/featurebranches/
---

Feature branches should be branched off from the master. The naming of those
is not strict, but if you start a branch to fix issue okapi-xxx filed in
[issues.folio.org](https://issues.folio.org/) then you might well call the
branch _okapi-xxx_ (or if you want to be more descriptive, something
like _okapi-xxx-contribution-guidelines_):

    git checkout -b okapi-xxx

You can commit stuff as you go, but try not to push obviously broken stuff into
GitHub, not even in your development branch -- that will be visible for the
whole world, and we plan to set up automatic testing for each branch, so
pushing a broken commit will cause some emails. But if you need to share the
code, for example for collaborating, of course you need to push it. Naturally
you will write decent commit messages explaining what you have done.

The first time you want to push your branch to GitHub, you may encounter an
error _The current branch okapi-xxx has no upstream branch_. Git tells you
what to do, namely:

    git push --set-upstream origin okapi-xxx

Once you have done that once, a simple `git push` will be sufficient
thereafter.

While developing your own branch, pull in the master every now and then, and
resolve any conflicts that may be there. If you don't, your branch
will diverge further from master, and the final merge of your work
back into master will be difficult to resolve.

When you are all done, pull master in again, to make sure your branch merges
cleanly and passes all tests. Commit the merge, and push to your branch:

    git push

You may also want to `git rebase` your branch, compressing multiple commits
into one, and editing the commit messages.
