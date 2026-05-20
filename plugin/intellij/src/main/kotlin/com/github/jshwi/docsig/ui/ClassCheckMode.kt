/**
 * Enumeration for the class check mode.
 */
package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.messages.DocsigBundle

/**
 * Maps class-check UI choices to optional CLI flags.
 *
 * @property label Combo box caption shown to the user.
 * @property flag CLI flag when present, or null when omitted.
 */
internal enum class ClassCheckMode(val label: String, val flag: String?) {
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
