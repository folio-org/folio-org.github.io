INPUT_PN="${GITHUB_WORKSPACE}/_data/repos.json"
echo "# ----------"
echo "# isSpringway:"
jq -r '.repos[] | if .isSpringway then .name else empty end' < ${INPUT_PN}
echo "# ----------"
echo "# hintOas:"
jq -r '.repos[] | if .hintOas then .name else empty end' < ${INPUT_PN}
echo "# ----------"
echo "# isRmb:"
jq -r '.repos[] | if .isRmb then .name else empty end' < ${INPUT_PN}
echo "# ----------"
echo "# hasRaml:"
jq -r '.repos[] | if .ramlDirName then .name else empty end' < ${INPUT_PN}
