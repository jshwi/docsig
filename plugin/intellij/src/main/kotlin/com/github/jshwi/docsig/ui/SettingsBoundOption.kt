package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.settings.DocsigSettings

internal sealed interface SettingsBoundOption<T> : Option {
    val get: (DocsigSettings) -> T

    val set: (DocsigSettings, T) -> Unit

    // cli flag is fixed for every stored value
    interface WithFixedFlag<T> : SettingsBoundOption<T> {
        val flag: String
    }

    // cli flag depends on the stored enum-like value
    interface WithValueFlag<T : Any> : SettingsBoundOption<T> {
        val flagOf: (T) -> String?
    }
}
