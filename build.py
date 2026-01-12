import PyInstaller.__main__
import os
import shutil

if os.path.exists('build'):
    shutil.rmtree('build')
if os.path.exists('dist'):
    shutil.rmtree('dist')

PyInstaller.__main__.run([
    'main.py',                          # Основной файл
    '--name=ParCom_System',             # Имя executable
    '--windowed',                       # Без консоли (GUI app)
    '--onefile',                        # Один файл
    '--icon=NONE',                      # Можно добавить иконку позже
    '--add-data=theme.py:.',            # Добавляем theme.py
    '--hidden-import=customtkinter',    # Явно указываем зависимости
    '--hidden-import=PIL._tkinter_finder',
    '--collect-all=customtkinter',      # Собираем все файлы customtkinter
    '--noconfirm',                      # Не спрашивать подтверждение
])

print("\n✅ Build completed! Executable: dist/ParCom_System.exe")
