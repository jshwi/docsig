package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.messages.DocsigBundle

internal enum class ClassCheckMode(
    internal val label: String,
    internal val flag: String?,
) {
    NONE(
        DocsigBundle.message(
            "settings.options.class-checking-mode-none",
        ),
        null,
    ),
    CLASS(
        DocsigBundle.message(
            "settings.options.class-checking-mode-check-class",
        ),
        "--check-class",
    ),
    CLASS_CONSTRUCTOR(
        DocsigBundle.message(
            "settings.options.class-checking-mode-check-class-constructor",
        ),
        "--check-class-constructor",
    ),
}
