# Git Version Control

**Phase:** 1 (Foundation)  
**Prerequisites:** `02-Linux-Bash-Essentials.md` (basic terminal comfort)  
**When to Skip:** If you can rebase, resolve merge conflicts, and use `git bisect` confidently  
**Projects This Enables:** All projects. Your WDI ETL pipeline is already on GitHub.

## What to Cover

### 1. Core Concepts
- Repository, working directory, staging area
- Commits as snapshots (not diffs)
- Branches as pointers to commits
- HEAD, detached HEAD state

### 2. Essential Commands
- `init`, `clone`, `status`, `add`, `commit`, `push`, `pull`
- `branch`, `checkout`, `switch` (modern syntax)
- `merge`, `rebase` (when to use which)
- `stash`, `pop`, `apply`
- `log`, `diff`, `blame`, `show`

### 3. Branching Strategies
- Feature branches
- GitHub Flow vs. Git Flow
- Pull Requests and code review
- `git rebase -i` for clean history

### 4. Undoing Mistakes
- `git reset` (soft, mixed, hard)
- `git revert` (safe undo for shared history)
- `git reflog` (the safety net)
- `git cherry-pick`

### 5. Collaboration
- Forking vs. branching
- `.gitignore` patterns (especially for data files: `*.csv`, `data/raw/`)
- GitHub Actions basics (CI triggers on push)
- Git LFS for large files (but prefer cloud storage for data)

### 6. Advanced (Phase 5+ Return)
- `git bisect` for finding bugs
- Submodules and subtrees
- Hooks (`pre-commit`, `post-merge`)

## Hands-On Exercise

1. Create a repo for your learning notes
2. Make a feature branch for "sql-notes"
3. Add 3 commits with meaningful messages
4. Rebase to squash them into 1 commit
5. Open a PR to yourself and merge

## Why This Matters for Data Engineering

- Your pipeline code lives in Git
- dbt uses Git for version control of SQL transformations
- Airflow DAGs are deployed via Git
- Data contracts and schemas are versioned in Git
- Team collaboration on shared data infrastructure

## Next File
→ `05-Python-Core-for-Data-Engineering.md`
