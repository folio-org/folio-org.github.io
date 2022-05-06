---
layout: null
---

# Circulation Rules

<!-- How to generate the table of contents using https://github.com/folio-org/okapi/blob/master/doc/md2toc :
     ../../okapi/doc/md2toc -l 2 -h 3 circulationrules.md
-->

* [Line comment](#line-comment)
* [Allowed characters for names](#allowed-characters-for-names)
* [Policies](#policies)
* [Criteria type names](#criteria-type-names)
* [Criterium](#criterium)
    * ["!" and "all"](#-and-all)
* [Criteria](#criteria)
* [Multiple matching rules](#multiple-matching-rules)
    * [Criterium type priority](#criterium-type-priority)
    * [Rule specificity priority (number-of-criteria)](#rule-specificity-priority-number-of-criteria)
    * [Line number priority](#line-number-priority)
* [Fallback policy](#fallback-policy)
* [Single circulation rules file](#single-circulation-rules-file)
* [Loan Rules UX Design Video](#loan-rules-ux-design-video)

This document describes the circulation rules that actually have been implemented in
the mod-circulation back-end module.

The circulation rules engine calculates the loan policies based on the patron's
patron group and the item's material type, loan type, and location.

Example circulation rules file:

    fallback-policy: l no-circulation r no-request n no-notice o overdue i lost-item
    m book : l regular-loan r no-requests n no-notices o not-overdue i lost-item
    m newspaper: l reading-room r no-requests n no-notices o overdue i lost-item
    m streaming-subscription: l policy-s r no-requests n no-notices o overdue i lost-item
        g visitor undergrad: l in-house r no-requests n no-notices o overdue i lost-item

How does this short example work?

The `fallback-policy` line defines a default policy for each of the 4 policy types.
An `l` indicates a loan policy, `r` a request policy, `n` a notice policy, `o` 
an overdue fine policy' and `i` a lost item fee policy.

After `m` is the item's material type. Books can be loaned using the `regular-loan` loan policy,
newspapers can be loaned for the `reading-room` only.

Streaming subscriptions use the `policy-s` loan policy; however there are two
exceptions placed in the next line using indentation: For the user groups (`g`)
`visitor` and `undergrad` the streaming subscriptions can be loaned using
the `in-house` loan policy only.

The request and notice policies in this example are the same as the default, but
they work the same way as the loan policies.

## Line comment

A hash "#" or a slash "/" starts a line comment; all characters from that position
until the end of the line are ignored.

A hash starts a section title. Use the "filter rules" search box of the circulation
rules editor to temporarily show only the sections that contain the search box text
in their section title.

## Allowed characters for names

A name of a loan policy, a patron group, a material type, a loan type or a location
can contain only these characters: a-z, A-Z, 0-9 and minus "-".

## Policies

A list of policies is appended to a criteria line after a colon, with each policy's
type indicated by an `l`, `r`, `n`, `o`, `i`.
They can be in any order, but must have one of each type.
If the line matches then those policies are applied.

The list of policies (including the colon) is optional.

## Criteria type names

These are the single letter criteria type names:

* `g` the patron's patron group (like staff, undergrad, visitor)
* `m` the item's material type (like book, newspaper)
* `t` the item's loan type (like rare, course-reserve)
* `a` the item's institution (location)
* `b` the item's campus (location)
* `c` the item's library (location)
* `s` the item's location (location)

`a`, `b`, `c` and `s` build a location hierarchy.

## Criterium

A criterium consists of a single letter criterium type and a name selection of that type.

If it has one or more names of that type it matches any patron group listed. If the patron
group is `visitor` or `undergrad` this rule matches:

```
g visitor undergrad: l loan-a r request-a n notice-a o overdue-a i lost-item-a
```

### "!" and "all"

If the criterium has one or more negated names (name with exclamation mark prepended) then it matches
any patron group that is not listed, for example this rule matches `staff` but neither `visitor` nor `undergrad`:

```
g !visitor !undergrad: l loan-b r request-b n notice-b o overdue-b i lost-item-b
```

Use the keyword `all` for the name selection to match all patron groups, for example
```
g all: l loan-a r request-a n notice-b o overdue-b i lost-item-b
```
This is needed to alter the rule priority, see below.

## Criteria

Criteria can be combined in two ways:

Concatenating them into one line using `+` as separator like

```
g visitor + t rare: l loan-policy-a r request-policy-a n notice-policy-a o overdue i lost-item
```

matches if the patron group is `visitor` and the loan type is `rare`.

To avoid long lines one may replace the `+` by a line break followed by an indentation like

```
g visitor
    t rare: l loan-policy-a r request-policy-a n notice-policy-a o overdue i lost-item
```

The second line matches when the criteria of the first and the second line matches.

Indentation allows for a nested hierarchy:

```
g staff: l loan-policy-a r request-policy-a n notice-policy-a o overdue-a i lost-item-a
g visitor: l loan-policy-b r request-policy-b n notice-policy-b o overdue-b i lost-item-b
    m book: l loan-policy-c r request-policy-c n notice-policy-c o overdue-c i lost-item-c
        t rare: l loan-policy-d r request-policy-d n notice-policy-d o overdue-d i lost-item-d
        t course-reserve: l loan-policy-e r request-policy-e n notice-policy-e o overdue-e i lost-item-e
            s law-department: l loan-policy-f r request-policy-f n notice-policy-f o overdue-f i lost-item-f
            s math-department: l loan-policy-g r request-policy-g n notice-policy-g o overdue-g i lost-item-g
    s new-acquisition: l loan-policy-h r request-policy-h n notice-policy-h o overdue-h i lost-item-h
```

A current line matches if the current line's criteria matches and for
each smaller indentation level the last line before the current line
has matching criteria.

The hierarchy shown before contains these rules:

Patron group staff (indentation level 0) gives loan-policy-a, request-policy-a,
 notice-policy-a, overdue-a and lost-item-a.
(This is true for any material type, any loan type and any shelving location.)

Patron group visitor (indentation level 0) and shelving location new-acquisition
(indentation level 1) gives loan-policy-h, request-policy-h, notice-policy-h, overdue-h
and i lost-item-h.
(This is true for any loan type and any material type.)

Patron group visitor (indentation level 0) and material type book (indentation level 1)
and loan type course-reserve (indentation level 2) and shelving location math-department
(indentation level 3) gives loan-policy-g, request-policy-g, notice-policy-g, overdue-g
and i lost-item-g.

Patron group visitor (indentation level 0) and material type book (indentation level 1)
and loan type course-reserve (indentation level 2) and shelving location law-department
(indentation level 3) gives loan-policy-f, request-policy-f, notice-policy-f, overdue-f
and i lost-item-f.

Patron group visitor (indentation level 0) and material type book (indentation level 1)
and loan type course-reserve (indentation level 2) and any shelving location different from
math-department and law-department gives loan-policy-e, request-policy-e, notice-policy-e, overdue-e
and i lost-item-e.

Patron group visitor (indentation level 0) and material type book (indentation level 1)
and loan type rare (indentation level 2) gives loan-policy-d, request-policy-d, notice-policy-d,
overdue-d and i lost-item-d.
(This is true for any shelving location.)

Patron group visitor (indentation level 0) and material type book (indentation level 1)
and any loan type different from rare and course-reserve gives loan-policy-c, request-policy-c, notice-policy-c,
overdue-c and i lost-item-c. (This is true for any shelving location.)

Patron group visitor (indentation level 0) and any material type different from book and globe
gives loan-policy-b, request-policy-b, notice-policy-b, overdue-b and i lost-item-b. (This is true for any loan type
and any shelving location.)

## Multiple matching rules

If more than one rule matches then the rule with the highest priority is used. The priority line
lists the priority regulations in the order they are checked until only a single matching rule
remains. The priority line must be before the first rule line.

The priority line may contain one, two or three priority regulations. The last regulation must be
a line regulation: either `first-line` or `last-line`.

Before the line regulation there can be zero, one or two of the other regulations:
`criterium (…)`, `number-of-criteria`

The `criterium (…)` regulation contains the seven criterium types in any order, for example
`criterium (t, s, c, b, a, m, g)`.

This is an example for a complete priority line:

`priority: number-of-criteria, criterium (t, s, c, b, a, m, g), last-line`

For compatibility with former versions a priority line may contain only the seven criterium types:

`priority: t, s, c, b, a, m, g`

This is the same as

`priority: criterium(t, s, c, b, a, m, g), number-of-criteria, last-line`

### Criterium type priority

The criterium priority lists the criterium types in decreasing priority, for example
`criterium(t, s, c, b, a, m, g)`. For each rule take the criterium type with
the highest priority. Now compare the matching rules using that criterium type.
The rules with the highest priority win.

Example a:

```
priority: criterium(t, s, c, b, a, m, g), number-of-criteria, last-line
fallback-policy: l no-circulation r no-request n no-notice o overdue i lost-item
g visitor: l loan-policy-a r request-policy-a n notice-policy-a o overdue i lost-item
t rare: l loan-policy-c r request-policy-c n notice-policy-c o overdue i lost-item
m book: l loan-policy-e r request-policy-e n notice-policy-e o overdue i lost-item
```

A loan for patron group `visitor` and loan type `rare` and material type `book` matches
all three rules. However, the rule with loan-policy-c, request-policy-c, and notice-policy-c
is the only rule with the highest criterium type `t` and wins.

Example b:

```
priority: criterium(t, s, c, b, a, m, g), number-of-criteria, last-line
fallback-policy: l no-circulation r no-request n no-notice o overdue i lost-item
g visitor:l loan-policy-a r request-policy-a n notice-policy-a o overdue i lost-item
    t rare: l loan-policy-b r request-policy-b n notice-policy-b o overdue i lost-item
t rare: l loan-policy-c r request-policy-c n notice-policy-c o overdue i lost-item
    m book: l loan-policy-d r request-policy-d n notice-policy-d o overdue i lost-item
m book: l loan-policy-e r request-policy-e n notice-policy-e o overdue i lost-item
```

We assign priority numbers to the criterium types:
t=7, a=6, b=5, c=4, s=3, m=2, g=1.

A loan for material type `book` and loan type `rare` and patron group `visitor` matches
all five rules and each rule has this priority:

```
priority: criterium(t, s, c, b, a, m, g), number-of-criteria, last-line
fallback-policy: l no-circulation r no-request n no-notice o overdue i lost-item
g visitor: max(g=1)=1: l loan-policy-a r request-policy-a n notice-policy-a o overdue o overdue i lost-item
g visitor + t rare: max(g=1, t=7)=7: l loan-policy-b r request-policy-b n notice-policy-b o overdue i lost-item
t rare: max(t=7)=7: l loan-policy-c r request-policy-c n notice-policy-c o overdue i lost-item
t rare + m book: max(t=7, m=2)=7: l loan-policy-d r request-policy-d n notice-policy-d o overdue i lost-item
m book: max(m=2)=2: l loan-policy-e r request-policy-e n notice-policy-e o overdue i lost-item
```

The three rules with policy-b, policy-c and policy-d have the highest criterium type priority of 7.
For the tie we need to continue with "2. Rule specificity priority".

The rule with loan-policy-e has a lower criterium type priority of 2,
the rule with loan-policy-a has the lowest criterium type priority of 1.

### Rule specificity priority (number-of-criteria)

Specificity is the number of criterium types.  Higher number of criterium types has higher priority.
Any number of location criterium types (`a`, `b`, `c`, `s`) count as one.

```
priority: criterium(t, s, c, b, a, m, g), number-of-criteria, last-line
fallback-policy: l no-circulation r no-request n no-notice o overdue i lost-item
g visitor + t rare: l loan-policy-b r request-policy-b n notice-policy-b o overdue-b i lost-item-b
t rare: l loan-policy-c r request-policy-c n notice-policy-c o overdue-c i lost-item-c
t rare + m book: l loan-policy-d r request-policy-d n notice-policy-d o overdue-d i lost-item-d
```

A loan for material type `book` and loan type `rare` and patron group `visitor` matches
all three rules. The criterium type priority is the same (`t`). The line with loan-policy-b has a
specificity of 2 because it has two criteria (`g` and `t`). The line with loan-policy-c has a
specificity of 1 because it has only one criterium (`t`). The line loan-policy-d has a
specificity of 2 because it has two criteria (`t` and `m`).

The rules with loan-policy-b and loan-policy-d have the highest specificity priority of 2.

Use the `all` keyword to match all names of that criterium type. That way the
criterium type is used for both the Criterium type priority and the Rule specificity
priority but without restricting to some names. Example:

```
priority: criterium(t, s, c, b, a, m, g), number-of-criteria, last-line
fallback-policy: l no-circulation r no-request n no-notice o overdue i lost-item
g visitor + t rare: l loan-policy-b r request-policy-b n notice-policy-b o overdue i lost-item
t rare: l loan-policy-c r request-policy-c n notice-policy-c o overdue i lost-item
t rare + m book: l loan-policy-d r request-policy-d n notice-policy-d o overdue i lost-item
g all + t all + s course-reserve: l loan-policy-e r request-policy-e n notice-policy-e o overdue i lost-item
```

The loan-policy-e rule has priority over the other three rules because it has a `t` criterium
and uses three criteria.

### Line number priority

For the line number priority the order of the rules is relevant. For `last-line` the
last matching rule (the rule with the highest line number) is taken, for `first-line` the
first matching rule (the rule with the lowest line number) is taken.

```
priority: criterium(t, s, c, b, a, m, g), number-of-criteria, last-line
fallback-policy: l no-circulation r no-request n no-notice o overdue
g visitor + t rare: l loan-policy-b r request-policy-b n notice-policy-b o overdue
t rare + m book: l loan-policy-d r request-policy-d n notice-policy-d o overdue
```

A loan for material type `book` and loan type `rare` and patron group `visitor` matches
both lines. The criterium type priority is the same (`t`). They both have two criteria.
The line with loanpolicy-d has higher priority because it is last (it has a higher line number).

## Fallback policy

There always must be a line with a set of three fallback policies, one for
each type like `fallback-policy: l no-circulation r no-request n no-notice o overdue i lost-item`.
It must be after the priority line and before the first rule.

For `priority: first-line` it must be after the last rule.

## Single circulation rules file

For one tenant there is only a single circulation rules file.

It must have a single priority line and a single fallback-policy line.

## Loan Rules UX Design Video

The video from May 2017 explains the user experience (UX) design of the loan rules.
The general principles still apply but note that some aspects have changed since then
or haven't been implemented yet.

[https://discuss.folio.org/t/loan-rules-ux-iteration-4/834](https://discuss.folio.org/t/loan-rules-ux-iteration-4/834)

* 00:08 What is a loan policy?
* 00:26 What does a loan policy contain?
* 00:37 Can loan policies be combined?
* 01:00 How are loan policies applied?
* 01:09 Loan rules
* 01:19 Loan rule criteria
* 01:46 Criteria shorthand
* 02:04 Combining criteria - Plus (+) and Colon (:)
* 02:28 Using multiple criteria values
* 02:56 Nesting criteria
* 03:36 Modifiers - exclamation mark (!)
* 04:00 Logic - Rule Priority
* 05:32 Logic: 1. Priority of criteria in a rule
* 06:43 Logic: 2. Specificity of a rule 
* 06:57 Logic: 3. Line number of a rule
* 07:32 Special selectors: The "all" selector
* 08:33 Example of loan rules setup
* 09:14 Demo: fallback-policy
* 09:50 Demo: Section headlines (#)
* 10:11 Demo: priority
* 10:42 Demo: Sections, sub-sections, comments (/)
* 11:12 Demo: Simple rules
* 11:46 Demo: Nesting rules
* 12:51 Demo: Exception - exclamation mark (!)
* 13:32 Demo: Multiple names in a criterium
* 13:58 Demo: Exceptions - "all" selector
* 16:36 Demo: Auto-suggest
* 19:34 Demo: Syntax error warnings
* 20:16 Demo: Testing outcome of loan rules
* 22:38 Demo: Editing policies in context
* 23:34 Demo: Searching and filtering loan rules
