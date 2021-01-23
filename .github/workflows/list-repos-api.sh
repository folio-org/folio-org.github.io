INPUT_PN="${GITHUB_WORKSPACE}/_data/repos.json"
echo "isSpringway:"
jq -r '.repos[] | if .isSpringway then .name else empty end' < ${INPUT_PN}
