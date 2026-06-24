#!/bin/bash
JAVA_HOME="$(/usr/libexec/java_home -v 21)" sh gradlew "${@}"
