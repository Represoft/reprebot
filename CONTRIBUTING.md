# Contributing Guidelines

Before starting make sure you have a
[GitHub](https://docs.github.com/en/get-started/start-your-journey/creating-an-account-on-github) account.

To send your contributions follow these steps:

1. Write an issue for your idea if it doesn't exist
[here](https://github.com/Represoft/reprebot/issues).

2. [Fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) the [reprebot](https://github.com/Represoft/reprebot) repository.

3. [Clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) your fork:

```sh
git clone https://github.com/{your-username}/reprebot.git
```

Owners can clone the repository directly instead of fork it.

4. Set up the development environment:

    1. Install [Python](https://www.python.org/downloads/).
    2. Install [Git](https://git-scm.com/downloads).
    3. Install [pip](https://pip.pypa.io/en/stable/installation/).
    4. Install [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).
    5. [Create](https://docs.python.org/3/library/venv.html) a virtual
    environment inside your cloned repository: `python3 -m venv env`.
    6. [Activate](https://docs.python.org/3/tutorial/venv.html) the virtual
    environment. On Windows, run `env\Scripts\activate`, and on Linux run
    `source env/bin/activate`.
    7. Install the dependencies: `pip install -r requirements.txt`.
    10. Run the unit tests: `pytest test/unit/src`

5. Create a branch with the following naming convention:

```
reprebot-<your-github-username>
```

For example if your GitHub username is `happy-cat`, name your branch
`reprebot-happy-cat`.

Create and switch to your branch:

```
git checkout -b <your-branch-name>
```

6. Code your idea. Make sure you run the unit tests each time and that they
pass.

7. Commit your changes locally.

Use the following convention for your commit messages:

```
reprebot/[type]: #[issue-number] [title]

[body]
```

For the type of your commit use any of the following depending on what've you
implemented:

- `feat`: if it's a new feature or enhancement in performance
- `fix`: if it's a fix to a bug
- `refac`: if it's a refactoring of some kind
- `style`: if it's related to code style only
- `test`: if it's adding or improving tests

Here's an example of a commit message:

```
reprebot/feat: #19 define the llm client class

- define the `LLMClient` class
- use `LLMClient` class in `app` module
```

8. Rebase onto the `main` branch.

Do this only if there are changes in the `main` branch.

```sh
# Switch to the 'main' branch
git checkout main

# Pull latest changes from the 'main' branch
git pull

# Switch to your branch branch
git checkout <your-branch-name>

# Rebase your branch branch onto 'main'
git rebase main
```

Fix any conflict that might arise during the rebase.

9. Push your changes to your branch.

```sh
git push --set-upstream origin <your-branch-name>
```

10. Wait for the pipelines to succeed.

11. Create a pull request from your fork to [reprebot](https://github.com/Represoft/reprebot).

If you're an owner, create the PR from your branch instead.

> [!NOTE]
> Make sure your PR are only 1 commit ahead of **reprebot** `main` branch.
Sometimes you make a commit and realize something needs to change. In that case
use `git commit --amend` when you're finished with your changes. If you already
pushed the commit to your branch, you don't need to use
`git push --set-upstream origin <your-branch-name>` but just `git push -f`. You
can do this as many times as you need to make sure the build pipeline succeeds
before creating your PR.
