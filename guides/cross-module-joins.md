---
layout: page
title: Conduct cross-module joins via their APIs
permalink: /guides/cross-module-joins/
menuInclude: no
menuTopTitle: Guides
---

Joins between different modules cannot be created at the SQL level, because you don't even know what other modules exist in the system, and you have no way of discovering what their tables and fields are even if you do know.
All modules must be called via their [APIs](/reference/api/).

