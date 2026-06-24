package com.github.jshwi.docsig.models

internal data class Issue(
    internal val line: Int?,
    internal val message: String,
    internal val exit: Int,
)
