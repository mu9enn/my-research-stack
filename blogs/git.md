# Git Reference

Minimal high-frequency Git commands for daily research workflow.

---
## 0. Common Workflow

```bash
git pull --rebase
git checkout -b feature-x
# edit files
git add .
git commit -m "feat: implement x"
git push -u origin feature-x
```

---

## 1. Setup

```bash
git clone <repo-url>
git init
git remote -v
git remote add origin <repo-url>
```

---

## 2. Status & Diff

```bash
git status
git diff
git diff --staged
git log --oneline --graph --decorate
```

---

## 3. Add & Commit

```bash
git add <file>
git add .
git restore <file>            # discard changes
git commit -m "message"
git commit --amend            # modify last commit
```

---

## 4. Branching

```bash
git branch
git branch <branch-name>
git checkout <branch-name>
git checkout -b <branch-name>
git switch <branch-name>
git merge <branch-name>
git branch -d <branch-name>
```

---

## 5. Sync with Remote

```bash
git pull
git pull --rebase
git push
git push -u origin <branch-name>
git fetch
```

---

## 6. Undo & Recovery

```bash
git reset --soft HEAD~1
git reset --hard HEAD~1
git revert <commit-id>
git stash
git stash pop
git reflog
```

---

## 7. File Tracking

```bash
git rm <file>
git mv <old> <new>
git ls-files
```

---

## 8. Ignore Files

`.gitignore` example:

```
__pycache__/
*.pyc
.env
*.log
.DS_Store
```

---

## 9. Clean

```bash
git clean -n
git clean -fd
```

---



