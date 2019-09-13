#!/bin/bash

set -e
set -u
set -o pipefail

URL="${2:-https://api.github.com/repos/clearlinux/distribution/issues}"
PAGE=20 
OPTION="${1:-}"

BANNER="Get github issues data, if no <issues_url> provided, issues from ClearLinux github will be downloaded."
USAGE="$(basename "$0") [-h] [-u <issues_url>]
where:
  -h | --help help
  -u | --url <issues_url> to download github issues"

run() {
  echo "=============================================================="
  printf "$(date) -- %s"
  printf "%s\n" "$@"
  echo "=============================================================="
}

# install required bundles
install_reqs () {
  swupd bundle-add jq
}

# curl github issues; if you hit the api ratelimit, use authenticated requests
get_data () {
  install_reqs
  while [[ $PAGE -gt 0 ]]
  do
    URL+="?per_page=100&page="
    curl "$URL$PAGE" > /workdir/data/raw/issues-$((100 * PAGE)).json
    (( PAGE -= 1 ))
  done
  jq --slurp "." /workdir/data/raw/issue*.json >> /workdir/data/raw/all_issues.json
}

while :
do
    case "$OPTION" in
    -h | --help ) run && echo "$USAGE"
      exit
      ;;
    -u | --url ) begin="$(date +%s)"
       run "get issues data from ::  ${URL}" && get_data
       finish="$(date +%s)"
       runtime=$(((finish-begin)/60))
       run "Done in :  $runtime minute(s)"
      exit
      ;;
    *) echo "invalid flag, try -h for help" >&2
      exit 1
      ;;
    esac
done
run && echo "$BANNER"
