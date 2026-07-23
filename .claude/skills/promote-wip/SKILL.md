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
- **Open the PR yourself; never hand that step to the user.** The `Closes #<N>`
  body is the only thing that closes the issue, and a PR opened from the
  terminal link lands with an empty body.

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
- **Header fits 72 chars** including the `(#<N>)` suffix (`.conform.yaml`
  `header.length`).

Check a candidate before committing rather than guessing:

```bash
printf '%s\n\nSigned-off-by: <name> <email>\n' "<subject>" > /tmp/cm.txt
conform enforce --commit-msg-file /tmp/cm.txt
```

Every policy reports individually. **GPG always FAILs here** — a bare message
file has no commit to verify — so read the other rows and ignore that one; it
passes on the real signed commit.

The news fragment is the subject verbatim (see CLAUDE.md), so the subject _is_
the changelog line. Prefer the descriptive house style over a literal `wip:`
carry-over — compare `fix: google docstrings undetected by keyword args section`
against the internal jargon of the wip subject it came from.

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

`--body` is mandatory. Never use `--fill`: it copies the commit _body_, which is
only the `Signed-off-by` trailer, leaving the PR with no description and no
closing keyword.

### 9. Report

Give the user the issue URL, the new commit SHA, and the PR URL. Call out any
deviation from the literal wip subject (a conform reword) and note the pipeline
is running.

### 10. Merge

```bash
git checkout master && git merge <issue-branch> && git push
```

master fast-forwards, and GitHub marks the PR merged by itself once the head
commit lands on the default branch — PR #1003's `merge_commit_sha` equals its
head SHA, so no merge commit is created. That auto-merge is what fires
`Closes #<N>` from the PR body.

So the PR must exist, with the keyword in its body, **before** master is pushed.
If the issue is still open afterwards, the body was the problem, not the merge
route. Recover with:

```bash
gh issue close <N> --repo jshwi/docsig --reason completed --comment "Fixed in <sha> on master."
gh api -X DELETE repos/jshwi/docsig/git/refs/heads/<issue-branch>
```

Leave the PR alone while doing so — closing it by hand records it as `CLOSED`
rather than `MERGED`, preempting the auto-detection.

### 11. After the merge, when rebasing dev/main

`git rebase master` on `dev/main` replays the wip commit that was just promoted.
It does **not** drop out automatically: if the promoted commit gained anything
the wip lacked (an extra test probe, a reworded docstring) the patch IDs differ,
so git replays it and conflicts.

- **The promoted wip itself → `git rebase --skip`.** Confirm master supersedes it
  first, by checking every line the wip added is present in the promoted commit:
  ```bash
  git diff <wip>~1 <wip> -- <file> > /tmp/wip.patch
  git diff <promoted>~1 <promoted> -- <file> > /tmp/master.patch
  grep '^+' /tmp/wip.patch | grep -vxFf <(grep '^+' /tmp/master.patch)
  ```
  Empty output (or only lines you deliberately reworded) means skipping is safe.
- **Later commits appending to the same file → resolve, never skip.** Tests all
  append to the end of `tests/fix_test.py`, so an unrelated wip that adds a test
  there collides with whatever the promotion added last. Keep both sides.
- Run the full suite before `git push --force-with-lease` — a hand-resolved
  conflict is not covered by the PR pipeline that already passed.

Pre-flight the whole thing while the pipeline runs, in a throwaway detached
worktree, so the conflicts are known before touching `dev/main`:

```bash
git worktree add -f --detach <scratch>/rb dev/main && cd <scratch>/rb
git rebase <promoted-sha>
```

## Quick reference

| Symptom                                           | Cause                                 | Action                                             |
| ------------------------------------------------- | ------------------------------------- | -------------------------------------------------- |
| conform: `Header Case ... not lower`              | description starts uppercase          | reword to lead with a lowercase verb               |
| conform: spellcheck misspelling                   | coined jargon in subject              | use dictionary words                               |
| `check news ... Created news fragment` then error | expected first-attempt block          | commit again                                       |
| `commit description changed, updated <N>.fix.md`  | subject changed between attempts      | commit again                                       |
| cherry-pick conflict                              | fix depends on dev/main-only refactor | land the refactor on master first                  |
| branch named `...-1`                              | `gh issue develop` run twice          | delete both branches (local+remote), recreate once |
| conform: `GPG ... reference not found`            | preflighting a bare message file      | ignore; real signed commits pass                   |
| dev/main rebase conflicts on the promoted wip     | promoted commit differs from the wip  | verify master supersedes it, then `--skip`         |
| dev/main rebase conflicts at end of `fix_test.py` | two commits append tests there        | resolve keeping both, never `--skip`               |
