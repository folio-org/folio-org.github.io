---
layout: page
title: Source code index
permalink: /source-code/xref/
menuInclude: yes
menuTopTitle: Source
menuSubTitle: Source code index
menuSubIndex: 2
---

## Introduction

List of modules and links to some related documentation.

Last [gathered](#further-information) date:
{{ site.data.repos.metadata.generatedDateTime | date_to_long_string }}

{% assign urlGithub = "https://github.com/folio-org" %}
{% assign urlApiBase = "https://dev.folio.org/reference/api" %}

{% for group in site.data.repos-group %}
  {% assign groupId = group[0] %}
  {% assign repos = site.data.repos.repos | where:"repoType",groupId %}
  <h2 id="{{ groupId }}"> {{ group[1].title }} </h2>
  {% for repo in repos %}
    {%- assign repoName = repo.name -%}
    {%- assign metadata = site.data.repos-metadata[repoName] -%}
    <h3 id="{{ repoName }}"> {{ repoName }} </h3>
    {%- if repo.description -%}
      {% capture desc %}{{ repo.description }}{% endcapture %}
    {% else %}
      {% capture desc %}[Not provided]{% endcapture %}
    {%- endif -%}
    <p> Description: {{ desc }} </p>
    {%- if metadata.furtherDescription -%}
        <p> {{ metadata.furtherDescription }} </p>
    {%- endif -%}
    {%- capture urlRepo -%}{{ urlGithub }}/{{ repoName }}{%- endcapture -%}
    <p> GitHub README: <a href="{{ urlRepo }}">{{ urlRepo }}</a> </p>
    {%- if repo.docDirName -%}
      {% capture urlGhDocs %}{{ urlGithub }}/{{ repoName }}/tree/master/{{ repo.docDirName }}{%- endcapture -%}
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
      <p> API documentation: <a href="{{ urlApi }}">{{ urlApi }}</a> </p>
    {%- endif -%}
  {% endfor %}
{% endfor %}

## Further information

Explanation about how the index is assembled and maintained:

Details of each repository that is hosted at FOLIO GitHub are gathered automatically.
This is done occasionally as a FOLIO DevOps infrastructure
[job](https://github.com/folio-org-priv/folio-infrastructure/tree/master/verify-repo-config).
It is not yet automated, but is initiated manually.
The resulting JSON file is committed as the
[\_data/repos.json](https://github.com/folio-org/folio-org.github.io/tree/master/_data/repos.json) data file.

The data file
[\_data/repos-metadata.yml](https://github.com/folio-org/folio-org.github.io/tree/master/_data/repos-metadata.yml)
contains additional metadata about some specific repositories.
Please send pull-requests to add documentation links for your repository.
The YAML structure is explained in the head of that file.
The tool "[yq](https://github.com/kislyuk/yq)" is useful for verifying YAML files (e.g. do `yq '.' repos-metadata.yml`).

Behind the scenes of this page
[source-code/xref.md](https://raw.githubusercontent.com/folio-org/folio-org.github.io/master/source-code/xref.md)
the Jekyll Liquid program assembles and presents this page.

