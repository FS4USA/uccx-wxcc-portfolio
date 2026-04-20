# Pushing this portfolio to GitHub

Your GitHub account: **[FS4USA](https://github.com/FS4USA)**.

## One-time setup on GitHub

1. Go to https://github.com/new
2. **Repository name:** `uccx-wxcc-portfolio` (or whatever you prefer)
3. **Description:** `UCCX & Webex Contact Center portfolio — script patterns, flows, API integrations, and CDR analysis.`
4. **Public**.
5. Do **NOT** check "Initialize with README" / LICENSE / .gitignore (we already have these).
6. Click **Create repository**.

GitHub will show you the remote URL, something like:
```
https://github.com/FS4USA/uccx-wxcc-portfolio.git
```

## Initialize and push (run these in the portfolio folder)

Open a terminal in the `uccx-wxcc-portfolio/` folder and run:

```bash
git init -b main
git add .
git commit -m "Initial commit: UCCX and Webex Contact Center portfolio"
git remote add origin https://github.com/FS4USA/uccx-wxcc-portfolio.git
git push -u origin main
```

If you hit an auth prompt, use a **GitHub Personal Access Token** (PAT) as the password — not your account password. Create a PAT at https://github.com/settings/tokens (fine-grained token with `Contents: Read and write` on this one repo is enough).

## Before every future `git push`

Run the sanitization scan to make sure no real customer data is about to leak:

```bash
# From the repo root
grep -rEin "jack ?henry|jha|symitar|episys|bankeasy|bankwithchoice|marconet|cashmgmt|businesssolutions|\bwires\b" . --include="*.md" --include="*.json" --include="*.py"
grep -rEn "[A-Za-z0-9._%+-]+@(?!example\.com)[A-Za-z0-9.-]+\.[A-Za-z]{2,}" . --include="*.md" --include="*.json" --include="*.py"
grep -rEn "\+1[2-9]\d{9}" . --include="*.md" --include="*.json" --include="*.py"
```

Any output from those commands means a real token slipped in — fix it before pushing.
