package com.github.jshwi.docsig.settings

import com.intellij.openapi.components.PersistentStateComponent
import com.intellij.openapi.components.Service
import com.intellij.openapi.components.State
import com.intellij.openapi.components.Storage

@Service(Service.Level.PROJECT)
@State(name = "DocsigSettings", storages = [Storage("docsig.xml")])
internal class DocsigSettings : PersistentStateComponent<DocsigState> {
    private var state = DocsigState()

    // returns the current in-memory state object shared with the
    // settings ui serialized into docsig.xml
    override fun getState(): DocsigState = state

    // replaces cached values after xml deserialization from disk
    override fun loadState(state: DocsigState) {
        this.state = state
    }
}
