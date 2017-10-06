---
layout: guidelines
title: Merging Pull Requests
heading: Merging Pull Requests
permalink: /guidelines/mergepullrequest/
---

When someone has assigned a pull request to you, check out the branch, and
look at the git log, and the code, and decide whether all is good.
You can also look at the commit messages and code changes in GitHub.

If there are small details, you can fix them yourself, commit and push to the
branch. Do not copy & paste the content as this loses the commit history that
contains the attribution required by the Apache License and is used for the
[merge check](https://git-scm.com/book/en/v2/Git-Branching-Branch-Management)
of the `git branch` command; if needed create a new branch from pull request's branch.

If there are serious issues, you can close the pull request without
merging, with a comment explaining why you could not do it.

Once all is well, you can use GitHub's interface. Just go to the
conversation tab, and click on _Merge Pull Request_ (don't squash, don't rebase,
[learn why](https://git-scm.com/book/en/v2/Git-Branching-Rebasing#The-Perils-of-Rebasing)).
Edit the comment if
necessary, and click on _Confirm Merge_. GitHub should tell you that the
_Pull request successfully merged and closed_. Next to it is a button to
_Delete the Branch_. For a simple feature branch, you might as well delete
it now, it has served its purpose. But if you think there is more work that
should be done in this branch, of course you don't delete it.

This merging of the pull request's branch okapi-xxx can also be done on the
command line, if you prefer.

    git checkout master
    git merge okapi-xxx

When done, you probably want to delete the local branch from your own machine

    git branch -d okapi-xxx