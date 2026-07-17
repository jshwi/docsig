---
name: promote-wip
description: Promote a docsig `wip:` commit from dev/main to a `fix:` on master — open the GitHub issue, cherry-pick, let the commit-msg hook build the news fragment, and open a PR. Use when the user says "promote <sha>", "create an issue for <sha> and open a PR", or otherwise asks to ship a wip commit.
---

# Promote a wip commit to master

Turn a `wip:` commit on `dev/main` into a `fix:` commit on an issue branch, then a
PR targeting `master`. This is the `wip → master promotion` workflow from
`CLAUDE.md`, with the sharp edges that only show up when you run it.

**Input:** a commit SHA (the `wip:` commit). If the user gives more than one,
repeat the whole flow once per SHA — one issue and one PR each.

## Non-negotiables

- **Never create the GitHub issue or news fragments by hand.** The issue is
  opened here; the fragment is created by the `commit-msg` hook. Manually
  writing either breaks the flow.
- **Every commit uses `git commit -s`** (conform enforces DCO sign-off).
- **`gh issue develop` runs once per issue.** A second run makes a `-1` branch;
  if that happens, delete both local and remote copies of both branches and
  start the branch step over.
- **After every commit, confirm `HEAD` actually moved** — the `rtk`/hook output
  can print `ok` even when a hook blocked the commit.

## Steps

### 1. Inspect the commit

```bash
git show <sha>
git branch --contains <sha>        # expect: dev/main
```

Read the diff. Note which files it touches and whether the fix is
self-contained or leans on a preparatory refactor.

### 2. Confirm it applies to master

`dev/main` carries refactors master doesn't have (module renames, etc.). The fix
only ports cleanly if the files/regions it edits also exist on master.

- Check the touched files exist on master and the surrounding context matches
  (e.g. `git grep -n '<nearby line>' master -- <file>`).
- If the fix **depends on** a `refactor:` commit that isn't on master yet, land
  that refactor on master first via a temp branch (see CLAUDE.md
  "Prerequisite refactors"), then rebase before cherry-picking.
- If it's independent (most one-file fixes are), continue.

### 3. Open the issue

Title = a clear description of the bug. Body = a short explanation plus a minimal
reproducer.

```bash
gh issue create --repo jshwi/docsig --title "<bug title>" --body "<desc + repro>"
```

Grab the issue number `<N>` from the returned URL.

### 4. Create and check out the issue branch

```bash
gh issue develop <N> --repo jshwi/docsig --checkout
```

This branches off master. Verify with `git branch --show-current`.

### 5. Cherry-pick and stage

```bash
git cherry-pick <sha>
git reset --soft HEAD~1      # keep the changes staged, drop the wip commit
git status --short           # expect the touched files, all staged (M)
```

If the cherry-pick conflicts, stop and reassess step 2 — the fix probably
depends on something only on `dev/main`.

### 6. Craft the final subject

Transform the wip subject: strip `wip:`, the word after it becomes the type,
append the issue number.

```
wip: fix <subject>   →   fix: <subject> (#<N>)
```

Then make it satisfy **conform** (it runs as a commit-msg hook and will reject
otherwise):

- **Description starts lowercase.** If stripping `wip: fix ` leaves an uppercase
  first word (e.g. an error code like `SIG306`), reword so a lowercase verb
  leads: `fix: stop SIG306 false positive ...`.
- **No `and` in the subject.** Split the work into two commits if you need it.
- **Spellcheck-safe words.** Avoid coined jargon like `dedup`/`params`; prefer
  dictionary words (`reduce`, `parameters`, `deduplicate` spelled out).
- **Header stays short** (~66 chars including the `(#<N>)` suffix).

The news fragment is derived from this subject, so a clean subject also reads
well in the changelog.

### 7. Commit (expect two or three attempts)

Run make, then commit. The first attempt is _designed_ to fail — the hook
creates `changelog/<N>.fix.md` and blocks:

```bash
make && git add . && git commit -s -m "fix: <subject> (#<N>)"
```

Look at the tail: `Created news fragment at .../changelog/<N>.fix.md`, and
confirm `conform ... Passed`. If conform **failed**, fix the subject (step 6)
before continuing.

Commit again to pick up the fragment:

```bash
git add . && git commit -s -m "fix: <subject> (#<N>)"
```

If you reworded the subject between attempts, the hook prints
`commit description changed, updated <N>.fix.md` and blocks once more — just run
the same commit a third time. Then:

```bash
git log --oneline -1        # confirm HEAD is the new fix: commit
git show --stat HEAD        # confirm changelog/<N>.fix.md + the fix files
```

### 8. Push and open the PR

```bash
git push -u origin <issue-branch>
gh pr create --repo jshwi/docsig --base master \
  --head <issue-branch> \
  --title "fix: <subject> (#<N>)" \
  --body "Closes #<N>

<what was wrong + what the fix does>"
```

### 9. Report

Give the user the issue URL, the new commit SHA, and the PR URL. Call out any
deviation from the literal wip subject (a conform reword) and note the pipeline
is running.

## Quick reference

| Symptom                                           | Cause                                 | Action                                             |
| ------------------------------------------------- | ------------------------------------- | -------------------------------------------------- |
| conform: `Header Case ... not lower`              | description starts uppercase          | reword to lead with a lowercase verb               |
| conform: spellcheck misspelling                   | coined jargon in subject              | use dictionary words                               |
| `check news ... Created news fragment` then error | expected first-attempt block          | commit again                                       |
| `commit description changed, updated <N>.fix.md`  | subject changed between attempts      | commit again                                       |
| cherry-pick conflict                              | fix depends on dev/main-only refactor | land the refactor on master first                  |
| branch named `...-1`                              | `gh issue develop` run twice          | delete both branches (local+remote), recreate once |
