package com.github.jshwi.docsig.messages

import com.intellij.DynamicBundle
import org.jetbrains.annotations.Nls
import org.jetbrains.annotations.NonNls
import org.jetbrains.annotations.PropertyKey

internal object DocsigBundle {
    @NonNls
    private const val BUNDLE = "messages.DocsigBundle"

    private val instance = DynamicBundle(DocsigBundle::class.java, BUNDLE)

    internal fun message(
        @PropertyKey(resourceBundle = BUNDLE) key: String,
        vararg args: Any,
    ): @Nls String = instance.getMessage(key, *args)
}
