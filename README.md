# Some useful scripts

|                              |                                                              |
|------------------------------|--------------------------------------------------------------|
| `gh-rm-merged`               | Deletes a branch, but only if it’s been merged via a PR.     |
| `./githooks/jira-intellij/`  | git hooks for Jira + IntelliJ integration                    |
| `vscode_to_idea-node-attach` | updates node.js attach configs from VS Code to IntelliJ IDEA |

## `gh-rm-merged`

This is useful when you merge via rebase or squash. In those situations, your local commit isn’t actually in the main
branch, so you can’t use the safe `-d` option to delete it. You can use `-D`, but then you need to make sure your branch
really is merged. `git diff` isn’t a great way to do that, because the diff can be non-empty if other commits came in
after yours. So, this script effectively checks that your commit really is merged, and then does `-D` on your behalf.

## `./githooks/jira-intellij/`

If you create a task in IntelliJ that references a Jira ticket, these scripts will check that the ticket is still open, and if so, add a reference to it to your commit messages.

To use it, symlink the scripts to your repo's `.git/hooks/` dir. Alternatively, you can or invoke them from existing scripts you have there, making sure to forward all the args:

    /path/to/yshavit/scripts/githooks/jira-intellij/$(basename "$0") "$@"

## 'vscode_to_idea-node-attach`

Looks through all of the `*/.vscode/launch.json` files in the given directory (or `$PWD`, if unspecified) to find launch
configurations for attaching to Node.js processes. Upserts them into a same-named configuration in your IDEA configs.
The IDEA configs must be in `./idea/workspace.xml` relative to the dir you specify (or PWD).

