# Guidelines for theme

Currently Jekyll is used to generate the site.
These are some notes to assist with deciding whether an improved theme meets our needs.

* Currently using "github-pages". So follow whatever constraints that that imposes.
(This could change in the future.)

* Currently using "minima" theme.

* If current theme cannot meet our needs for improved navigation (perhaps by adding some supporting tools for navigation, and tweaking the current theme) then find a better theme.

* Easy maintenance for us. Currently we over-ride a couple of templates and add a minimum of extra CSS.

* Compact and uncluttered. Well-utilised screen space for technical documentation.

* Ability to add more items to the top navigation bar.
(Currently cannot fit many more. Perhaps shorten some names.)

* Ability for a second row navigation bar at the top.
The top row would link to other important FOLIO spaces (i.e. enable cohesion across the group of sites).
The second row would link to important dev.f.o spaces.

* Ability for non-obtrusive side-bar navigation, e.g. sliding toggleable.
Configurable content, e.g. from a data file.

* Ability for multiple columns in a section when required.

* Utilise the footer to link to standard important areas.

* Ensure that theme source development is not stale, e.g. responds to pull requests.

* Meets responsive web design.
Consider browser window width 1024px (this is the "medium" [used](https://github.com/folio-org/stripes-components/blob/master/lib/variables.css) by the FOLIO application, and seems to be around the GitHub width too) and consider hand-held devices.
