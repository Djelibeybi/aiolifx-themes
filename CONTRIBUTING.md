# Contributing

Contributions are welcome, and very much appreciated! Every little helps, and credit will always be given.

Here are some of the ways you can contribute:

## Types of Contributions

### Report a bug

We use [GitHub issues][gh-issues] to track bugs. When reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

### Fix a bug

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help wanted" is open to whoever wants to tackle it.

### Add a new features

Look through the GitHub issues for features. Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.

### Write documentation

There's no such thing as too much documentation. It doesn't even have to be part of the official docs: let us know if you blog or post on social media about the project so we can link to your content.

### Provide feedback or suggest a feature

The best way to provide feedback or suggest a new feature is by opening a [GitHub issue][gh-issues]. If you are proposing a feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember that this is a volunteer-driven project, and that contributions are welcome 😊

## Getting started

Ready to contribute? Here's how to set up your local development environment.

1. Fork this repo on GitHub.

2. Clone your fork locally:

   ```shell
   git clone git@github.com:your_name_here/aiolifx-themes.git
   ```

3. Install the project dependencies using [Poetry](https://python-poetry.org):

   ```shell
   cd aiolifx-themes
   poetry install
   ```

4. Create a branch for local development:

   ```shell
   git checkout -b name-of-your-bugfix-or-feature
   ```

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass our tests:

   ```shell
   poetry run pytest
   ```

6. Linting is done using [pre-commit](https://pre-commit.com). We recommend installing it globally, then you can either run all the linters as a once-off action:

   ```shell
   pre-commit run -a
   ```

   Or better still, install the hooks once and have them run automatically each time you commit:

   ```shell
   pre-commit install
   ```

7. Commit your changes and push your branch to GitHub:

   ```shell
   git add .
   git commit -m "feat(something): your detailed description of your changes"
   git push origin name-of-your-bugfix-or-feature
   ```

   Note: your commit message should follow the [conventional commits](https://www.conventionalcommits.org) standard. We run [`commitlint` on CI](https://github.com/marketplace/actions/commit-linter) to validate this, and if you installed pre-commit hooks during the previous step, the message will be checked as part of the commit process.

8. Submit a pull request through the GitHub website or using the GitHub CLI (if you have it installed):

   ```shell
   gh pr create --fill
   ```

## Pull request guidelines

We like to have the pull request open as soon as possible as it's a great place to discuss any piece of work, even unfinished. You can open a draft pull request if it's still a work in progress. Here are a few guidelines to follow:

1. Include tests for all new features or bug fixes.
2. Update the documentation for significant features or anything that's visible to a user.
3. Ensure the tests run by GitHub Actions are passing.

## Tips

To run a subset of tests:

```shell
pytest tests
```

## Making a new release

The deployment is semi-automated and can be triggered from the Semantic Release workflow in GitHub. The next version will be based on [the commit logs](https://python-semantic-release.readthedocs.io/en/latest/commit-log-parsing.html#commit-log-parsing). This is done by [python-semantic-release](https://python-semantic-release.readthedocs.io/en/latest/index.html) via a GitHub action.

[gh-issues]: https://github.com/Djelibeybi/aiolifx-themes/issues
