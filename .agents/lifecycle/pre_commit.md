# Pre-Commit Checklist

> Workspaces may contain one repo, nested repos, or ignored project folders.
> Identify the target Git root before every Git command. See
> `.agents/rules/commit_policy.md` for the canonical process.

1. Resolve the target repo with `git -C <path> rev-parse --show-toplevel`.
2. Compare the target repo with `.agents/project/repos.md` if that overlay file
   exists.
3. Use `git -C <repo>` for every command.
4. Run `git -C <repo> status` and optionally `git -C <repo> status --short --branch`
   for a compact view.
5. Run `git -C <repo> diff` for unstaged and `git -C <repo> diff --cached` for
   staged changes.
6. Review untracked files; never blanket-add.
7. Separate current-agent changes from pre-existing user changes.
8. Confirm no unrelated user changes are staged.
9. Check for sensitive files, generated files, binary replacements, and lock
   conflicts.
10. Run relevant validation for the touched files.
11. Confirm the commit message follows `.agents/rules/commit_policy.md`,
    including the forbidden-patterns list.
12. Confirm the `commit-msg` hook is active in the target repo when hooks are
    part of the project workflow. If not active, document the activation command
    for the user; do not bypass with `--no-verify`.
