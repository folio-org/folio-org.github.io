---
layout: null
---


* Start Date: 2022-03-29
* RFC PR: 
  * Preliminary Review: https://github.com/folio-org/rfcs/pull/3
  * Draft Review : https://github.com/folio-org/rfcs/pull/3
  * Public Review : https://github.com/folio-org/rfcs/pull/3
  * Final Review : https://github.com/folio-org/rfcs/pull/3
* FOLIO Issue:
* Current Status: :no_entry_sign: ACCEPTED :no_entry_sign:
* Submitter : Radhakrishnan Gopalakrishnan (rgopalakrishnan@ebsco.com)
* Co-Submitter(s) : Zak Burke (zburke@ebsco.com)
* Sub Group : 
  * Marc Johnson (marc.johnson@k-int.com)
  * Julian Ladisch (julian.ladisch@gbv.de)
  * Peter Murray (peter@indexdata.com)
  * Tod Olson (tod@uchicago.edu)

# Localizing API (Backend) Messages

## Summary
The purpose of this RFC is to define an approach that allows API developer to provide
messages in the API response depending on the language preference set in the request. 


## Motivation

- Help users understand the information coming from the application backend using a language they understand better
- To allow FOLIO platform to be used by users across the world 
- To create a tremendous opportunity for growth that we can never could have achieved within just one country.
- To Promote consistency and make it easier for tools and translators when handling translation files

### Terminology
* Base Language - Language on which all other translations are based.
* Message Key - Refers to the string that is used in place of a hardcoded message in the code
* Message Value - Refers to the string that is fetched using a message key lookup for a given locale
* Translation file - Contains Message key and values for a given locale
* Static (design / compile time) Messages - Message values that are defined during development and do not vary by deployment environment
* Dynamic Messages - Messages stored in the database that requires translation. A.k.a Runtime messages
* Message Format - Refers to the standard used for formatting the message values in the translation file

### In Scope Requirements/Use cases
- Return localized messages based on the value passed in the accept-language header
- Handle static messages with placeholder(s)

### Out of Scope Requirements/Use cases
- Naming convention to be used for keys
- Process for managing (decoupled from lokalise.com) translations
- Returning formatted (HTML/Markdown) messages
- Usage of [soft hyphen](https://wiki.folio.org/display/I18N/How+To+translate+FOLIO#HowTotranslateFOLIO-Softhyphentobreakwords) to break messages
- Support customization per tenant
- Process  for [back porting](https://wiki.folio.org/display/I18N/Backport) API/Backend messages similar to what we have for the front end 
- Support for [controlled vocabulary](https://issues.folio.org/browse/UXPROD-3148) (runtime data/data coming from DB tables. E.g. Patron Groups for tenants)

## Detailed Explanation/Design
#### API Protocol
* **accept-language** header value MUST be in languageCode-regionCode format, -regionCode is an optional part of the value.
  * **languageCode** is a two-letter language code from [ISO 639-1](https://en.wikipedia.org/wiki/ISO_639-1) (2002) or a three-letter code from [ISO 639-2](https://en.wikipedia.org/wiki/ISO_639-2) (1998), [ISO 639-3](https://en.wikipedia.org/wiki/ISO_639-3) (2007) or ISO 639-5 (2008), or registered through the BCP 47 process and composed of five to eight letters;
  * **regionCode** is a two-letter country code from [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) (written in upper case), or a three-digit code from [UN M.49](https://en.wikipedia.org/wiki/UN_M49) for geographical regions.
* A module MUST return messages in the language specified in the HTTP "Accept-language" request header
  (see IETF RFC 7231 section 5.3.5).  If the requested language is not available, a module
  MUST return the message in the en language.
* When handling messages with placeholders, replace the placeholders with the actual value on the server side before
    sending it back to the client
* Reliance on the lang query string parameter is DEPRECATED and MUST be updated to use the "Accept-language" header
  at the earliest possible development sprint.

#### Translation files
* Translation file format will depend on the language that is used to develop the module
  * Java, Groovy - properties
  * JavaScript, nodejs - json
  * Any other language - Please contact Technical Council for further guidance
* Translation files MUST be placed under translations/\<Backend Module Name\>, relative to the root of the repo.
  The files are being stored under a folder named after the module/repo to avoid having conflicts when using the same
  message key across multiple backend modules. 
* Translation file name MUST be named [language code]-[country code].[extension] 
  The language code and country code MUST adhere to  [IETF Language Tag standard](https://en.wikipedia.org/wiki/IETF_language_tag)  
  and `extension` is the appropriate extension for the file format.
#### Translations
* Translation message keys MUST be a valid string 
* Message values in the translation file MUST be formatted according to the [ICU](https://icu.unicode.org)  standard
#### Language/Runtime
* Module MUST use language/framework specific recommended best practices for loading translation at runtime



## Rationale and Alternatives
<span style="color:green">**_Following 4 options were considered. All options except Option 4 involves stripes in some manner.
Coupling the API backend to a specific front end framework limits the usage of FOLIO API to
only clients that are built using Stripes. As a result, we are recommending that we go with Option 4._**
</span>.

### Option 1
Distribute them over the existing front-end modules:

ui-checkin with translation key ui-checkin.mod-circulation.itemNotFound
ui-requests with translation key ui-requests.mod-circulation.patronHasItemOnLoad

*Pros*
- Uses existing front-end modules

*Cons*
- Cannot disable a front-end module for a tenant if it hosts a mod-circulation translation key that is needed by another enabled front-end module.
- Not all originating messages can be mapped to a frontend module 

### Option 2a
For each back-end module with translation keys create a dedicated front-end module with language files:

For example create ui-mod-circulation module, and use translation keys

ui-mod-circulation.itemNotFound
ui-mod-circulation.patronHasItemOnLoad

*Pros*
- Any front-end module that uses mod-circulation can require ui-mod-circulation to load the translation files.
- All mod-circulation translation strings go into a single module.
*Cons*
- Additional overhead in managing more ui modules
- Not all originating messages can be mapped to a frontend module

### Option 2b
For each back-end interface with translation keys create a dedicated front-end module with language files:

For example create i18n-circulation module, and use translation keys

i18n-circulation.itemNotFound
i18n-circulation.patronHasItemOnLoad

*Pros*
- Any front-end module that uses the circulation API can require i18n-circulation to load the translation files.
- All circulation translation strings go into a single module.
*Cons*
- Additional overhead in managing more ui modules
- Not all originating messages can be mapped to a frontend module

### Option 3
The back-end module hosts the language files.

mod-circulation creates a translations/mod-circulation/ directory.

Stripes fetches the translation files from the back-end module and can process them the same way as translation files from frone-end modules.

*Pros*
- Software and language files are in the same repository. Options 1 and 2 require to add the message string to some other repository using a second pull request.

*Cons*
- Is this technically feasible? How can Stripes fetch languages files from a non-Stripes module?

### Option 4:
When calling the back-end pass the required locale. The back-end maintains the translations files, replaces the placeholders and puts the final string into the "message" property. A lang query parameter that many FOLIO API interfaces already have or an "accept-language" header line might be used.

*Pros*
- Java code and translation files live in the same repository. No work for the front-end.
- This is a well known pattern in the Java community

*Cons*
- We are essentially dealing with translations in multiple locations. Frontend and Backend

## Risks and Drawbacks

- Translation files are spread over multiple repositories


## Unresolved Questions

