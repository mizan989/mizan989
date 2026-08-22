# Setup (Windows / PowerShell)

## 1. Create the magic repo
Repo name must exactly match your GitHub username.

```powershell
gh repo create mizan989 --public --clone
cd mizan989
```

Then copy in everything from this build: `scripts/`, `.github/workflows/`, `README.md`, `SETUP.md`.

## 2. Python environment
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r scripts\requirements.txt
```
`pillow`, `numpy`, `opencv-python`, `rembg` are only needed locally for the one-time portrait step — the daily GitHub Actions workflow only installs `requests` + `beautifulsoup4`.

## 3. Generate the ASCII portrait (one time, or whenever your photo changes)
Drop a clear, front-facing photo into the repo root, then:

```powershell
python scripts\prep_photo.py my-photo.jpg
python scripts\make_ascii_svg.py
```
This writes `source-prepped.png` (intermediate — fine to `.gitignore`) and `mizan-ascii.svg`.

## 4. Generate the info card
```powershell
python scripts\make_info_card.py
```
Edit the `ROWS` list at the top of `scripts\make_info_card.py` any time you want to update Now/Prev/Stack/Highlights text — it's plain Python, no rebuild step needed beyond re-running the script.

## 5. Generate the first heatmap
```powershell
mkdir data
python scripts\fetch_contributions.py
python scripts\render_heatmap_svg.py
```

## 6. Push and verify
```powershell
git add .
git commit -m "profile: animated terminal README"
git push
```
Open `github.com/mizan989` and confirm all three SVGs render and animate.

## 7. Turn on the daily refresh
In your repo → **Actions** tab → find "Update profile art" → **Run workflow** once by hand to confirm it commits a fresh `contrib-heatmap.svg`. After that the cron (`17 6 * * *` UTC) keeps it current automatically.

## Notes / gotchas
- GitHub strips inline `<style>` margins from README HTML — only `<br>` gives you vertical spacing.
- `<h1>`/`<h2>` draw a full-width underline; this README uses `<h3>` for the terminal-prompt headers to avoid that.
- If a script errors on `Select-String`-style pattern checks you're doing yourself, remember: PowerShell uses `Select-String -Path file -Pattern "term"`, not `grep`.
- Re-run `make_ascii_svg.py` / `make_info_card.py` locally and `git push` any time you want to update them — only the heatmap is automated.
