# Linux & Bash Essentials

**Phase:** 1 (Foundation)  
**Prerequisites:** None — this is your starting point  
**When to Skip:** Only if you can write a bash script with loops, conditionals, and piping without Googling  
**Projects This Enables:** Every single project in this course. You cannot be a data engineer without the terminal.

## What to Cover

### 1. Navigation & File Operations
- `ls`, `cd`, `pwd`, `mkdir`, `rm`, `cp`, `mv`, `touch`
- Wildcards (`*`, `?`, `[]`) and globbing
- `find` and `locate`

### 2. Text Processing (The Data Engineer's Toolkit)
- `cat`, `head`, `tail`, `less`, `more`
- `grep` (with regex, `-i`, `-v`, `-c`, `-n`)
- `sed` and `awk` (basic substitution and field extraction)
- `sort`, `uniq`, `wc`, `cut`, `paste`
- **Pipe chaining:** `cat file.csv | grep "ERROR" | cut -d',' -f3 | sort | uniq -c`

### 3. Permissions & Users
- `chmod`, `chown`, `sudo`
- File permissions (`rwx`, numeric `755`, `644`)
- `ps`, `top`, `htop`, `kill`, `killall`

### 4. Shell Scripting
- Variables, quoting (`"` vs `'` vs `` ` ``)
- `if/else`, `for` loops, `while` loops
- Functions in bash
- Exit codes (`$?`) and `set -euo pipefail`
- Cron jobs (`crontab -e`)

### 5. Environment & Configuration
- `.bashrc`, `.bash_profile`, `.zshrc`
- Environment variables (`export`, `env`, `echo $PATH`)
- `ssh` and `scp` basics

## Hands-On Exercise

Write a bash script that:
1. Downloads a CSV file from a URL
2. Counts the number of rows
3. Extracts unique values from column 2
4. Saves the result to a timestamped file

## Why This Matters for Data Engineering

- 90% of your data pipelines will run on Linux servers
- Bash is the glue between Python scripts, Docker, and cloud CLIs
- Log analysis and debugging happen in the terminal
- Your Airflow workers, Spark executors, and Docker containers all run Linux

## Next File
→ `03-Git-Version-Control.md`
