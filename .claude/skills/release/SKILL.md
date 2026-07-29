---
name: release
description: Publish a docsig release — verify conform over the range, bump the version so towncrier folds the changelog fragments in, merge and tag, publish to PyPI, create the GitHub release, then rebase dev/main. Use when the user says "publish a release", "cut v<N>", "make bump", or otherwise asks to ship a version.
---

# Publishing a docsig release

Run these from the clone, never from the maintainer's checkout. `make bump`
runs the pre-commit hooks, so the working tree needs a `.venv` first
(`make install-venv`).

## 1. Verify every commit since the last tag passes conform

```bash
git rebase v<prev> -x 'conform enforce'
```

Fix anything this reports before going further — a subject that fails conform
here fails the tag push later.

## 2. Bump the version on a temp branch

towncrier folds the `changelog/` fragments into `CHANGELOG.md` as part of this.

```bash
git checkout -b bump
make bump part=patch   # or major|minor
```

## 3. Merge to master, push commits and tag

```bash
git checkout master && git merge bump && git push && git push --tags
git branch -d bump
```

## 4. Publish to PyPI

```bash
make publish
```

## 5. Create the GitHub release

Use the new `CHANGELOG.md` section as the body. Anything a changelog fragment
could not carry — such as a fix that surfaces new violations on unchanged
code — belongs here, and should already be staged in the PR body from when the
fix was promoted.

```bash
gh release create v<N> --repo jshwi/docsig --title "v<N>" --notes "..."
```

## 6. Rebase dev/main onto master

```bash
git checkout dev/main && git rebase master && git push --force-with-lease
```
