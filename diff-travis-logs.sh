#!/usr/bin/env bash
# Usage diff-travis-logs.sh https://travis-ci.org/python-pillow/docker-images/jobs/361337420 https://travis-ci.org/python-pillow/docker-images/jobs/368529735

echo $1
echo $2

job1=$(basename $1)
job2=$(basename $2)

echo $job1
echo $job2

url1="https://api.travis-ci.org/v3/job/${job1}/log.txt"
url2="https://api.travis-ci.org/v3/job/${job2}/log.txt"

echo $url1
echo $url2
echo "bc $url1 $url2"

/usr/local/bin/bcompare $url1 $url2
