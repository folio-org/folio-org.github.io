---
layout: null
---

# Building and running `mod-ldp` for development

<!-- md2toc -l 2 running-in-dev.md -->
* [Building the module](#building-the-module)
* [Finding the LDP datasbase](#finding-the-ldp-datasbase)
* [Testing the connection to the LDP database](#testing-the-connection-to-the-ldp-database)
* [Running the module](#running-the-module)
* [Initializing the module](#initializing-the-module)
* [Plumbing](#plumbing)
* [Daily update procedure](#daily-update-procedure)


## Building the module

Use `mvn install`. If it fails with errors like this:
> [ERROR] ColumnObjControllerTest » IllegalState Could not find a valid Docker environment
It's probably because your user doesn't have permission to use Docker. You can "fix" this by running as root, but better is to add your user to the `docker` group:
```
sudo usermod -a -G docker mike
```
Then you can log out and in again to have it take effect, or use `newgrp docker` to explicitly tell your present shell that you have the new group. `mvn install` should now work.


## Finding the LDP datasbase

The name of the host that contains the folio-snapshot LDP database unfortunately changes on each rebuild. It is always for the form `ec2-NUMBER-NUMBER-NUMBER-NUMBER.compute-1.amazonaws.com` and can be found as follows:

* Go to https://dev.folio.org/guides/automation/#reference-environments
* Choose "folio-snapshot" (or "folio-snapshot-2" if you prefer) in the left-hand ToC.
* Follow the "See Jenkins job: folio-snapshot" link.
* Go to the most recent build in the "Build History" left-hand panel.
* Select "View as plain text" in the left-hand panel.
* Do browser "Find in page" to look for: `ec2-`

Shortcut: go straight to [the console text from the latest folio-snapshot build](https://jenkins-aws.indexdata.com/job/FOLIO_Reference_Builds/job/folio-snapshot/lastBuild/consoleText)


## Testing the connection to the LDP database

Once you have found the current hostname, you can test it with the command-line Postgres client:
```
psql -h ec2-34-224-78-21.compute-1.amazonaws.com -U ldp ldp
Password: diku_ldp9367
```
Try this query:
```
select * from public.user_users limit 1;
```


## Running the module

Once you have found the current hostname, you can start mod-ldp as follows:
```
env DB_HOST=ec2-34-224-78-21.compute-1.amazonaws.com DB_PORT=5432 DB_DATABASE=ldp DB_USERNAME=ldp DB_PASSWORD=diku_ldp9367 java -jar target/mod-ldp-1.0.3-SNAPSHOT.jar --server.port=12370
```

You can test that it's running correctly with something like:
```
curl -H 'X-Okapi-Tenant: diku' localhost:12370//ldp/config/dbinfo
```
This will not actually work, as the necessary configuration entries are not in place until the module has been inserted into Okapi hand had its tenant intialization interface invoked, but you should at least get an informative response like "No such key dbinfo".


## Initializing the module

You will need to insert database information for mod-ldp to run usefully:
```
curl -X PUT -H 'X-Okapi-Tenant: diku' -H 'Content-type: application/json' localhost:12370/ldp/config/dbinfo -d '{ "tenant": "diku", "key": "dbinfo", "value": "{ \"url\": \"jdbc:postgresql://ec2-34-224-78-21.compute-1.amazonaws.com:5432/ldp\", \"user\": \"ldp\", \"pass\": \"diku_ldp9367\" }" }'
```
You can verify that this has worked using:
```
curl -H 'X-Okapi-Tenant: diku' localhost:12370/ldp/config/dbinfo
```
Now you should be able to have mod-ldp fetch the list of tables, using:
```
curl -H 'X-Okapi-Tenant: diku' localhost:12370/ldp/db/tables
```

## Plumbing

In the invocation above, we told mod-ldp to listen on port 12370, using `--server.port=12370`. (Other FOLIO modules use 
`-Dport=1234`,
`-Dhttp.port=1234`
or
`-Dserver.port=1234` -- there is no standard.)

Now we need to make this available to the Okapi of a running FOLIO system. The simplest way is to run a `folio/testing-backend` Vagrant box, and make a reverse tunnel into that box so Okapi can see the port:
```
$ vagrant ssh -- -R 12370:localhost:12370
guest$ # Leave the ssh session open
```

Now all you need to do is tell Okapi about the locally running module. In another shell: POST the module descriptor, POST a discovery descriptor that tells Okapi where to find the already-running module, and enable the module for a tenant:
```
curl -w '\n' http://localhost:9130/_/proxy/modules -d @target/ModuleDescriptor.json
curl -w '\n' http://localhost:9130/_/discovery/modules -d '{ "srvcId": "mod-ldp-1.0.3-SNAPSHOT", "instId": "127.0.0.1-12370", "url" : "http://127.0.0.1:12370" }'
curl -w '\n' http://localhost:9130/_/proxy/tenants/diku/modules -d '{ "id": "mod-ldp-1.0.3-SNAPSHOT" }'
```

(`srvcId` in the second command, and `id` in the third, must both match the `id` specified in the module descriptor; `url` in the second command must point to the running instance that you have provided a tunnel for; `instId` can be anything unique.)

Now you can run Stripes against the VM's Okapi on http://localhost:9130 and the side-loaded mod-ldp will be available, as you can verify by going to the **Software versions** at (for example) http://localhost:3000/settings/about and searching within the page for `mod-harvester-admin`.


## Daily update procedure

Because the folio-snapshot backend that provides the LDP database gets rebuilt every day, and gets allocated a different hostname each time, it's necessary to go through a tedious update process at the beginning of each day's development:

* Restart mod-ldp, as described [above](#running-the-module), using the new hostname as the value of the `DB_HOST` environment variable.
* Go to http://localhost:3000/settings/ldp/dbconfig and set **Database URL** to the new value in the format `jdbc:postgresql://ec2-3-85-12-188.compute-1.amazonaws.com/ldp` and reset **Username** and **Password** to their correct values.


