import PyInstaller.__main__
import os
import shutil
import sys

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

if os.path.exists('build'):
    shutil.rmtree('build')
if os.path.exists('dist'):
    shutil.rmtree('dist')

print("Starting build process...")

PyInstaller.__main__.run([
    'main.py',                          # Main file
    '--name=ParCom_System',             # Executable name
    '--windowed',                       # No console (GUI app)
    '--onefile',                        # Single file
    '--icon=NONE',                      # Can add icon later
    '--add-data=theme.py:.',            # Add theme.py
    '--hidden-import=customtkinter',    # Explicitly specify dependencies
    '--hidden-import=PIL._tkinter_finder',
    '--collect-all=customtkinter',      # Collect all customtkinter files
    '--noconfirm',                      # Don't ask for confirmation
])

print("\n[SUCCESS] Build completed! Executable: dist/ParCom_System.exe")
