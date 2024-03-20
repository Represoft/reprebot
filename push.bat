@echo off
setlocal

:: Check if the current directory is a git repository
if exist ".git" (
    :: Retrieve GitHub username from Git configuration
    for /f "tokens=*" %%a in ('git config user.name') do (
        set username=%%a
    )

    if defined username (
        echo Your GitHub username is: %username%

        :: Perform git operations with dynamic branch name
        git checkout main
        git pull
        git checkout "reprebot-%username%"
        git rebase main
        git push -f --set-upstream origin "reprebot-%username%"
    ) else (
        echo GitHub username not found.
    )
) else (
    echo Not a git repository.
)
