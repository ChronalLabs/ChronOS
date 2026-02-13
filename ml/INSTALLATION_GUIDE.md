# ML Setup Installation Guide

## Issue: Package Installation in MSYS2/MinGW64 Environment

The Python environment detected is MSYS2 Python which has build issues with numpy and other packages when using pip in PowerShell.

## Solutions

### Option 1: Use MSYS2 MinGW Terminal (Recommended)

1. Open **MSYS2 MinGW64** terminal (not PowerShell)
2. Navigate to the ML folder:
   ```bash
   cd /d/Hacks-Projects/CIVISM-main/civisim/ml
   ```

3. Create virtual environment:
   ```bash
   python -m venv ml_venv
   ```

4. Activate the virtual environment:
   ```bash
   source ml_venv/bin/activate
   ```

5. Install packages using pacman (system-wide, easier):
   ```bash
   pacman -S mingw-w64-ucrt-x86_64-python-numpy \
             mingw-w64-ucrt-x86_64-python-pandas \
             mingw-w64-ucrt-x86_64-python-scikit-learn \
             mingw-w64-ucrt-x86_64-python-pytorch-cpu \
             mingw-w64-ucrt-x86_64-python-pip
   ```

6. Then install remaining packages with pip:
   ```bash
   pip install transformers pdfplumber python-docx spacy matplotlib seaborn plotly
   ```

### Option 2: Install Windows Native Python

1. Download Python 3.11 or 3.12 from https://www.python.org/downloads/
2. During installation, check "Add Python to PATH"
3. Open new PowerShell terminal
4. Navigate to ML folder:
   ```powershell
   cd d:\Hacks-Projects\CIVISM-main\civisim\ml
   ```

5. Create virtual environment with Windows Python:
   ```powershell
   python -m venv ml_venv_win
   ```

6. Activate virtual environment:
   ```powershell
   .\ml_venv_win\Scripts\Activate.ps1
   ```

7. Install all packages:
   ```powershell
   pip install numpy pandas scikit-learn torch torchvision torchaudio transformers pdfplumber python-docx spacy matplotlib seaborn plotly
   ```

### Option 3: Use Conda/Anaconda

1. Install Miniconda from https://docs.conda.io/en/latest/miniconda.html
2. Create conda environment:
   ```powershell
   conda create -n civisim_ml python=3.11
   conda activate civisim_ml
   ```

3. Install packages:
   ```powershell
   conda install numpy pandas scikit-learn pytorch torchvision torchaudio cpuonly -c pytorch
   pip install transformers pdfplumber python-docx spacy matplotlib seaborn plotly
   ```

## Verify Installation

After successful installation, run:

```bash
cd d:/Hacks-Projects/CIVISM-main/civisim/ml
python test_setup.py
```

## Quick Start Demo

Once packages are installed:

```bash
python quick_start.py
```

This will run Tasks 1 and 2 (Document Parser + Intent Extractor) on a sample policy document.

## Pylance Import Errors

After installing packages, VS Code's Pylance may still show import errors. To fix:

1. **Select Python Interpreter**: Press `Ctrl+Shift+P`, type "Python: Select Interpreter"
2. Choose the interpreter from your virtual environment:
   - For MSYS2 venv: `ml_venv/bin/python`
   - For Windows venv: `ml_venv_win/Scripts/python.exe`
   - For conda: `civisim_ml` environment

3. **Reload Window**: Press `Ctrl+Shift+P`, type "Developer: Reload Window"

The import errors should disappear once Pylance recognizes the correct Python environment with installed packages.
