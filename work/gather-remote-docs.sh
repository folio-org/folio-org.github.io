#!/usr/bin/env bash

# Requirements:
#   httpie
#   jq

output_base_dir="${GH_F_WEB}/_remote"
input_fn="${GH_F_WEB}/_data/remote-docs.json"
#input_fn="${GH_F_WEB}/_data/remote-docs-temp.json"
delay=20
urls=$(jq -r '.[]' ${input_fn})

function gather () {
  url=$1
  doc=${url##*/}
  str1=${url#*folio-org/}
  repo=${str1%%/*}
  str2=${url#*/master/}
  path=${str2%/*}
  if [ "$path" == "$doc" ]; then
    path=""
  fi
  echo "$repo | $path | $doc"
  output_dir="${output_base_dir}/${repo}/${path}"
  mkdir -p ${output_dir}
  output_file="${output_dir}/${doc}"
  http --output $temp_file_2 ${url}
  # concatenate and remove Liquid-like syntax
  cat $temp_file_1 $temp_file_2 \
    | sed 's/{{//g' | sed 's/}}//g' \
    > $output_file
}

temp_file_1="/tmp/remote1"
temp_file_2="/tmp/remote2"
cat << EOH > "${temp_file_1}"
---
layout: null
---

EOH

for u in ${urls}; do
  gather $u
  sleep $delay
done

rm -f $temp_file_1 $temp_file_2

