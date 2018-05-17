# Notes for maintaining the theme

* Currently using theme [classic-jekyll-theme](https://github.com/Balancingrock/classic-jekyll-theme).
See documentation at https://balancingrock.github.io/classic-jekyll-theme/

* Keep up-to-date with new versions of the theme. Update `_config.yml` and set "remote_theme" property to the new version. Restart the local server and test.

* If we need an intermediate bug-fix version, then set that "remote_theme" property to the relevant commit ID.

* If there is a need to override any more files, then copy them from the currently-used version theme. Commit the initial raw copy, then modify, so that we know what changes we have made.

* Endeavour to limit our need to over-ride files by reporting issues and feature suggestions upstream.

* If ever we feel a need to choose a new theme, then see some [guidelines](guide-theme.md).

