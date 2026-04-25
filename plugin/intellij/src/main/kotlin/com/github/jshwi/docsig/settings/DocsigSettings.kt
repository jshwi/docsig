/**
 * Persistent plugin state: CLI path and docsig check flags.
 */
package com.github.jshwi.docsig.settings

import com.github.jshwi.docsig.model.DocsigState
import com.intellij.openapi.components.PersistentStateComponent
import com.intellij.openapi.components.Service
import com.intellij.openapi.components.State
import com.intellij.openapi.components.Storage
import com.intellij.openapi.project.Project

/** Application-level XML state for the docsig integration. */
@Service(Service.Level.PROJECT)
@State(name = "DocsigSettings", storages = [Storage("docsig.xml")])
class DocsigSettings : PersistentStateComponent<DocsigState> {
    private var state = DocsigState()

    /**
     * Returns the object serialized into docsig.xml on commit.
     *
     * @return Current in-memory state shared with the settings UI.
     */
    override fun getState(): DocsigState = state

    /**
     * Replaces cached values after XML deserialization from disk.
     *
     * @param state Newly loaded state from persistent storage.
     */
    override fun loadState(state: DocsigState) {
        this.state = state
    }

    companion object {
        /**
         * Resolves the application-level service instance.
         *
         * @return Singleton settings backed by component storage.
         */
        fun getInstance(project: Project): DocsigSettings =
            project.getService(DocsigSettings::class.java)
    }
}
