---
layout: page
title: FTP CI test server
permalink: /guides/ftp-ci-server/
menuInclude: no
menuTopTitle: Guides
---

## Introduction

There is a File Transfer Protocol (FTP) server available for use with application testing and the CI
[reference environments](/guides/automation/#reference-environments).

* Domain name: `ftp.ci.folio.org`
* Username: `folio` Password: `Ffx29%pu`

The data store is short-lived and there is automatic [cleanup](#cleanup) after a certain age.

Both [sftp](#sftp) clients and plain [ftp](#ftp) clients can be utilised.

There is only one user (`folio`).

The data is stored in that user space at the `/ftp/files/` directory.
Within that space, files and sub-directories can be created and deleted as needed.
There are no restrictions.

## sftp

Background information:
[SSH File Transfer Protocol](https://en.wikipedia.org/wiki/SSH_File_Transfer_Protocol)
(also known as "Secure File Transfer Protocol" or SFTP).

Command-line client example:

```
$ sftp folio@ftp.ci.folio.org
... password
sftp> get test-get.txt
sftp> bye
```

`curl` client examples:

```
# Download:
curl -k "sftp://ftp.ci.folio.org/ftp/files/test-get.txt" \
  --user "folio:########" -o "get.txt"

# Upload and new sub-directory:
curl -k "sftp://ftp.ci.folio.org/ftp/files/newdir/" --ftp-create-dirs \
  --user "folio:########" -T "test-put.txt"
```

## ftp

Background information:
[File Transfer Protocol](https://en.wikipedia.org/wiki/File_Transfer_Protocol)
(also known as FTP).

The "Anonymous FTP access" is not enabled by this service.

Command-line client example:

```
$ ftp ftp.ci.folio.org
... password
ftp> cd files
ftp> get test-get.txt
ftp> bye
```

`curl` client examples:

```
# Download:
curl -k "ftp://ftp.ci.folio.org/files/test-get.txt" \
  --user "folio:########" -o "get.txt"

# Upload and new sub-directory:
curl -k "ftp://ftp.ci.folio.org/files/newdir/" --ftp-create-dirs \
  --user "folio:########" -T "test-put.txt"
```

## Cleanup

A cron job will automatically remove old files.

The current setting is after 7 days.

Contact FOLIO DevOps if there is a need to vary that in special circumstances.

Of course the command-line clients and curl can be used to tidy, when files and directories are no longer needed.

