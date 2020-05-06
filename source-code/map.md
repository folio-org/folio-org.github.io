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

List of FOLIO modules hosted at the [folio-org GitHub organization](https://github.com/folio-org), with links to some related documentation.
Also refer to the [Source-code overiew](/source-code/).

{% assign urlGithub = "https://github.com/folio-org" %}
{% assign urlApiBase = "https://dev.folio.org/reference/api" %}
{% assign urlApiBaseLocal = "/reference/api" %}
{% assign countTotal = site.data.repos.repos | size %}
{% assign alpha = "A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z" | split:"," %}
{% assign numPerSection = 15 %}

Last [gathered](#further-information) date:
{{ site.data.repos.metadata.generatedDateTime | date_to_long_string }}
({{ countTotal }} repositories).

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
    {%- capture urlRepo -%}{{ urlGithub }}/{{ repoName }}{%- endcapture -%}
    <p> GitHub README: <a href="{{ urlRepo }}">{{ urlRepo }}</a> </p>
    {%- if repo.docDirName -%}
      {%- capture urlGhDocs -%}{{ urlGithub }}/{{ repoName }}/tree/master/{{ repo.docDirName }}{%- endcapture -%}
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
    {%- if repo.ramlDirName -%}
      {%- capture urlGhRaml -%}{{ urlGithub }}/{{ repoName }}/tree/master/{{ repo.ramlDirName }}{%- endcapture -%}
      <p> GitHub RAMLs directory: <a href="{{ urlGhRaml }}">{{ urlGhRaml }}</a> </p>
      {%- capture urlApi -%}{{ urlApiBase }}/#{{ repoName }}{%- endcapture -%}
      {%- capture urlApiLocal -%}{{ urlApiBaseLocal }}/#{{ repoName }}{%- endcapture -%}
      <p> API documentation: <a href="{{ urlApiLocal }}">{{ urlApi }}</a> </p>
    {%- endif -%}
  {%- endfor -%}
{%- endfor -%}

## Further information

Explanation about how the index is assembled and maintained:

Details of each repository that is hosted at FOLIO GitHub are gathered automatically
(including information such as type of repository; does it have a "docs" directory; if backend, then does it have a "ramls" directory).
This collection is done occasionally as a FOLIO DevOps infrastructure
[job](https://github.com/folio-org-priv/folio-infrastructure/tree/master/verify-repo-config).
It is not yet automated, but is initiated manually.
The resulting JSON file is committed as the
[\_data/repos.json](https://github.com/folio-org/folio-org.github.io/tree/master/_data/repos.json) data file.

The data file
[\_data/repos-metadata.yml](https://github.com/folio-org/folio-org.github.io/tree/master/_data/repos-metadata.yml)
contains additional metadata about some specific repositories.
This information includes extra documentation links, beyond that gathered in the above-mentioned repos.json file (note that such links are intended as starting points, not to list every piece of documentation here).
Please send pull-requests to add documentation links for your repository.
The YAML structure is explained in the head of that file.
The tool "[yq](https://github.com/kislyuk/yq)" is useful for verifying YAML files (e.g. do `yq '.' repos-metadata.yml`).

Behind the scenes of this page
[source-code/map.md](https://raw.githubusercontent.com/folio-org/folio-org.github.io/master/source-code/map.md)
the Jekyll Liquid program assembles and presents this page.

