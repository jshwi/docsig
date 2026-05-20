/**
 * Enumeration for the class check mode.
 */
package com.github.jshwi.docsig.ui

/**
 * Maps class-check UI choices to optional CLI flags.
 *
 * @property label Combo box caption shown to the user.
 * @property flag CLI flag when present, or null when omitted.
 */
internal enum class ClassCheckMode(val label: String, val flag: String?) {
    NONE(
        "settings.options.class-checking-mode-none",
        null,
    ),
    CLASS(
        "settings.options.class-checking-mode-check-class",
        "--check-class",
    ),
    CLASS_CONSTRUCTOR(
        "settings.options.class-checking-mode-check-class-constructor",
        "--check-class-constructor",
    ),
}
