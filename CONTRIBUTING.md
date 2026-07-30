# Contributing to docsig

Thanks for contributing — bug reports, ideas, and patches are all welcome.

## Code of Conduct

This project follows the
[docsig Code of Conduct](https://github.com/jshwi/docsig/blob/master/CODE_OF_CONDUCT.md).
Report unacceptable behavior to <s.whitlock@live.com>.

## Reporting issues

Bugs and feature requests are tracked on the
[issue tracker](https://github.com/jshwi/docsig/issues). Open a
[new issue](https://github.com/jshwi/docsig/issues/new/choose) and pick the
matching template — it asks for everything a report needs. Questions are
welcome as issues too.

Never report security problems on the public tracker — see the
[security policy](https://github.com/jshwi/docsig/blob/master/SECURITY.md).

## Contributing code

By submitting a change you confirm that you wrote it, that you have the
right to contribute it, and that it may be distributed under the
[project license](https://github.com/jshwi/docsig/blob/master/LICENSE).

Fork and clone the repository, then run make to set everything up

```shell
$ make
```

This builds the virtualenv, installs the git hooks, and prints the
available targets. Run the test suite with

```shell
$ make tests
```

## Testing

Coverage must stay at 100%, and the pipeline fails otherwise.

If a change fixes an issue, add a regression test to `tests/fix_test.py`.
For anything else, add tests to `tests/_test.py`. Base tests for core
functionality are organized into
[categories](https://docsig.io/en/latest/development/tests.html).

Don't worry about formatting — autoformatting runs on commit.

## Commit messages

Any clear commit message is fine, and messages may be tidied up on merge.
The [commit policy](https://docsig.io/en/latest/development/commit-policy.html)
is the standard the maintainer holds their own commits to — follow it if
you like, but it isn't required of contributors.
