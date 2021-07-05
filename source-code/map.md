---
layout: page
title: Source-code map
permalink: /source-code/map/
menuInclude: yes
menuTopTitle: Source
menuSubTitle: Source-code map
menuSubIndex: 2
---

## Introduction

List of FOLIO modules hosted at GitHub, with links to some related documentation.
Also refer to the [Source-code overview](/source-code/).

{% assign urlGithub = "https://github.com" %}
{% assign urlApiBase = "https://dev.folio.org/reference/api" %}
{% assign urlApiBaseLocal = "/reference/api" %}
{% assign countTotal = site.data.repos.repos | size %}
{% assign alpha = "A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z" | split:"," %}
{% assign numPerSection = 15 %}

Last [gathered](#further-information) date:
{{ site.data.repos.metadata.generatedDateTime | date_to_long_string }}
({{ countTotal }} repositories).
See [usage notes](#usage-notes) below.

{% for group in site.data.repos-group %}
  {%- assign groupId = group[0] -%}
  {%- assign groupStem = group[1].stem -%}
  {%- assign repos = site.data.repos.repos | where:"repoType",groupId -%}
  {%- assign countSection = repos | size -%}
  <h2 id="{{ groupId }}"> {{ group[1].title }} </h2>
  <p> {{ countSection }} repositories. </p>
  {%- assign numSubSections = countSection | divided_by:numPerSection -%}
  {%- assign remainder = countSection | modulo:numPerSection -%}
  {%- if remainder > 0 and countSection > numPerSection -%}
    {%- assign numSubSections = numSubSections | plus:1 -%}
  {%- endif -%}
  {%- if numSubSections == 1 -%}
    {%- assign numSubSections = 0 -%}
  {%- endif -%}
  {%- comment -%} Build the arrays for subsection headings {%- endcomment -%}
  {%- assign headingsString = "" -%}
  {%- assign headingIdsString = "" -%}
  {%- if numSubSections > 0 -%}
    {%- assign numAlphasPerSubSection = 26 | divided_by:numSubSections -%}
    {%- assign alphaNum = 0 -%}
    {%- for i in (1..numSubSections) -%}
      {%- assign alphaBegin = alpha[alphaNum] -%}
      {%- assign alphaNum = alphaNum | plus:numAlphasPerSubSection -%}
      {%- if alphaNum > 25 -%}
        {%- assign alphaNum = 25 -%}
      {%- endif -%}
      {%- assign alphaEnd = alpha[alphaNum] -%}
      {%- assign heading = "" | append:alphaBegin | append:"-" | append:alphaEnd | append:"," -%}
      {%- assign headingsString = headingsString | append: heading -%}
      {%- assign headingId = groupStem | append:alphaBegin | append:"-" | append:alphaEnd | downcase | append:"," -%}
      {%- assign headingIdsString = headingIdsString | append: headingId -%}
      {%- assign alphaNum = alphaNum | plus:1 -%}
    {%- endfor -%}
    {%- assign headings = headingsString | split:"," -%}
    {%- assign headingIds = headingIdsString | split:"," -%}
    {%- comment -%} Output the first sub-section heading. {%- endcomment -%}
    {%- assign subSectionNum = 0 -%}
    <h3 id="{{ headingIds[subSectionNum] }}"> {{ headings[subSectionNum] }} </h3>
  {%- endif -%}
  {%- for repo in repos -%}
    {%- assign repoName = repo.name -%}
    {%- assign metadata = site.data.repos-metadata[repoName] -%}
    {%- if numSubSections > 0 -%}
      {%- comment -%} If repoName begins with char of next sub-section, then output sub-section heading. {%- endcomment -%}
      {%- assign sectionChar = headingIds[subSectionNum] | slice:-1,1 | upcase -%}
      {%- assign repoNameAlpha = repoName | remove_first:groupStem -%}
      {%- assign repoNameChar = repoNameAlpha | slice:0 | upcase -%}
      {%- assign charNum = 0 -%}
      {%- for char in alpha -%}
        {%- if char == sectionChar -%}
          {%- assign sectionCharNum = charNum -%}
        {%- endif -%}
        {%- if char == repoNameChar -%}
          {%- assign repoNameCharNum = charNum -%}
        {%- endif -%}
        {%- assign charNum = charNum | plus:1 -%}
      {%- endfor -%}
      {%- if repoNameCharNum > sectionCharNum -%}
        {%- assign subSectionNum = subSectionNum | plus:1 -%}
        <h3 id="{{ headingIds[subSectionNum] }}"> {{ headings[subSectionNum] }} </h3>
      {%- endif -%}
    {%- endif -%}
    {%- if numSubSections > 0 -%}
      <h4 id="{{ repoName }}"> {{ repoName }} </h4>
    {%- else -%}
      <h3 id="{{ repoName }}"> {{ repoName }} </h3>
    {%- endif -%}
    {%- if repo.description -%}
      {%- capture desc -%}{{ repo.description }}{%- endcapture -%}
    {%- else -%}
      {%- capture desc -%}[Not provided]{%- endcapture -%}
    {%- endif -%}
    <p> Description: {{ desc }} </p>
    {%- if metadata.furtherDescription -%}
        <p> {{ metadata.furtherDescription }} </p>
    {%- endif -%}
    {%- if repo.snippetIntro -%}
      {%- capture intro -%}{{ repo.snippetIntro }}{%- endcapture -%}
      <div> {{ intro }} </div>
    {%- endif -%}
    {%- capture urlRepo -%}{{ urlGithub }}/{{ repo.org }}/{{ repoName }}{%- endcapture -%}
    <p> GitHub README: <a href="{{ urlRepo }}">{{ urlRepo }}</a> </p>
    {%- if repo.docDirName -%}
      {%- capture urlGhDocs -%}{{ urlGithub }}/{{ repo.org }}/{{ repoName }}/tree/master/{{ repo.docDirName }}{%- endcapture -%}
      <p> GitHub other documentation: <a href="{{ urlGhDocs }}">{{ urlGhDocs }}</a> </p>
    {%- endif -%}
    {%- if metadata -%}
      {%- if metadata.urlUserTips -%}
        <p> App tips: <a href="{{ metadata.urlUserTips }}">{{ metadata.urlUserTips }}</a> </p>
      {%- endif -%}
      {%- if metadata.urlAppSettings -%}
        <p> App settings: <a href="{{ metadata.urlAppSettings }}">{{ metadata.urlAppSettings }}</a> </p>
      {%- endif -%}
      {%- if metadata.urlsOther -%}
        <p> Other documentation:<br/>
        {%- for urlDoc in metadata.urlsOther -%}
          <a href="{{ urlDoc }}">{{ urlDoc }}</a><br/>
        {%- endfor -%}
        </p>
      {%- endif -%}
    {%- endif -%}
    {%- if repo.hasDbSchema -%}
      {%- capture urlDbSchema -%}{{ urlGithub }}/{{ repo.org }}/{{ repoName }}/{{ repo.hasDbSchema }}{%- endcapture -%}
      <p> GitHub DB schema: <a href="{{ urlDbSchema }}">{{ urlDbSchema }}</a> </p>
    {%- endif -%}
    {%- if repo.ramlDirName -%}
      {%- capture urlGhRaml -%}{{ urlGithub }}/{{ repo.org }}/{{ repoName }}/tree/master/{{ repo.ramlDirName }}{%- endcapture -%}
      <p> GitHub RAMLs directory: <a href="{{ urlGhRaml }}">{{ urlGhRaml }}</a> </p>
      {%- capture urlApi -%}{{ urlApiBase }}/#{{ repoName }}{%- endcapture -%}
      {%- capture urlApiLocal -%}{{ urlApiBaseLocal }}/#{{ repoName }}{%- endcapture -%}
      <p> API documentation: <a href="{{ urlApiLocal }}">{{ urlApi }}</a> </p>
    {%- endif -%}
    {%- if repo.hintOas -%}
      {%- capture urlApi -%}{{ urlApiBase }}/#{{ repoName }}{%- endcapture -%}
      {%- capture urlApiLocal -%}{{ urlApiBaseLocal }}/#{{ repoName }}{%- endcapture -%}
      <p> API documentation: <a href="{{ urlApiLocal }}">{{ urlApi }}</a> </p>
    {%- endif -%}
  {%- endfor -%}
{%- endfor -%}

## Usage notes

### Mainline branch information

The links are to current main branches of each repository, thereby reflecting the current state of development.

So for specific module releases, the GitHub URLs need to be be adjusted to the relevant release "tag".
Use the "Branches/Tags" menu at the left-hand of its breadcrumb trail.

### DB schema

If a "DB schema" link is shown, then use this to assist construction of
[CQL search queries](/faqs/explain-cql/).

It shows which tables are available, the database indexes and their types (e.g. fullTextIndex, uniqueIndex, etc.) along with details of those indexes (e.g. caseSensitive, removeAccents, etc.).

## Further information

Refer to tips for module developers to [increase visibility of module documentation](/guides/visibility-module-docs/).

[Explanation](/guides/visibility-module-docs/#assemble-source-code-map) about how this map is assembled and maintained.

<div class="folio-spacer-content"></div>

