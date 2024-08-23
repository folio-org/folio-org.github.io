---
layout: null
---

# How to add new settings to the mod-settings module

Mike Taylor, Index Data. mike@indexdata.com


<!-- md2toc -l 2 HOWTO.md -->
* [Introduction](#introduction)
* [What to do](#what-to-do)
    * [1. Define one or more scopes](#1-define-one-or-more-scopes)
    * [2. Define relevant permissions for the scopes](#2-define-relevant-permissions-for-the-scopes)
    * [3. Assign necessary permissions to users](#3-assign-necessary-permissions-to-users)
* [Summary](#summary)



## Introduction

When FOLIO client code (whether a UI module or a back-end module) wants to store settings, the simplest and most secure way to do this is in mod-settings. To do so requires establishing one or more scopes and creating some permissions. This document explains what is required of the client module.



## What to do


### 1. Define one or more scopes

Settings in the mod-settings module belong to a scope, which is named by a short string. Within a given scope, each setting has a unique key, which is also a short string.

There is no conept of defining a machine-readable object that is a scope -- for example, in a module descriptor. Instead, a scope exists when there are settings within that scope and permissions that provide access to them.

In order to avoid multiple modules defining scopes with the same names, it is conventional for scope names to begin with the name of the module that is defining them. For example, the `mod-inventory` module might define a scope called mod-inventory` which contains all the settings used by the Inventory app.

When all of a module's settings are within the same scope, it follows that a user who has permissions to access to any one setting has permission to access them all. It is almost always better for a module to define several scopes, using the module name as the first of multiple `.`-separated facets. For example, the `mod-inventory` module might define scopes `mod-inventory.admin` and `mod-inventory.prefs`, For adminstrative settings and preferences respectively, and assign permissions to allow only a few inventory users access to the administrative settings, but allow a broader group access to the pereferences.

In the example above, the `mod-inventory.admin` scope might contain settings with keys like `max-loans` and `max-holds` (which should only be set by administrators); and `mod-inventory.prefs` might contain settings with keys like `search-default-language` and `search-default-resource-type`.

Nothing prevents one module from naming a scope that properly belongs to another -- for example, `mod-inventory` naming the scope `mod-users.prefs`. Nothing, that is, but common sense and basic decency. **Do not do this.**

One a scope has been defined, it is laborious and error-prone to change its name, as it appears in permissions, in code, and in extant settings objects. So it is worth taking some time to think about a future-proof name for a scope when starting to use it. In particular, naming scopes _only_ after the modules that define them (e.g. the `mod-inventory` scope) is likely to lead to problems when it subsequently becomes necessary for the same module to define a second  scope. So it is generally best to use a multi-facet scope name even when it is (initially) the only scope defined by a module.


### 2. Define relevant permissions for the scopes

A scope's only manifestation in a module descriptor is in the permissions that allow user to access keys in that scope. Typically two permissions are defined: 

`mod-settings.global.read.SCOPE` allows a user to read settings in the named scope, and `mod-settings.global.write.SCOPE` allows a user to write settings in the named scope. For example, `mod-settings.global.read.mod-inventory.prefs` allows a user to read settings from the scope `mod-inventory.prefs`. The settings module itself enforces this requirement.

Note that, although these permissions are in the `mod-settings` namespace, they are defined by the client module (e.g. in the present example `mod-inventory`). This is a unique situation in FOLIO, required by the need for `mod-settings` to determine the name of the permission to check when all it knows is the scope and the operation (read or write).

(There are two more pairs of permissions that can be defined for a scope: read and write for "user", meaning a user-specific value of a setting; and for "self", meaning the current user's own user-specific value. These permissions are named `mod-settings.user.read.SCOPE`/`mod-settings.user.read.SCOPE` and `mod-settings.self.read.SCOPE`/`mod-settings.self.read.SCOPE`. These have not yet been used in real code, but are available when needed.)


### 3. Assign necessary permissions to users

Obviously, users must be assigned whatever permissions defined by the client module are needed for the settings access they are intended to have: in the example above, including `mod-settings.global.write.mod-inventory.prefs` to set preferences, or `mod-settings.global.read.mod-inventory.admin` to read the administrative settings.

In addition to these, every user must be assigned basic permissions to use the settings modules. These include:

* `mod-settings.entries.item.get` to fetch a known setting
* `mod-settings.entries.item.post` to create a new setting
* `mod-settings.entries.item.put` to update an existing setting
* `mod-settings.entries.item.delete` to delete an existing setting
* `mod-settings.entries.collection.get` to search available settings

(These are of course defined by `mod-settings` and do not need to be defined by the client module.)

In practice, fetching a known setting is rarely used, as the opaque ID is not usually known. Instead, users must be granted the `mod-settings.entries.collection.get` permission, which governs the `/settings/entries` entry point.This is generally used with a `query` parameter such as `scope=mod-inventory.admin and key=max-loans`.


## Summary

If we want a module `mod-foo` to support a domain `mod-foo.bar`, then:

* It will be necessary for this module to define the permissions `mod-settings.global.read` and `mod-settings.global.write`.
* Users who are to read settings in this scope will need the `mod-settings.global.read.mod-foo.bar` permission as well as `mod-settings.entries.collection.get` (and they may as well have `mod-settings.entries.item.get` too).
* Users who are to write settings in this scope will need the `mod-settings.global.write.mod-foo.bar` permission as well as `mod-settings.entries.item.post`, `mod-settings.entries.item.put` and `mod-settings.entries.item.delete`.


