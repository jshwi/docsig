/**
 * Project-scoped docsig orchestration and PSI refresh.
 */
package com.github.jshwi.docsig.service

import com.intellij.openapi.project.Project
import com.intellij.util.Alarm

/**
 * A thin wrapper around IntelliJ’s com.intellij.util.Alarm.
 *
 * Implements the plugin’s own AlarmLike interface. DocsigService
 * schedules debounced work (save / idle) through AlarmLike, so
 * production code uses a real Alarm while tests can substitute a fake.
 *
 * Tests can replace how alarm instances are built (or avoid real
 * alarms) without mocking the whole adapter.
 *
 * @param project The current project.
 */
internal class AlarmAdapter(project: Project) : AlarmLike {
    private val alarm =
        alarmBuilder(project)

    // delegate straight to the underlying alarm
    override fun cancelAllRequests() {
        alarm.cancelAllRequests()
    }

    // delegate straight to the underlying alarm
    override fun addRequest(task: Runnable, delayMs: Long) {
        alarm.addRequest(task, delayMs)
    }

    override fun hasPendingRequests(): Boolean = !alarm.isEmpty

    internal companion object {
        var alarmBuilder: (Project) -> Alarm = ::buildAlarm

        // work runs off the edt on a pooled thread, and the alarm is
        // tied to the project so requests are canceled when the project
        // is disposed (standard intellij pattern)
        @Suppress("UnstableApiUsage")
        private fun buildAlarm(project: Project): Alarm =
            Alarm(Alarm.ThreadToUse.POOLED_THREAD, project)

        // restore the default after tests.
        internal fun resetAlarmBuilderForTests() {
            alarmBuilder = ::buildAlarm
        }
    }
}
