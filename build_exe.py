"""
Build Script for Line Analyzer
==============================
Скрипт для сборки standalone .exe файла с помощью PyInstaller

Использование:
    python build_exe.py

Результат:
    - dist/LineAnalyzer.exe - готовый к распространению .exe файл
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def check_pyinstaller():
    """Проверяет наличие PyInstaller"""
    try:
        import PyInstaller.__main__  
        return True
    except ImportError:
    # Автоматически установит PyInstaller
        print("✗ PyInstaller not found")
        print("\nInstalling PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✓ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("✗ Failed to install PyInstaller")
            return False


def clean_build_folders():
    """Очищает папки сборки"""
    folders_to_clean = ['build', 'dist', '__pycache__']
    
    for folder in folders_to_clean:
        if os.path.exists(folder):
            print(f"Cleaning {folder}/...")
            shutil.rmtree(folder, ignore_errors=True)
    
    # Удаляем .spec файлы
    for spec_file in Path('.').glob('*.spec'):
        print(f"Removing {spec_file}...")
        spec_file.unlink()
    
    print("✓ Build folders cleaned")


def build_exe():
    """Собирает .exe файл"""
    print("\n" + "="*60)
    print("Building Line Analyzer executable...")
    print("="*60 + "\n")
    
    # Параметры PyInstaller
    params = [
        sys.executable,                 # Используем текущий Python
        '-m', 'PyInstaller',            # Запускаем PyInstaller как модуль
        '--onefile',                    # Один файл
        '--windowed',                   # Без консоли (для GUI)
        '--name=LineAnalyzer',          # Имя выходного файла
        '--icon=NONE',                  # Иконка (можно добавить свою)
        '--add-data=line_geometry.py;.',  # Добавляем модули
        '--add-data=gui_app.py;.',
        '--hidden-import=customtkinter',
        '--hidden-import=matplotlib',
        '--hidden-import=PIL',
        '--hidden-import=numpy',
        '--clean',                      # Очистить кэш
        'main.py'                       # Главный файл
    ]
    
    print("Running PyInstaller with parameters:")
    print(" ".join(params))
    print()
    
    try:
        result = subprocess.run(params, check=True, capture_output=False)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed with error code {e.returncode}")
        return False
    except Exception as e:
        print(f"\n✗ Build failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def create_readme_for_dist():
    """Создает README для папки dist"""
    readme_content = """
LINE ANALYZER - USER GUIDE
===========================

Thank you for using Line Analyzer!

WHAT IS THIS?
-------------
Line Analyzer is a tool for analyzing relationships between lines 
in the plane. It helps you determine if lines intersect, are parallel, 
or coincide, and calculates intersection points and angles.

HOW TO USE:
-----------
1. Double-click LineAnalyzer.exe to start the application
2. Enter the number of lines you want to analyze (minimum 2)
3. Click "Generate Input Fields"
4. Enter coefficients A, B, C for each line (Ax + By + C = 0)
5. Click "Analyze Lines" to see results
6. Click "Visualize" to see a graphical representation

REQUIREMENTS:
-------------
- Windows 7 or later
- No additional software needed - everything is included!

FEATURES:
---------
✓ Modern, user-friendly interface
✓ Accurate mathematical calculations
✓ Visual representation of lines
✓ Support for vertical and horizontal lines
✓ Detailed analysis reports

TROUBLESHOOTING:
----------------
If the application doesn't start:
- Make sure your antivirus hasn't blocked it
- Try running as administrator
- Check that you have enough RAM (minimum 500 MB free)

For more information or support, contact your instructor.

Developed for Analytic Geometry Course
October 2025
"""
    
    dist_path = Path('dist')
    if dist_path.exists():
        readme_path = dist_path / 'README.txt'
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"✓ Created {readme_path}")


def main():
    """Главная функция сборки"""
    print("\n" + "╔" + "═"*58 + "╗")
    print("║" + " "*15 + "LINE ANALYZER BUILD SCRIPT" + " "*16 + "║")
    print("╚" + "═"*58 + "╝\n")
    
    # Проверяем PyInstaller
    if not check_pyinstaller():
        print("\n✗ Cannot proceed without PyInstaller")
        return False
    
    # Очищаем старые файлы сборки
    print("\nCleaning old build files...")
    clean_build_folders()
    
    # Собираем .exe
    print("\nBuilding executable...")
    if build_exe():
        print("\n" + "="*60)
        print("✓ BUILD SUCCESSFUL!")
        print("="*60)
        print("\nYour executable is ready:")
        print("  📁 dist/LineAnalyzer.exe")
        print("\nYou can distribute this file to users.")
        print("They can simply double-click it to run the application.")
        
        # Создаем README
        create_readme_for_dist()
        
        # Показываем размер файла
        exe_path = Path('dist/LineAnalyzer.exe')
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"\nFile size: {size_mb:.2f} MB")
        
        return True
    else:
        print("\n" + "="*60)
        print("✗ BUILD FAILED")
        print("="*60)
        print("\nPlease check the error messages above.")
        print("Common issues:")
        print("  - Missing dependencies (install with pip)")
        print("  - Syntax errors in Python files")
        print("  - Insufficient disk space")
        return False


if __name__ == "__main__":
    try:
        success = main()
        
        if success:
            print("\n✓ All done! Press Enter to exit...")
            input()
            sys.exit(0)
        else:
            print("\n✗ Build failed. Press Enter to exit...")
            input()
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n✗ Build cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        print("\nPress Enter to exit...")
        input()
        sys.exit(1)
