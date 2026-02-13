# Fixing Pylance Import Errors

## Current Issue

You're seeing these Pylance import errors:
- `Import "pdfplumber" could not be resolved`
- `Import "docx" could not be resolved`
- `Import "transformers" could not be resolved`
- `Import "torch" could not be resolved`
- `Import "numpy" could not be resolved`
- `Import "sklearn.metrics.pairwise" could not be resolved from source`

## Root Cause

The Python packages haven't been successfully installed yet due to build issues with MSYS2 Python in PowerShell. MSYS2 Python is missing development headers (`Python.h`) needed to build numpy from source.

## Quick Fix: Install via MSYS2 MINGW64 Terminal

### Step 1: Open MSYS2 MINGW64 Terminal

1. Press Windows key, search for "MSYS2 MINGW64"
2. Open the MINGW64 terminal (NOT PowerShell)

### Step 2: Install Python Development Package

```bash
pacman -S mingw-w64-ucrt-x86_64-python-devel --noconfirm
```

### Step 3: Install ML Packages via pacman (Easiest)

```bash
pacman -S mingw-w64-ucrt-x86_64-python-numpy \
          mingw-w64-ucrt-x86_64-python-pandas \
          mingw-w64-ucrt-x86_64-python-scikit-learn \
          mingw-w64-ucrt-x86_64-python-pytorch-cpu \
          --noconfirm
```

### Step 4: Install Remaining Packages with pip

```bash
cd /d/Hacks-Projects/CIVISM-main/civisim/ml
source ml_venv/bin/activate
pip install transformers pdfplumber python-docx spacy matplotlib seaborn plotly
```

### Step 5: Configure VS Code Python Interpreter

1. In VS Code, press `Ctrl+Shift+P`
2. Type `Python: Select Interpreter`
3. Select: `./ml_venv/bin/python` (3.12.9)
4. Press `Ctrl+Shift+P` again
5. Type `Developer: Reload Window`

✅ Import errors should now be resolved!

## Alternative: Use Windows Native Python (Recommended if MSYS2 doesn't work)

### Step 1: Install Python from python.org

1. Go to https://www.python.org/downloads/
2. Download Python 3.11 or 3.12 for Windows
3. Run installer
4. ✅ **Check "Add Python to PATH"**
5. Click Install

### Step 2: Create New Virtual Environment

Open PowerShell in VS Code:

```powershell
cd d:\Hacks-Projects\CIVISM-main\civisim\ml
python -m venv ml_venv_windows
.\ml_venv_windows\Scripts\Activate.ps1
```

### Step 3: Install All Packages

```powershell
pip install numpy pandas scikit-learn torch torchvision torchaudio transformers pdfplumber python-docx spacy matplotlib seaborn plotly
```

This should work without any build issues since Windows Python has pre-compiled wheels for all these packages.

### Step 4: Update VS Code Interpreter

1. `Ctrl+Shift+P` → `Python: Select Interpreter`
2. Select: `.\ml_venv_windows\Scripts\python.exe`
3. `Ctrl+Shift+P` → `Developer: Reload Window`

## Verify Installation

After packages are installed, run the test script:

```bash
# In MINGW64 terminal or PowerShell (depending on which Python you used)
cd /d/Hacks-Projects/CIVISM-main/civisim/ml  # MINGW64
# OR
cd d:\Hacks-Projects\CIVISM-main\civisim\ml  # PowerShell

python test_setup.py
```

You should see:
```
✓ All packages installed successfully!
✓ DistilBERT model loaded successfully
```

## Run the Demo

```bash
python quick_start.py
```

This will process a sample construction policy document and demonstrate:
- Task 1: Document text extraction (PDF/DOCX parsing)
- Task 2: Semantic intent extraction with DistilBERT

---

**Need Help?** If you're still experiencing issues, please provide:
1. Your Python version: `python --version`
2. Your pip version: `pip --version`
3. Your operating system
4. The full error message
