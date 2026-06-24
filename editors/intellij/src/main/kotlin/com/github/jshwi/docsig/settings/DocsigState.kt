package com.github.jshwi.docsig.settings

import com.github.jshwi.docsig.ui.ClassCheckMode

internal data class DocsigState(
    var classCheckMode: ClassCheckMode = ClassCheckMode.NONE,
    var checkDunders: Boolean = false,
    var checkNested: Boolean = false,
    var checkOverridden: Boolean = false,
    var checkPropertyReturns: Boolean = false,
    var checkProtected: Boolean = false,
    var ignoreArgs: Boolean = false,
    var ignoreKwargs: Boolean = false,
    var ignoreNoParams: Boolean = false,
    var includeIgnored: Boolean = false,
    var exclude: String? = null,
    var excludes: List<String> = emptyList(),
    var disable: List<String> = emptyList(),
    var target: List<String> = emptyList(),
)
