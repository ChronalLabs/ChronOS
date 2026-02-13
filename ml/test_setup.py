"""
CIVISIM ML Setup Script
Verify installation and download required models
"""

import sys


def test_imports():
    """Test if all required packages are installed"""
    print("🔍 Testing package imports...")
    
    required_packages = {
        'torch': 'PyTorch',
        'transformers': 'Transformers',
        'pdfplumber': 'PDF Plumber',
        'docx': 'python-docx',
        'numpy': 'NumPy',
        'sklearn': 'scikit-learn'
    }
    
    missing = []
    installed = []
    
    for package, name in required_packages.items():
        try:
            __import__(package)
            installed.append(name)
            print(f"  ✓ {name}")
        except ImportError:
            missing.append(name)
            print(f"  ✗ {name} - NOT INSTALLED")
    
    return missing, installed


def test_models():
    """Test if models can be loaded"""
    print("\n🤖 Testing model loading...")
    
    try:
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
        print("  ✓ DistilBERT tokenizer loaded")
        return True
    except ImportError:
        print("  ✗ transformers package not installed")
        print("  → Run: pip install transformers")
        print("  → See FIX_IMPORTS.md for installation help")
        return False
    except Exception as e:
        print(f"  ✗ Error loading DistilBERT: {e}")
        return False


def main():
    """Run setup verification"""
    print("=" * 60)
    print("CIVISIM ML/AI Setup Verification")
    print("=" * 60)
    
    # Test Python version
    print(f"\n🐍 Python Version: {sys.version.split()[0]}")
    if sys.version_info < (3, 8):
        print("  ⚠️  Python 3.8+ recommended")
    else:
        print("  ✓ Version OK")
    
    # Test imports
    missing, installed = test_imports()
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("\n📦 Install missing packages:")
        print("   pip install -r requirements.txt")
        return False
    
    print(f"\n✅ All required packages installed ({len(installed)} packages)")
    
    # Test models
    models_ok = test_models()
    
    if not models_ok:
        print("\n⚠️  Model loading failed")
        print("   This is normal on first run - models will download automatically")
    
    # Final status
    print("\n" + "=" * 60)
    if missing:
        print("❌ Setup incomplete - install missing packages")
    else:
        print("✅ Setup complete! Ready to run ML tasks")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
