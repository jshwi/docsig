package com.github.jshwi.docsig.models

import com.fasterxml.jackson.annotation.JsonIgnoreProperties

// tolerant reader: the docsig cli attaches extra keys to each json
// diagnostic (a per-entry "path"), so unknown fields must be ignored or
// jackson throws UnrecognizedPropertyException and every run is dropped
@JsonIgnoreProperties(ignoreUnknown = true)
internal data class Issue(
    internal val line: Int?,
    internal val message: String,
    internal val exit: Int,
)
