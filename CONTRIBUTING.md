# Contributing Steps

To send your contributions follow these steps:

1. Write an issue for your idea if it doesn't exist [here](https://github.com/Represoft/reprebot/issues).

2. Clone the repository:

```sh
git clone https://github.com/Represoft/reprebot.git
```

3. Set up the development environment:

> You will need a recent version of Python, a Python environment manager and a Python package manager installed in your system. Here we're going to use: `virtualenv` and `pip` but you can use any other that you find more convenient.

**Create the virtual environment:**

```sh
python3 -m venv env
```

**Activate the environment:**

On Windows run:

```sh
cd env/Scripts
activate
cd ../..
```

On Linux run:

```
source env/bin/activate
```

**Install the required dependencies:**

```sh
pip install -r requirements.txt
```

4. Create a branch with the following naming convention:

```
reprebot-<your-github-username>
```

For example if your GitHub username is `happy-cat`, name your branch `reprebot-happy-cat`.

Create and switch to your branch:

```
git checkout -b <your-branch-name>
```

5. Code your idea.

6. Commit your changes locally.

Use the following convention for your commit messages:

```
reprebot/[type]: #[issue-number] [title]

[body]
```

For the type of your commit use any of the following depending on what've you implemented:

- `feat`: if it's a new feature or enhancement in performance
- `fix`: if it's a fix to a bug
- `refac`: if it's a refactoring of some kind
- `test`: if it's adding or improving tests

Here's an example of a commit message:

```
reprebot/feat: #19 define the llm client class

- define the `LLMClient` class
- use `LLMClient` class in `app` module
```

7. Rebase onto the `main` branch.

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

8. Push your changes to your branch.

```sh
git push --set-upstream origin <your-branch-name>
```

9. Wait for the pipelines to succeed.

10. Create a pull request.
