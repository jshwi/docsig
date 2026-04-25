package com.github.jshwi.docsig.model

import com.github.jshwi.docsig.ui.ClassCheckMode

/**
 * Serializable snapshot mirrored to disk under the component name.
 *
 * Mutable fields follow IntelliJ XML bean persistence conventions.
 *
 * @property cliPath Executable path or bare command on PATH.
 * @property classCheckMode Class docstring check mode for the CLI.
 * @property checkDunders Whether dunder definitions are checked.
 * @property checkNested Whether nested callables are checked.
 * @property checkOverridden Enables checks on overridden methods.
 * @property checkPropertyReturns Enables property return checks.
 * @property checkProtected Whether protected members are checked.
 * @property ignoreArgs Ignores positional vararg shape mismatches.
 * @property ignoreKwargs Ignores keyword vararg shape mismatches.
 * @property ignoreNoParams Whether empty param lists are ignored.
 * @property includeIgnored Whether git-ignored paths are scanned.
 * @property exclude Pattern of paths to exclude.
 * @property disable Message codes passed through --disable.
 * @property target Shared list backing several list option rows.
 */
data class DocsigState(
    var cliPath: String = "docsig",
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
    var disable: List<String> = emptyList(),
    var target: List<String> = emptyList(),
)
