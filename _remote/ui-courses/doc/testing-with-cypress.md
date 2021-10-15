---
layout: null
---

# Testing Stripes modules with Cypress and Yakbak

Mike Taylor, Index Data. &lt;mike@indexdata.com&gt;

6th-20th July 2020.

<!-- md2toc -l 2 testing-with-cypress.md -->
* [Introduction](#introduction)
* [Components of a testing regimen](#components-of-a-testing-regimen)
    * [The components](#the-components)
        * [Cypress to run tests against the UI](#cypress-to-run-tests-against-the-ui)
        * [Stripes CLI to provide the UI](#stripes-cli-to-provide-the-ui)
        * [FOLIO backend](#folio-backend)
        * [Yakbak proxy](#yakbak-proxy)
    * [Scenarios](#scenarios)
        * [Overview](#overview)
        * [Scenario 1. Testing against the Snapshot UI](#scenario-1-testing-against-the-snapshot-ui)
        * [Scenario 2. Local UI against the Snapshot backend](#scenario-2-local-ui-against-the-snapshot-backend)
        * [Scenario 3. Regenerating the mocked backend](#scenario-3-regenerating-the-mocked-backend)
        * [Scenario 4. Local UI against the mocked backend](#scenario-4-local-ui-against-the-mocked-backend)
        * [Summary](#summary)
* [Setting up Cypress](#setting-up-cypress)
    * [Initialization and pruning](#initialization-and-pruning)
    * [Jenkins integration](#jenkins-integration)
    * [ESLint configuration](#eslint-configuration)
    * [Measuring code coverage](#measuring-code-coverage)
        * [Instrumenting the code](#instrumenting-the-code)
        * [Writing coverage data to files](#writing-coverage-data-to-files)
            * [!!! WARNING: LARK'S VOMIT !!!](#-warning-larks-vomit-)
        * [Generating coverage reports](#generating-coverage-reports)
* [Repeated requests when using YakBak](#repeated-requests-when-using-yakbak)
    * [The problem](#the-problem)
    * [Solutions](#solutions)
        * [Write tests not to make the same request twice](#write-tests-not-to-make-the-same-request-twice)
        * [Yakbak proxy inserts serial numbers into requests](#yakbak-proxy-inserts-serial-numbers-into-requests)
        * [Yakbak proxy inserts serial numbers into duplicate requests](#yakbak-proxy-inserts-serial-numbers-into-duplicate-requests)
        * [Excise `id` fields from POST requests](#excise-id-fields-from-post-requests)
        * [Re-use tapes until the next write event](#re-use-tapes-until-the-next-write-event)
        * [Something cleverer that I've not thought of yet](#something-cleverer-that-ive-not-thought-of-yet)
* [What next?](#what-next)




## Introduction

In summer of 2020, as it became apparent that automated UI tests would be required for [FOLIO](https://www.folio.org/)'s [Course Reserves module `ui-courses`](https://github.com/folio-org/ui-courses), there was an opportunity to reassess how we go about testing in the world of Stripes (FOLIO's UI toolkit).

Previously, testing had taken two separate tracks: the use of [NightmareJS](http://www.nightmarejs.org/) to automate end-to-end testing for integration tests; and of [BigTest](https://bigtestjs.io/), including its mocking facilities, to create unit tests that do not require a FOLIO backend to be available. So UI modules have Nightmare-based integration tests, some have BigTest-based unit-tests and some have both. Both NightmareJS and BigTest are rather elderly, and not well supported. Almost all UI modules' tests are flaky, due largely to deficiencies in the Nightmare and BigTest libraries that they are based on. As a result, UI test maintenance is a major resource sink in the FOLIO project.

We investigated alternative approaches, documenting the issues and outcomes in [_Notes on automated UI tests_](testing-notes.md). The present document can be considered a sequel to that one, and lays out in more detail how we implement the chosen alternative approach.

The new approach used in testing Course Reserves is:
* [Cypress](https://www.cypress.io/) for browser automation to drive tests, including the [Mocha testing framework](https://mochajs.org/) and [Chai assertion library](https://www.chaijs.com/) that it provides.
* [Yakbak](https://github.com/flickr/yakbak) to record "tapes" of interactions with the backend and play them back.

Using YakBak in this way makes it possible write a single set of tests in Cypress. The tests can exercise the whole FOLIO stack in integration testing, writing Yakbak tapes as a side-effect; and they can exercise the frontend alone in unit testing, reading Yakbak tapes to mock the backend.

(There are other and lower levels of unit-testing that might also be desirable, such and verifying that individual React components render their data in the expected way. The present document does not address this level of testing.)




## Components of a testing regimen

First we will consider the four primary components of the testing system; then we will analyse the different ways of plugging them together.



### The components


#### Cypress to run tests against the UI

[Cypress](https://www.cypress.io/) is a much more modern and all-embracing browser automation framework than Nightmare. It comes with test-running (via Mocha) and assertion evaluation (via Chai) baked in. Crucially, it runs the JavaScript of the tests from _within_ the browser. This has several valuable consequences:
* The testing dashboard is shown in a sidebar on the browser.
![Cypress in action](cypress-in-action.png)
* Tests can be paused while running and single-stepped.
* After they have run, you can "time travel" to see the browser's state at different points in the process by navigating through the list of tests in the sidebar.
* Tests have the option of usin state from within the browser: for example, logging out of FOLIO by directly invoking `localforage.removeItem('okapiSess')`.

Running Cypress tests also leaves behind useful artifacts: a video of the browser throughout the run, and screenshots of the various fail states.

Cypress has
[voluminous and helpful documentation](https://docs.cypress.io), including both
[tutorials](https://docs.cypress.io/guides/overview/why-cypress.html#In-a-nutshell)
and
[reference guides](https://docs.cypress.io/api/api/table-of-contents.html);
and
[a Gitter](https://gitter.im/cypress-io/cypress)
(Slack-like discussion app) where questions are usually answered helpfully and promptly.


#### Stripes CLI to provide the UI

Cypress can run directly against a hosted FOLIO UI such as [FOLIO Snapshot](https://folio-snapshot.dev.folio.org/) (see Scenario 1 below) but most of the time its value is in running against a local frontend built from the current source-code of the module being tested.

Stripes bundles are built by [the Stripes CLI](https://github.com/folio-org/stripes-cli/). It can build an app or set of apps into a bundle of static files to be served by any HTTP server, or it can build the bundle in memory and serve it itself. The latter mode is most useful in development as it can respond quickly to changes in the source code.

The Stripes CLI has built-in support for tests based on NightmareJS or BigTest, but not for other frameworks including Cypress. It turns out that this does not matter too much: it's possible simply to launch the CLI in build-and-serve mode, and run tests against it. The facilities that it provides to Nightmare tests -- access to a config structure and some helper functions -- would be nice to have in Cypress, but are not indispensible.


#### FOLIO backend

A FOLIO backend is a big, heavy unit, containing an [Okapi](https://github.com/folio-org/okapi) fronting a set of at least a dozen modules, often many more. Running a FOLIO backend is a laborious inconvenience for a frontend developer. This can be ameliorated by using a "FOLIO-in-a-box" virtual machine [provisioned by Vagrant](https://github.com/folio-org/folio-ansible), but the resulting VM is memory-hungry and best avoided where possible.

As a result, UI testing is often most conveniently performed against one of the public FOLIO nodes. There are
[several of these](https://dev.folio.org/guides/automation/)
including
[Fameflower-Dev](https://folio-fameflower.dev.folio.org/),
[Snapshot](https://folio-snapshot.dev.folio.org/)
and
[Snapshot-Stable](https://folio-snapshot-stable.dev.folio.org/). Since Snapshot is the most frequently updated of these (and therefore most likely to have fully up-to-date back-end modules), we will refer to it throughout this document, but any FOLIO backend can be used.


#### Yakbak proxy

While the Yakbak library provides all the facilities we need to record and play back tapes in place of a real FOLIO backend, it can be awkward to integrate. Typically, the tests themselves are wired to know about Yakbak, to start and configure a Yakbak server, and to direct their requests to it rather than to the real backend. This introduces additional complexity to the tests and spreads responsiblity in an error-prone way.

Instead, we created [`yakbak-proxy`](https://github.com/folio-org/yakbak-proxy), a simple standalone program that proxies HTTP requests to a nominated real server, while recording and/or playing back tapes. The [the usage documentation](for details), but most importantly the proxy may be run in `--norecord` mode, in which case it will _never_ call out to the real backend but only serve responses from tapes that it has previously made.

(The Yakbak proxy can of course be used with any server-client system to generate and replace tapes. In particular, it can be used to record the responses for the existing Nightmare-based tests of other Stripes apps.)



### Scenarios


#### Overview

The software components described above can be plugged together in various combinations to exercise different parts of the system in different ways.

We are now in a position to examine four testing scenarios. In the diagram below, blue boxes represent Cypress driving a Web browser; yellow boxes represent a Stripes UI (deep yellow for a remote hosted UI and pale yellow for a local UI in developement); purple boxes represent the Yakbak proxy; and green boxes represent FOLIO backends. As noted above, we describe this arrangement using FOLIO Snapshot as the backend, but any running backend can be used.

![Diagrams of four testing scenarios](testing-scenarios.svg)

We can now examine each scenario is more detail.


#### Scenario 1. Testing against the Snapshot UI

In the simplest scenario, the Cypress tests run against a remote UI, such as that provided by FOLIO Snapshot. This is useful for two reasons: to get Cypress testing up and running with minimal scaffolding, and to verify that deployed versions of a FOLIO app pass the tests.

THe default UI tested by Cypress is specified by the `baseUrl` entry in the `cypress.json` configuration file. However, this can be overridden at run-time by the `-config` option of the Cypress CLI as follows:

	cypress run --config baseUrl=https://folio-snapshot.dev.folio.org


#### Scenario 2. Local UI against the Snapshot backend

In the second scenario shows above, Stripes is running locally as Cypress is connecting to it -- but the local UI is connecting directly to remote FOLIO backend such that that provided by the public FOLIO Snapshot server. This is useful as an end-to-end integration test.

The Cypress configuration in `ui-courses` establishes http://localhost:3001/ as the default UI to connect to, so this need not be overridden with `--config` when running in this way. The Stripes CLI will listen on port 3000, but this can be changed using the `--port` argument, so running the two services in different terminals:

	terminal1$ stripes serve --port 3001
	terminal2$ cypress run

(It is helpful to use a port other than the default 3000 to avoid the possibility of a clash with another Stripes server already running on port 3000.)

If running both parts of this together -- for example, in batch mode as part of a CI job -- it is necessary to run the Stripes server in the background and ensure that the Stripes server has begun listening before the Cypress tests commence. The simplest way to do this is with [the `wait-on` utility](https://github.com/jeffbski/wait-on), which simply waits until a given URL can be successfully requested before exiting. It is also polite to shut down the Stripes service after the tests have completed. So:

	stripes serve --port 3001 & wait-on http://localhost:3001 && cypress run && kill $!


#### Scenario 3. Regenerating the mocked backend

This scenario is the same as the second, except that all traffic between the Stripes UI and the FOLIO backend is proxied via the Yakbak proxy so that tapes can be made of the requests and their corresponding responses.

To do this, it necessary to include quite a bit of configuration:
* The Yakbak proxy must be configured to contact the real backend, which is done by specifying the backend service's URL on the command-line.
* The Yakbak must listen on a specified port: this can be done using the `-p` command-line options, but the default of 3002 is often appropriate.
* The Stripes UI must be configured to use the Yakbak proxy as its FOLIO service, which can be done using its `--okapi` command-line argument.

It is also helpful to remove any existing tapes to ensure that we have a complete new set.

	terminal1$ stripes serve --port 3001 --okapi http://localhost:3002
	terminal2$ rm -rf tapes && yakbak-proxy -i https://folio-snapshot-okapi.dev.folio.org
	terminal3$ cypress run

(The other option here given to `yakbak-proxy` is `-i`, which tells it to ignore headers when identifying requests, so that when the tapes are replayed a given request is recognised provided only that its protocol, method and URL are the same as before.)

Note that there is rather a lot of plumbing here: Cypress must contact the Stripes UI on the correct port, the Stripes UI must contact the Yakbak proxy on the correct port, and the Yakbak proxy must contant the FOLIO backend on the correct URL. Some of this is obscured in the commands above because the Cypress configuration sets its connection URL appropriately, and because the Yakbak proxy's default port of 3002 is suitable.

When running in CI, both the Stripes server and the Yakbak proxy must be run in the background, and as before Cypress must not be started until the Stripes server is listening for connections. Now that there are two background processes to be killed, we need to do a bit more work in order to capture both of the process-IDs to kill:

	stripes serve --port 3001 --okapi http://localhost:3002 & pid1=$! &&
	rm -rf tapes &&
	yakbak-proxy -v -i https://folio-snapshot-okapi.dev.folio.org & pid2=$! &&
	wait-on http://localhost:3001 &&
	cypress run &&
	kill $pid1 $pid2

This is a slightly fearsome command (and it is a single shell command, even though here it is shown broken over six lines for clarity).


#### Scenario 4. Local UI against the mocked backend

This is the unit-testing scenario, which can only be run after tapes have been generated by scenario 3. In this, the Yakbak proxy is invoked (using the `--norecord` or `-n` command-line option) not to contact any back-end at all, but only to supply responses to requests for which it has tapes (returning 404 for any requests whose responses have not already been recorded).

Invocation is very similar to that of scenario 3, except that the `tapes` directory is of course not removed, and the `-n` command-line option is given to `yakbak-proxy`. Hence:

	stripes serve --port 3001 --okapi http://localhost:3002 & pid1=$! &&
	rm -rf tapes &&
	yakbak-proxy -v -i https://folio-snapshot-okapi.dev.folio.org & pid2=$! &&
	wait-on http://localhost:3001 &&
	cypress run &&
	kill $pid1 $pid2


#### Summary

The same set of software components, then, can be be used to run in several different ways. In the `ui-courses` package file, `scripts` entries are provided for each of these scenarios:

1. `yarn test-folio-snapshot` -- local tests against a remote UI
2. `yarn test-running-service` -- against a local UI with a remote backend
3, `yarn regenerate` -- against local UI via a taping proxy to a remote backend
4. `yarn test` -- against a local UI with a mocked backend provided by tapes

The last of these would normally be the command run by [Jenkins](https://www.jenkins.io/) in continuous integration -- see [below](#jenkins-integration) for details.

It _may_ be worth building a higher-level tool to invoke the various software components in the combinations required for these scenarios; but for now we go the more explicit route of invoking each component separately.



## Setting up Cypress



### Initialization and pruning

Cypress is easily added to a project's development dependencies using `yarn add --dev cypress`. It is run in interactive mode using `yarn cypress open` and in batch mode using `yarn cypress run`. The first time it is run in interactive mode, it sets up a directory structure:

![The directory hierarchy that Cypress creates for you](cypress-setup.png)

This structure is described in detail in [the Cypress documentation](https://docs.cypress.io/guides/core-concepts/writing-and-organizing-tests.html#Folder-Structure) but in very brief summary:
* Everything is kept in the `cypress` director: we do not use a `test` directory.
* `fixtures` contains static data files used for explicitly programmed mocks. We do not use these.
* `integration` contains the actual tests.
* `plugins` and `support` provides ways to extend Cypress's core functionality.
* `videos` and `screenshots` are generated when tests are run.

The `integration` directory comes populated with many example tests, which we don't need in our repositories. These should all be deleted. The unused `fixtures` directory can also be deleted.

Annoyingly, `fixtures` has a habit of reappearing (along with a single tiny fixture file) after being deleted, so it's best to add a `cypress/.gitignore` file preventing this from being accidentally added to the project's git archive.



### Jenkins integration

FOLIO's Jenkins configuration [has been extended](https://issues.folio.org/browse/FOLIO-2674) to preserve the generated videos and screeshots when Cypress runs in CI and the tests fail.

The result of this can be seen in Jenkins [build pages for failed tests](https://jenkins-aws.indexdata.com/job/folio-org/job/ui-courses/job/master/249//). These now include a "Build artifacts" section with links to any screenshots generated by the run, and to `cypress.tar.gz` which contains all the videos and/or screenshots generated by the run.

At present, the Jenkins configuration for a Stripes app that uses Cypress needs to be more complex that it ought to be in order for the tests to build and run correctly in CI. See [!!! WARNING: LARK'S VOMIT !!!](#-warning-larks-vomit-) for details.


### ESLint configuration

Style conventions for Cypress tests are rather different from those used for Stripes app code. As a result, we need to provide a different ESLint configuration, which is based on the `cypress` ESLint plugin, which knows about the global variables that Cypress injects in the test context, and which knows to expect no semi-colons at the ends of lines. So we need `cypress/.eslintrc` along these lines:

	{
	  "plugins": [
	    "cypress"
	  ],
	  "globals": {
	    "cy": "readonly",
	    "describe": "readonly",
	    "it": "readonly",
	    "expect": "readonly"
	  },
	  "rules": {
	    "semi": ["warn", "never"]
	  }
	}



### Measuring code coverage

To measure code coverage of Cypress-based tests is a three-stage process: it's necessary to instrument the code so that it generates coverage data, to get that data written to files, and to interpret the data in human-readable formats. Fortunately, all of these turn out to be fairly simple.


#### Instrumenting the code

[The Istanbul library](https://istanbul.js.org/) knows how to modify JavaScript code by inserting statements that increment counters when different regions of the code are reached, and there is [a Babel plugin](https://github.com/istanbuljs/babel-plugin-istanbul) that uses it to have this happen for any code that is already being translated by Babel -- as Stripes modules are. As of version 1.18.0, the Stripes CLI can run in a mode that invokes this plugin by specifying the `--coverage` option on the command line.

So when starting the Stripes server with the intention to generate coverage reports, use something like `stripes serve --coverage --port 3001`. In the absence of this setting, coverage data is not generated, so that the code runs more efficiently.

#### Writing coverage data to files

Cypress has a code-coverage plugin which knows how the read the statistics accumulated by Istanbul and write them out at the end of a test run. [The `@cypress/code-coverage` installation documentation](https://github.com/cypress-io/code-coverage#install) explains how to wire this into Cypress: you will need to make small changes to `cypress/support/index.js` and `cypress/plugins/index.js`.

##### !!! WARNING: LARK'S VOMIT !!!

For reasons we do not understand (see [UICR-96](https://issues.folio.org/browse/UICR-96)), the inclusion of `@cypress/code-coverage` as a dev-dependency in your package file is not sufficient for it to be fully installed by `yarn install`. As of [this writing](https://github.com/folio-org/ui-courses/commit/60687f945d4a06a2b4083d1d64c7a92e6567dab9), it is also necessary to run `yarn add --dev @cypress/code-coverage` _even though the dependency is already there_. Unless this additional step is performed, `stripes serve` will fail, saying:

	Error: Cannot find module '@babel/plugin-proposal-decorators' from '/Users/mike/ui-courses'

We tried to working around this bug with [a horrible kludge](https://github.com/folio-org/ui-courses/blob/8ae160cf0c08cd4eba720f542f02a6a318c0e519/package.json#L18) in which the package file had a `postinstall` script that immediately runs the `yarn add` command if the relevant package has not been put in place by `yarn install`. But this breaks the Stripes platform build in away to also do not fully understand (see [STRIPES-689](https://issues.folio.org/browse/STRIPES-689)) so that approach had to be backed out.

Instead, the present approach is to modify the Jenkins configuration so that instead of `runTests = true`, it invokes the tests using the `runScripts` option:

	buildNPM {
	  // ...
	  runTest = false
	  runScripts = [
	   ['postinstall-and-test':'']
	  ]
	}

And the package file defines a `postinstall-and-test` rule that invokes both a postinstall rule (named `fix` to avoid the STRIPES-689 problem) and the `test` rule:

	"postinstall-and-test": "yarn fix && yarn test"

All of this is unpleasant. Hopefully it can be ripped out once we get to the bottom of UICR-96, or at least find a less offensive workaround for it.

##### Failing to output coverage reports

Occaisionally, the `coverageReport` task will start failing for each suite. You'll see errors like this in the after-all hooks:

> CypressError: `cy.task('coverageReport')` failed with the following error:
> Cannot read property 'loc' of undefined

[These have been reported](https://github.com/cypress-io/code-coverage/issues/216) and should generally be fixed with the versions of `@cypress/code-coverage` that is being installed. However, they can still happen with version 3.9.2 when the `.nyc_output` directory exists at the start of a run. `rm`ing that directory has fixed it for me since then. I believe this directory hangs around if you liberally Ctrl+C tests while they're running and catch it in a bad spot.

#### Generating coverage reports

The Cypress code-coverage plugin leaves coverage information in various formats in the `coverage` directory. An pre-formatted HTML report is available starting from `coverage/lcov-report/index.html` and textual reports in various formats can be generated by the `nyc` command-line tool. For example, `nyc report --reporter=text-summary` generates a terse summary report like this:

```
$ nyc report --reporter=text-summary

=============================== Coverage summary ===============================
Statements   : 36.54% ( 228/624 )
Branches     : 27.57% ( 75/272 )
Functions    : 23.48% ( 54/230 )
Lines        : 37.77% ( 224/593 )
================================================================================
Done in 0.57s.
```




## Repeated requests when using YakBak



### The problem

Our intention is that the Yakbak proxy should be entirely transparent in use, so that any test that runs correctly without it will also run the same through it, and then against against the tapes that it makes.

However, this goal breaks down in some circumstances. Consider this test:

1. Search for all records
2. Verify that there are 5
3. Create a record
4. Search for all records
5. Verify that there are now 6

Since the HTTP request in step 4 is the same as that in step 2, the Yakbak proxy will return the real server's response once as its response to step 2, and then again as its response to step 4. As a result, there will be only five records in the response despite one having been added, and step 5 of the test will fail.



### Solutions


#### Write tests not to make the same request twice

The simplest solution to this is require that tests work around it. For example, in the scenario above, step 4 could search for all records but then sort them in a different order from the first time the request was made, so that a fresh back-end request is made and a fresh tape recorded.

This will work, but violates our desire that developers should be able to write tests without knowing or caring about the use of the proxy. It suffices as a backup plan, but it would be disappointing to require this.


#### Yakbak proxy inserts serial numbers into requests

A first attempt to preserve completely transparent use of the proxy is the addition of the `--sequence` (`-q`) option in [v1.2.0 of yakbak-proxy](https://github.com/folio-org/yakbak-proxy/tree/v1.2.0), which modifies the hashing function that Yakbak uses in determining when two requests are considered the same. (This function maps each incoming request to a digest which is uses as the filename for the tape that records the response.) When `--sequence` is specified on the command-line, each request is considered to contain an additional `X-sequence` header whose value is an integer that is incremented for each request.

This works so far as preserving separate responses to multiple identical requests is concerned. However it does not solve the problem of repeatable tests due to the non-deterministic order of network requests issued by Stripes. [The front page of the Course Reserves app](https://folio-snapshot.dev.folio.org/cr/courses?sort=name), for example, fetches not only the list of courses, but also lists of departments, course-types, terms and locations in order to populate the filters in the left-hand pane. All these requests are issues simultaneously in principle, and they may be activated in any order. If an attempt to run tests against tapes happens to use a different order from that in which the tapes were recorded, the requests will fail because they will be made with different sequence numbers from those used to generate the tapes.


#### Yakbak proxy inserts serial numbers into duplicate requests

A second attempt at a similar solution uses a smarter approach to assigning serial numbers. As of [yakbak-proxy v1.3.0](https://github.com/folio-org/yakbak-proxy/tree/v1.3.0), the hash function runs on the unmodified request, yielding the same base digest as without the `--sequence` option; however, a register is kept of how many times each request has been seen, and a request-specific counter is incremented each time a given request is seen. The returned digest is a combination of the base digest and the counter.

This approach ensures that each successive instance of the same request records its own response, but that the sequence numbering for any given request does not interfere with, and is not interfered with by, that of any other request.

Experimentally, this works correctly. However, even this does not suffice to allow the recorded tests to pass due to another problem: when a new record is created, stripes-connect generates a random UUID and includes it as the `id` in the POSTed record. When running against recorded tapes, the generated `id` is different from when they were recorded, so the new-record POST response is not found.


#### Excise `id` fields from POST requests

And so was born the `--exciseid` (`-x`) option (also in [v1.2.0 of yakbak-proxy](https://github.com/folio-org/yakbak-proxy/tree/v1.2.0)), When this is specified, the hash function modifies the body of POST requests (and _only_ POSTs, not PUTs), to remove the `id` field at the top level if it exists. This does not affect some POSTs -- e.g. the POST to `/bl-users/login` that is used to log in at the start of the session. But when the POST is used to create a new record, the specific ID chosen by stripes-connect is ignored for the purposes of creating the request's hash.

This seems to be enough for tests to record and pass correctly. But it multiples tapes, as pefectly innocent requests like "give me all the course-types so I can populate the filter" are repeated over and over, and record numerous identical tapes. As a result, [at the time of writing](https://github.com/folio-org/ui-courses/tree/30853a28362d1b33a681795fdc1ee737c5608bc8/tapes) there are 176 tapes, including some that are repeated nine times.


#### Re-use tapes until the next write event

If we think of the accumulating set of tapes, in response to a given set of requests, as a cache, then we can consider cache invalidation strategies. The strategy in use as described in [the earlier section](#yakbak-proxy-inserts-serial-numbers-into-requests) amounts to "consider the cache as always invalid" -- hence each new request generates a new response, resulting in the many dupliate responses. A very smart strategy would understand all the different possible write operations in the Course Reserves app, and knew which writes invalidate which parts of the cache. However, experience teaches us that "smart" in a cache-invalidation strategy is a synonym for "error-prone" -- cache invalidation is after one of the [Two Hard Problems in computer science](https://martinfowler.com/bliki/TwoHardThings.html). So instead we can use the simplest possible strategy: _any_ write (except the POST used for login) invalides _the entire cache_.

So the strategy here is:
* When request comes in for the first time, fetch it, cache the response and return in.
* When it comes in subsequrntly, return the cached response.
* When any POST, PUT or DELETE request other than a login is received, all cached responses are consider invalidated, a subsequent instance of a prevously cached request will result in its sequence number being incremented and a new back-end request being made.

This is implemented in v1.5.0 of yakbak-proxy, and has been demonstrated to work with the ui-courses tests. The number of tapes generated for the tests is down from 176 to 98. Also: since the new sequence-numbering strategy results in no duplicate tapes at all when handling only read requests, there is no need ever _not_ to run in `--sequence` mode. That mode is therefore now permanently on, and the command-line switch is removed.

We now have a proxying setup that should work with any test-suite.


#### Something cleverer that I've not thought of yet

The addition of sequence-numbering and (especially) the `--exciseid` option to yakbak-proxy is starting to feel like special pleading. Part of me feels there has to be a more elegant way to do this. Is there?

Seriously, folks, I am open to suggestions. [Let me know!](mailto:mike@indexdata.com)




## What next?

Some thoughts on where we might go next ...

As noted [above](#stripes-cli-to-provide-the-ui), when the Stripes CLI is used to run Nightmare tests, it furnishes a set of helper functions to the tests, which can be used for common actions like logging in, switching to a specific app, and logging out. As we gain experience in using Cypress with Stripes, we may find it helpful to provide a standard Cypress-for-Stripes library of similar functions that all UI apps using Cypress testing can make use of. If we do this, we may find it simplest to provide these as simple importable function, as Cypress commands (in `cypress/support/commands.js`) or as Cypress plugins (in `cypress/plugins`). More experience is needed before a decision can be made.

Also as noted [above](#summary), it may prove worthwhile to simplify invocation of the various testing scenarios by providing a higher-level script that starts all the nececesary software components with appropriate plumbing to connect each to the others. Again, only experience will show whether this would be worth the work of building it -- or even whether the addition of another layer would make the underlying reality _more_ difficult to understand.

For further learning:
* [_Best Practices_ in the Cypress documentation](https://docs.cypress.io/guides/references/best-practices.html)
* [The Cypress documentation more generally](https://docs.cypress.io/)
* [The example tests generated for a new Cypress installation](https://github.com/cypress-io/birdboard/tree/master/cypress/integration/examples) will probably illustrate numerous helpful techniques.
* [Numerous tutorial videos](https://www.youtube.com/c/Cypressio/videos)

Finally: feedback on this document is welcome! Email &lt;mike@indexdata.com&gt;




