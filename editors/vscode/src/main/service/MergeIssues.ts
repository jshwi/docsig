import { Issue } from "../models/Issue";

/** Merge fresh cli output with cached issues when a global error occurs. */
export function mergeIssues(
  previous: Issue[] | undefined,
  issues: Issue[],
): Issue[] {
  const hasGlobalError = issues.some(
    (issue) => issue.exit === 2 && issue.line === null,
  );
  if (!hasGlobalError) {
    return issues;
  }

  const prevLineIssues = (previous ?? []).filter(
    (issue) => issue.line !== null,
  );
  const globalIssues = issues.filter((issue) => issue.line === null);
  return [...prevLineIssues, ...globalIssues];
}
