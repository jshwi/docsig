#!/bin/bash
_JAVA_HOME="$(/usr/libexec/java_home -v 21)"
export JAVA_HOME="${_JAVA_HOME}"
sh gradlew detekt "${@}"
