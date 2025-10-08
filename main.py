"""
Line Analyzer - Main Entry Point
================================
Аналитическая геометрия: Анализ отношений между линиями

Программа анализирует отношения между линиями в общем виде:
    Ax + By + C = 0

Для каждой пары линий определяет:
    - Пересекаются ли они (и находит точку пересечения)
    - Параллельны ли (но различны)
    - Совпадают ли
    - Если пересекаются - вычисляет угол между ними

Author: Analytic Geometry Team
Date: October 2025
"""

import sys
from gui_app import main as gui_main


def print_banner():
    """Выводит баннер приложения"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║              📐 LINE RELATIONSHIP ANALYZER 📐                ║
    ║                                                              ║
    ║                   Analytic Geometry Tool                     ║
    ║                                                              ║
    ║         Analyze relationships between lines in the plane     ║
    ║                  Ax + By + C = 0                            ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    
    Features:
    ✓ Determine line relationships (intersect/parallel/coincident)
    ✓ Calculate intersection points
    ✓ Compute angles between lines
    ✓ Visualize lines graphically
    ✓ Modern GUI with CustomTkinter
    
    Starting GUI application...
    """
    print(banner)


if __name__ == "__main__":
    print_banner()
    
    try:
        # Запускаем GUI приложение
        gui_main()
    except KeyboardInterrupt:
        print("\n\nApplication terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError: {e}")
        print("\nPlease make sure all dependencies are installed:")
        print("  pip install customtkinter matplotlib pillow")
        sys.exit(1)
