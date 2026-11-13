#!/usr/bin/env bash
# build-all.sh: build every compiled component so CodeQL can trace it
set -euo pipefail

# Java (example: Maven; use ./gradlew build for Gradle)
mvn -B -DskipTests package

# Go
go build ./...

# C# (example: .NET)
dotnet build
