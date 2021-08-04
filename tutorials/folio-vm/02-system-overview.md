---
layout: page
title: VM system overview
permalink: /tutorials/folio-vm/02-system-overview/
menuInclude: yes
menuLink: yes
menuTopTitle: Tutorials
---

This lesson provides a brief overview of the system.

## System setup

Some detail (about Okapi, Docker, and Postgres) is provided at [FOLIO system setup on Vagrant boxes](https://github.com/folio-org/folio-ansible/blob/master/doc/index.md#folio-system-setup-on-vagrant-boxes).

The sample data for each installed module is already loaded.

## Viewing logfiles

After [Launch the guest](../01-create-workspace#launch-the-guest), do:

```
vagrant ssh
```

### Okapi log

Get the container name of the Okapi module:

```
docker ps | grep okapi
```

View this module's logs:

```
docker logs --follow <container_name>
```

### Stripes log

Stripes is deployed as a Docker container with a dedicated name. So do:

```
docker logs stripes_stripes_1
```

Or to follow the logfile:

```
docker logs stripes_stripes_1 --follow
```

### Backend module logs

Each backend module is deployed by Okapi as a Docker container.

Get the container name of the module to be inspected, e.g.

```
docker ps | grep inventory
```

View this module's logs:

```
docker logs <container_name>
```

---
Next lesson: [Interact with the FOLIO VM](../03-interact/)

