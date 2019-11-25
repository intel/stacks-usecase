#!/bin/bash

set -e
set -u
set -o pipefail

PAGE=20
URL="https://api.github.com/repos/clearlinux/distribution/issues"
DLDIR="/workdir/data/raw"
AUTH=""

BANNER="Get github issues data, if no <issues_url> provided, issues from ClearLinux github will be downloaded."
USAGE="$(basename "$0" ) [-h] [-u <issues_url>] [-d <outputpath>] [-t <token>]
where:
  -h | --help help
  -u | --url <issues_url> to download github issues
  -d | --dir <directory> to download github issues
  -t | --token <git token> to download data"

run() {
  echo "=============================================================="
  printf "$(date) -- %s"
  printf "%s\n" "$@"
  echo "=============================================================="
}

# install required bundles
install_reqs () {
  swupd bundle-add jq curl
  pip install jupyter
  echo "Installed jq, curl and jupyter"
  echo "Run jupyter  notebook --ip=0.0.0.0 --port=8888 --allow-root to initiate a jupyter notebook"
}

# curl github issues; if you hit the api ratelimit, use authenticated requests
get_data () {
  install_reqs
  while [[ $PAGE -gt 0 ]]
  do
    URL+="?per_page=100&page="
    #curl -H "Authorization: token $TOKEN" "$URL$PAGE" > $DLDIR/issues-$((100 * PAGE)).json
    curl -H "$AUTH" "$URL$PAGE" > $DLDIR/issues-$((100 * PAGE)).json
    PAGE=$((PAGE - 1))
  done
  jq --slurp "." $DLDIR/issue*.json >> $DLDIR/all_issues.json
}

while [[ $# -gt 0 ]]
do
key="$1"
case $key in
    -h | --help ) run && echo "$USAGE"
      exit
      ;;
    -u|--url)
    URL=${2-default}
    shift # move argument
    shift # move value
    ;;
    -d|--dir)
    DLDIR=${2-default}
    shift # move argument
    shift # move value
    ;;
    -t|--token)
    AUTH="Authorization: token $2"
    shift #move argument
    shift #move value
    ;;
    *) echo "invalid flag, try -h for help" >&2
      exit 1
    ;;
esac
done

run && echo "$BANNER"

begin="$(date +%s)"
run "get issues data from ::  ${URL}" && get_data
finish="$(date +%s)"
runtime=$(((finish-begin)/60))
run "Done in :  $runtime minute(s)"
exit
