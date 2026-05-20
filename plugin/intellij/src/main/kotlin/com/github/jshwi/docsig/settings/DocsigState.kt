/**
 * Data class for the plugin settings.
 */
package com.github.jshwi.docsig.settings

import com.github.jshwi.docsig.ui.ClassCheckMode

/**
 * Serializable snapshot mirrored to disk under the component name.
 *
 * Mutable fields follow IntelliJ XML bean persistence conventions.
 *
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
 * @property excludes Path globs passed through --excludes (stored
 *     relative to the project root).
 * @property disable Message codes passed through --disable.
 * @property target Shared list backing several list option rows.
 */
internal data class DocsigState(
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
    var excludes: List<String> = emptyList(),
    var disable: List<String> = emptyList(),
    var target: List<String> = emptyList(),
)
