export default {
  extends: ["stylelint-config-standard", "stylelint-config-standard-scss"],
  rules: {
    "at-rule-empty-line-before": null,
    "block-no-empty": true,
    "color-hex-length": null,
    "comment-empty-line-before": null,
    "declaration-block-single-line-max-declarations": 2,
    "rule-empty-line-before": null,
    "selector-class-pattern": null,
    "scss/at-if-closing-brace-newline-after": null,
    "scss/at-if-closing-brace-space-after": null,
    "scss/at-rule-conditional-no-parentheses": null,
    "scss/comment-no-empty": null,
    "scss/dollar-variable-empty-line-before": null,
    "scss/dollar-variable-colon-space-after": null,
    "scss/dollar-variable-pattern": ['^(-?[a-z][a-z0-9]*)(-[a-zA-Z0-9]+)*$',],
    "scss/double-slash-comment-empty-line-before": null,
    "scss/double-slash-comment-whitespace-inside": null,
    "scss/operator-no-unspaced": null,
  }
};
