#!/usr/bin/env bash
set -euo pipefail

# The Java project targets release 25
export JAVA_HOME=/usr/lib/jvm/java-25-openjdk-amd64
export PATH="$JAVA_HOME/bin:$PATH"

(cd Java   && mvn -B -DskipTests clean package)
(cd Go     && go build ./...)
(cd CSharp && dotnet clean && dotnet build --no-incremental -p:UseSharedCompilation=false)
