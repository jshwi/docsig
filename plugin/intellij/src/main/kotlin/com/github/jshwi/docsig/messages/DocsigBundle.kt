/**
 * Load messages from the messages.DocsigBundle resource bundle.
 */
package com.github.jshwi.docsig.messages

import com.intellij.DynamicBundle
import org.jetbrains.annotations.Nls
import org.jetbrains.annotations.NonNls
import org.jetbrains.annotations.PropertyKey

/**
 * Loads messages from the messages bundle.
 */
internal object DocsigBundle {
    @NonNls
    private const val BUNDLE = "messages.DocsigBundle"

    private val instance = DynamicBundle(DocsigBundle::class.java, BUNDLE)

    /**
     * Retrieve a message from the resource bundle.
     *
     * @param key The key of the message to retrieve.
     * @param params The parameters to format the message with.
     * @return The formatted message.
     */
    fun message(
        @PropertyKey(resourceBundle = BUNDLE) key: String,
        vararg params: Any,
    ): @Nls String = instance.getMessage(key, *params)
}
