#!/bin/sh

set -x

cat ../sbt-versions.txt | \
	while read sbt_version; do 
		echo "downloading sbt-${sbt_version}..."
		wget \
			"https://github.com/sbt/sbt/releases/download/v${sbt_version}/sbt-${sbt_version}.tgz" 
			#- \
			#>"sbt-${sbt_version}.tgz"
	done
