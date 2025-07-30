# Manual GitHub Upload Instructions

Since Git commands are not working properly, here's how to upload your files manually:

## 1. Upload to GitHub

1. Go to https://github.com/Arielkfirr/Iron-Dome-for-Mosquitoes
2. Click "uploading an existing file" (or drag and drop)
3. Upload these files:
   - `src/` (entire folder)
   - `config/` (entire folder)
   - `models/` (entire folder)
   - `data/` (entire folder)
   - `requirements.txt`
   - `test_cat_detection.py`
   - `sync_phone_photos_to_git.py`
   - `run_test.bat`
   - `README.md`
   - `README_QUICK_START.md`
   - `CREATE_GITHUB_REPO.md`
   - `.gitignore`

4. Add commit message: "Initial upload: Iron Dome for Mosquitoes"
5. Click "Commit changes"

## 2. Alternative: Install GitHub Desktop

1. Download GitHub Desktop: https://desktop.github.com/
2. Install and sign in
3. Add the local repository: `C:\Users\Ariel\PycharmProjects\RaspberryPie\IronDomeMosquitoes`
4. Push to GitHub through the GUI

## 3. Test the Sync Script

After uploading, test the sync script:

```bash
python sync_phone_photos_to_git.py
```

## 4. Clone at Work

At your work computer:

```bash
git clone https://github.com/Arielkfirr/Iron-Dome-for-Mosquitoes.git
cd Iron-Dome-for-Mosquitoes
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python test_cat_detection.py
```

## Current Status

- ✅ Git installed
- ✅ Repository created on GitHub
- ✅ Sync script ready
- ⚠️ Need to upload files manually or fix Git connection

## Next Steps

1. Upload files to GitHub (manual or GitHub Desktop)
2. Test sync script
3. Start testing cat detection with Phone Link 