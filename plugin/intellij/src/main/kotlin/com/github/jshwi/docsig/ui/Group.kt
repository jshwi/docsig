package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.messages.DocsigBundle

internal enum class Group(internal val label: String) {
    CHECK(DocsigBundle.message("settings.group.check")),
    IGNORE(DocsigBundle.message("settings.group.ignore")),
    FILE_DISCOVERY(DocsigBundle.message("settings.group.file-discovery")),
    MESSAGES(DocsigBundle.message("settings.group.messages")),
}
