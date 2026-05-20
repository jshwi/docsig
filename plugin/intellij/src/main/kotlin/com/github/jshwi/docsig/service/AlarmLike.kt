/**
 * Project-scoped docsig orchestration and PSI refresh.
 */
package com.github.jshwi.docsig.service

/**
 * Mirror scheduling operations service needs from IntelliJ’s Alarm.
 *
 * Cancel pending work, and schedule a Runnable after a delay
 * (milliseconds).
 *
 * Production code uses AlarmAdapter, which implements this interface
 * with a real Alarm. Tests can supply a fake implementation that
 * records calls or runs work synchronously, without constructing
 * platform Alarm instances.
 *
 * So AlarmLike is the seam: the service depends on “something
 * alarm-shaped,” not on Alarm directly.
 */
internal interface AlarmLike {
    /**
     * drop any queued debounced tasks.
     *
     * For example, before scheduling a new run for the same path.
     */
    fun cancelAllRequests()

    /**
     * Run task after delayMs (debounce / coalesce behavior).
     */
    fun addRequest(task: Runnable, delayMs: Long)

    /**
     * True when a delayed task is still queued (not yet run).
     */
    fun hasPendingRequests(): Boolean
}
