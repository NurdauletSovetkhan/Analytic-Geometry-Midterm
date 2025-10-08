"""
Line Analyzer GUI Application
=============================
Современный графический интерфейс для анализа отношений между линиями
Использует CustomTkinter для современного внешнего вида
"""

import customtkinter as ctk
from tkinter import messagebox
from typing import List, Dict, Any
from line_geometry import Line, analyze_all_lines
import sys
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class LineAnalyzerApp(ctk.CTk):
    """Главное окно приложения для анализа линий"""
    
    def __init__(self):
        super().__init__()
        
        # Настройка окна
        self.title("Line Relationship Analyzer")
        
        # Устанавливаем тему (dark/light)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Получаем размер экрана и устанавливаем окно на весь экран
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+0+0")
        
        # Переменные
        self.num_lines = 0
        self.line_entries: List[Dict[str, ctk.CTkEntry]] = []
        
        # Создаем интерфейс
        self.create_widgets()
    
    def center_window(self):
        """Центрирует окно на экране"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Создает все виджеты интерфейса"""
        
        # Заголовок
        title_label = ctk.CTkLabel(
            self,
            text="📐 Line Relationship Analyzer",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=15)
        
        subtitle_label = ctk.CTkLabel(
            self,
            text="Analyze relationships between lines in general form: Ax + By + C = 0",
            font=ctk.CTkFont(size=11)
        )
        subtitle_label.pack(pady=(0, 15))
        
        # Основной контейнер - две колонки
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Левая колонка (ввод данных)
        left_column = ctk.CTkFrame(main_container, fg_color="#E8E8E8", corner_radius=10)
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Правая колонка (график)
        right_column = ctk.CTkFrame(main_container, fg_color="#FFFFFF", corner_radius=10)
        right_column.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # === ЛЕВАЯ КОЛОНКА: Ввод данных ===
        
        # Секция ввода количества линий
        input_frame = ctk.CTkFrame(left_column, fg_color="transparent")
        input_frame.pack(fill="x", pady=15, padx=15)
        
        num_lines_label = ctk.CTkLabel(
            input_frame,
            text="Number of lines (n ≥ 2):",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        num_lines_label.pack(pady=(0, 10))
        
        input_container = ctk.CTkFrame(input_frame, fg_color="transparent")
        input_container.pack(pady=5)
        
        self.num_lines_entry = ctk.CTkEntry(
            input_container,
            width=80,
            placeholder_text="e.g., 3"
        )
        self.num_lines_entry.pack(side="left", padx=5)
        
        generate_button = ctk.CTkButton(
            input_container,
            text="Generate Input Fields",
            command=self.generate_line_inputs,
            width=150
        )
        generate_button.pack(side="left", padx=5)
        
        random_button = ctk.CTkButton(
            input_container,
            text="🎲 Random",
            command=self.fill_random_values,
            width=100,
            fg_color="#9B59B6",
            hover_color="#8E44AD"
        )
        random_button.pack(side="left", padx=5)
        
        # Секция полей ввода коэффициентов (с прокруткой)
        self.lines_frame = ctk.CTkScrollableFrame(left_column, fg_color="transparent", height=250)
        self.lines_frame.pack(fill="both", expand=True, pady=10, padx=15)
        
        # Кнопки действий
        actions_frame = ctk.CTkFrame(left_column, fg_color="transparent")
        actions_frame.pack(fill="x", pady=10, padx=15)
        
        analyze_button = ctk.CTkButton(
            actions_frame,
            text="🔍 Analyze Lines",
            command=self.analyze_lines,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=40,
            fg_color="#2CC985",
            hover_color="#25A56C"
        )
        analyze_button.pack(fill="x", pady=2)
        
        clear_button = ctk.CTkButton(
            actions_frame,
            text="🗑️ Clear",
            command=self.clear_all,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=40,
            fg_color="#E74C3C",
            hover_color="#C0392B"
        )
        clear_button.pack(fill="x", pady=2)
        
        visualize_button = ctk.CTkButton(
            actions_frame,
            text="📊 Visualize",
            command=self.visualize_lines,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=40,
            fg_color="#3498DB",
            hover_color="#2980B9"
        )
        visualize_button.pack(fill="x", pady=2)
        
        source_button = ctk.CTkButton(
            actions_frame,
            text="📄 View Source Code",
            command=self.view_source_code,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=40,
            fg_color="#95A5A6",
            hover_color="#7F8C8D"
        )
        source_button.pack(fill="x", pady=2)
        
        # Секция результатов
        results_label = ctk.CTkLabel(
            left_column,
            text="📊 Analysis Results",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        results_label.pack(pady=(10, 5), padx=15)
        
        self.results_text = ctk.CTkTextbox(
            left_column,
            height=500,
            font=ctk.CTkFont(family="Consolas", size=10)
        )
        self.results_text.pack(fill="both", expand=True, pady=(0, 15), padx=15)
        
        # Изначально отключаем текстовое поле для редактирования
        self.results_text.configure(state="disabled")
        
        # === ПРАВАЯ КОЛОНКА: График ===
        
        graph_title = ctk.CTkLabel(
            right_column,
            text="The Graph",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        graph_title.pack(pady=20)
        
        # Контейнер для графика
        self.graph_frame = ctk.CTkFrame(right_column, fg_color="#F5F5F5")
        self.graph_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Placeholder
        self.graph_placeholder = ctk.CTkLabel(
            self.graph_frame,
            text="Press 'Visualize' to display the graph",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.graph_placeholder.pack(expand=True)
        
        # Canvas для matplotlib (будет создан при визуализации)
        self.canvas_widget = None
        
        # Статус бар
        self.status_label = ctk.CTkLabel(
            self,
            text="Ready",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        self.status_label.pack(side="bottom", pady=5)
    
    def generate_line_inputs(self):
        """Генерирует поля ввода для коэффициентов линий"""
        try:
            # Получаем количество линий
            n = int(self.num_lines_entry.get())
            
            # Валидация
            if n < 2:
                messagebox.showerror(
                    "Invalid Input",
                    "Number of lines must be at least 2!\n\nPlease enter n ≥ 2."
                )
                return
            
            if n > 10:
                response = messagebox.askyesno(
                    "Large Number of Lines",
                    f"You entered {n} lines. This will create {n*(n-1)//2} pairs to analyze.\n\nContinue?"
                )
                if not response:
                    return
            
            # Очищаем предыдущие поля
            for widget in self.lines_frame.winfo_children():
                widget.destroy()
            self.line_entries.clear()
            
            # Заголовок
            header = ctk.CTkLabel(
                self.lines_frame,
                text="Enter coefficients for each line:",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            header.pack(pady=10)
            
            # Создаем поля для каждой линии
            for i in range(n):
                line_container = ctk.CTkFrame(self.lines_frame)
                line_container.pack(fill="x", pady=5, padx=10)
                
                # Метка линии
                line_label = ctk.CTkLabel(
                    line_container,
                    text=f"Line {i+1}:",
                    font=ctk.CTkFont(size=12, weight="bold"),
                    width=60
                )
                line_label.pack(side="left", padx=5)
                
                # Поле A
                a_label = ctk.CTkLabel(line_container, text="A:", width=20)
                a_label.pack(side="left", padx=2)
                a_entry = ctk.CTkEntry(line_container, width=80, placeholder_text="0")
                a_entry.pack(side="left", padx=5)
                
                # Поле B
                b_label = ctk.CTkLabel(line_container, text="B:", width=20)
                b_label.pack(side="left", padx=2)
                b_entry = ctk.CTkEntry(line_container, width=80, placeholder_text="0")
                b_entry.pack(side="left", padx=5)
                
                # Поле C
                c_label = ctk.CTkLabel(line_container, text="C:", width=20)
                c_label.pack(side="left", padx=2)
                c_entry = ctk.CTkEntry(line_container, width=80, placeholder_text="0")
                c_entry.pack(side="left", padx=5)
                
                # Уравнение
                equation_label = ctk.CTkLabel(
                    line_container,
                    text="→  Ax + By + C = 0",
                    font=ctk.CTkFont(size=10),
                    text_color="gray"
                )
                equation_label.pack(side="left", padx=10)
                
                # Сохраняем ссылки на поля
                self.line_entries.append({
                    'A': a_entry,
                    'B': b_entry,
                    'C': c_entry
                })
            
            self.num_lines = n
            self.update_status(f"Generated {n} input fields")
            
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter a valid integer for the number of lines."
            )
    
    def analyze_lines(self):
        """Анализирует все введенные линии"""
        if not self.line_entries:
            messagebox.showwarning(
                "No Lines",
                "Please generate input fields first!"
            )
            return
        
        try:
            # Собираем данные из полей ввода
            lines = []
            for i, entry_dict in enumerate(self.line_entries):
                try:
                    A = float(entry_dict['A'].get() or 0)
                    B = float(entry_dict['B'].get() or 0)
                    C = float(entry_dict['C'].get() or 0)
                    
                    line = Line(A, B, C)
                    lines.append(line)
                    
                except ValueError as e:
                    if "Invalid line" in str(e):
                        messagebox.showerror(
                            "Invalid Line",
                            f"Line {i+1} is invalid!\n\n"
                            f"Both A and B cannot be zero.\n"
                            f"A line must be well-defined: (A, B) ≠ (0, 0)"
                        )
                        return
                    else:
                        messagebox.showerror(
                            "Invalid Input",
                            f"Error in Line {i+1}:\n{str(e)}\n\n"
                            f"Please enter valid numbers for A, B, and C."
                        )
                        return
            
            # Анализируем все пары
            results = analyze_all_lines(lines)
            
            # Отображаем результаты
            self.display_results(results)
            self.update_status(f"Analyzed {len(lines)} lines, found {len(results)} pairs")
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"An error occurred during analysis:\n\n{str(e)}"
            )
    
    def display_results(self, results: List[Dict[str, Any]]):
        """Отображает результаты анализа с подробными шагами решения"""
        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", "end")
        
        # Заголовок
        header = "╔" + "═" * 78 + "╗\n"
        header += "║" + " " * 25 + "ANALYSIS RESULTS" + " " * 37 + "║\n"
        header += "╚" + "═" * 78 + "╝\n\n"
        self.results_text.insert("end", header)
        
        if not results:
            self.results_text.insert("end", "No line pairs to analyze.\n")
            self.results_text.configure(state="disabled")
            return
        
        # Выводим каждую пару
        for i, result in enumerate(results, 1):
            line1 = result['line1']
            line2 = result['line2']
            pair = result['pair']
            relation = result['relation']
            intersection = result['intersection']
            angle = result['angle']
            
            # Заголовок пары
            pair_header = f"┌─ Pair {i}: Line {pair[0]} and Line {pair[1]} " + "─" * (54 - len(str(i))) + "┐\n"
            self.results_text.insert("end", pair_header)
            
            # Уравнения линий
            self.results_text.insert("end", f"│\n")
            self.results_text.insert("end", f"│ Given lines:\n")
            self.results_text.insert("end", f"│   L{pair[0]}: {line1.A}x + {line1.B}y + {line1.C} = 0\n")
            self.results_text.insert("end", f"│   L{pair[1]}: {line2.A}x + {line2.B}y + {line2.C} = 0\n")
            self.results_text.insert("end", f"│\n")
            
            # ШАГ 1: Проверка пропорциональности
            self.results_text.insert("end", f"│ STEP 1: Check proportionality of coefficients\n")
            self.results_text.insert("end", f"│ ─────────────────────────────────────────────\n")
            
            A1, B1, C1 = line1.A, line1.B, line1.C
            A2, B2, C2 = line2.A, line2.B, line2.C
            
            # Вычисляем отношения коэффициентов
            self.results_text.insert("end", f"│   Check ratios:\n")
            if A2 != 0:
                self.results_text.insert("end", f"│     A₁/A₂ = {A1}/{A2} = {A1/A2:.4f}\n")
            else:
                self.results_text.insert("end", f"│     A₁/A₂ = {A1}/{A2} = ∞ (A₂=0)\n")
            
            if B2 != 0:
                self.results_text.insert("end", f"│     B₁/B₂ = {B1}/{B2} = {B1/B2:.4f}\n")
            else:
                self.results_text.insert("end", f"│     B₁/B₂ = {B1}/{B2} = ∞ (B₂=0)\n")
            
            if C2 != 0:
                self.results_text.insert("end", f"│     C₁/C₂ = {C1}/{C2} = {C1/C2:.4f}\n")
            else:
                self.results_text.insert("end", f"│     C₁/C₂ = {C1}/{C2} = ∞ (C₂=0)\n")
            
            self.results_text.insert("end", f"│\n")
            
            # ШАГ 2: Определение отношения
            self.results_text.insert("end", f"│ STEP 2: Determine relationship\n")
            self.results_text.insert("end", f"│ ─────────────────────────────────────────────\n")
            
            if relation == "coincident":
                self.results_text.insert("end", f"│   A₁/A₂ = B₁/B₂ = C₁/C₂  →  Lines COINCIDE\n")
                self.results_text.insert("end", f"│   ≡ The lines are identical (same line)\n")
            elif relation == "parallel":
                self.results_text.insert("end", f"│   A₁/A₂ = B₁/B₂ ≠ C₁/C₂  →  Lines are PARALLEL\n")
                self.results_text.insert("end", f"│   ║ The lines never intersect\n")
            else:  # intersect
                self.results_text.insert("end", f"│   A₁/A₂ ≠ B₁/B₂  →  Lines INTERSECT\n")
                self.results_text.insert("end", f"│   ✓ The lines meet at one point\n")
            
            self.results_text.insert("end", f"│\n")
            
            # ШАГ 3: Точка пересечения (если есть)
            if intersection:
                x, y = intersection
                self.results_text.insert("end", f"│ STEP 3: Find intersection point (Cramer's Rule)\n")
                self.results_text.insert("end", f"│ ─────────────────────────────────────────────\n")
                self.results_text.insert("end", f"│   System of equations:\n")
                self.results_text.insert("end", f"│     {A1}x + {B1}y = {-C1}\n")
                self.results_text.insert("end", f"│     {A2}x + {B2}y = {-C2}\n")
                self.results_text.insert("end", f"│\n")
                
                # Детерминанты
                det = A1 * B2 - A2 * B1
                det_x = (-C1) * B2 - (-C2) * B1
                det_y = A1 * (-C2) - A2 * (-C1)
                
                self.results_text.insert("end", f"│   Calculate determinants:\n")
                self.results_text.insert("end", f"│     D = │{A1:6.1f} {B1:6.1f}│ = {A1}×{B2} - {A2}×{B1} = {det:.4f}\n")
                self.results_text.insert("end", f"│         │{A2:6.1f} {B2:6.1f}│\n")
                self.results_text.insert("end", f"│\n")
                self.results_text.insert("end", f"│     Dₓ = │{-C1:6.1f} {B1:6.1f}│ = {det_x:.4f}\n")
                self.results_text.insert("end", f"│          │{-C2:6.1f} {B2:6.1f}│\n")
                self.results_text.insert("end", f"│\n")
                self.results_text.insert("end", f"│     Dᵧ = │{A1:6.1f} {-C1:6.1f}│ = {det_y:.4f}\n")
                self.results_text.insert("end", f"│          │{A2:6.1f} {-C2:6.1f}│\n")
                self.results_text.insert("end", f"│\n")
                self.results_text.insert("end", f"│   Solution:\n")
                self.results_text.insert("end", f"│     x = Dₓ/D = {det_x:.4f}/{det:.4f} = {x:.4f}\n")
                self.results_text.insert("end", f"│     y = Dᵧ/D = {det_y:.4f}/{det:.4f} = {y:.4f}\n")
                self.results_text.insert("end", f"│\n")
                self.results_text.insert("end", f"│   ★ Intersection point: P = ({x:.4f}, {y:.4f})\n")
                self.results_text.insert("end", f"│\n")
            
            # ШАГ 4: Угол между линиями (если есть)
            if angle is not None:
                self.results_text.insert("end", f"│ STEP 4: Calculate angle between lines\n")
                self.results_text.insert("end", f"│ ─────────────────────────────────────────────\n")
                
                # Вычисляем наклоны
                if line1.B != 0 and line2.B != 0:
                    m1 = -line1.A / line1.B
                    m2 = -line2.A / line2.B
                    self.results_text.insert("end", f"│   Slopes:\n")
                    self.results_text.insert("end", f"│     m₁ = -A₁/B₁ = -{A1}/{B1} = {m1:.4f}\n")
                    self.results_text.insert("end", f"│     m₂ = -A₂/B₂ = -{A2}/{B2} = {m2:.4f}\n")
                    self.results_text.insert("end", f"│\n")
                    
                    if abs(1 + m1 * m2) > 1e-10:
                        tan_theta = abs((m2 - m1) / (1 + m1 * m2))
                        self.results_text.insert("end", f"│   Angle formula:\n")
                        self.results_text.insert("end", f"│     tan(θ) = |m₂ - m₁| / |1 + m₁×m₂|\n")
                        self.results_text.insert("end", f"│     tan(θ) = |{m2:.4f} - {m1:.4f}| / |1 + {m1:.4f}×{m2:.4f}|\n")
                        self.results_text.insert("end", f"│     tan(θ) = {tan_theta:.4f}\n")
                        self.results_text.insert("end", f"│     θ = arctan({tan_theta:.4f}) = {angle:.2f}°\n")
                    else:
                        self.results_text.insert("end", f"│   Lines are perpendicular (m₁×m₂ = -1)\n")
                        self.results_text.insert("end", f"│     θ = 90.00°\n")
                else:
                    self.results_text.insert("end", f"│   One line is vertical (B = 0)\n")
                    self.results_text.insert("end", f"│     θ = {angle:.2f}°\n")
                
                self.results_text.insert("end", f"│\n")
                self.results_text.insert("end", f"│   ★ Angle: θ = {angle:.2f}°\n")
                self.results_text.insert("end", f"│\n")
            
            # Итоги для пары
            self.results_text.insert("end", f"│ CONCLUSION:\n")
            if relation == "intersect":
                self.results_text.insert("end", f"│   ✓ Lines intersect at ({intersection[0]:.4f}, {intersection[1]:.4f})\n")
                self.results_text.insert("end", f"│   ✓ Angle between lines: {angle:.2f}°\n")
            elif relation == "parallel":
                self.results_text.insert("end", f"│   ║ Lines are parallel and distinct\n")
            else:
                self.results_text.insert("end", f"│   ≡ Lines coincide (same line)\n")
            
            self.results_text.insert("end", f"└" + "─" * 78 + "┘\n\n")
        
        # Общая статистика
        summary = "╔" + "═" * 78 + "╗\n"
        summary += "║" + " " * 30 + "SUMMARY" + " " * 41 + "║\n"
        summary += "╚" + "═" * 78 + "╝\n"
        
        # Подсчет типов отношений
        intersect_count = sum(1 for r in results if r['relation'] == 'intersect')
        parallel_count = sum(1 for r in results if r['relation'] == 'parallel')
        coincident_count = sum(1 for r in results if r['relation'] == 'coincident')
        
        summary += f"\nTotal pairs analyzed: {len(results)}\n"
        summary += f"  ✓ Intersecting pairs: {intersect_count}\n"
        summary += f"  ║ Parallel pairs: {parallel_count}\n"
        summary += f"  ≡ Coincident pairs: {coincident_count}\n"
        
        self.results_text.insert("end", summary)
        
        self.results_text.configure(state="disabled")
    
    def visualize_lines(self):
        """Визуализирует линии на графике внутри приложения"""
        if not self.line_entries:
            messagebox.showwarning(
                "No Lines",
                "Please generate input fields first!"
            )
            return
        
        try:
            # Собираем линии
            lines = []
            for i, entry_dict in enumerate(self.line_entries):
                try:
                    A = float(entry_dict['A'].get() or 0)
                    B = float(entry_dict['B'].get() or 0)
                    C = float(entry_dict['C'].get() or 0)
                    
                    line = Line(A, B, C)
                    lines.append(line)
                    
                except ValueError as e:
                    if "Invalid line" in str(e):
                        messagebox.showerror(
                            "Invalid Line",
                            f"Line {i+1} is invalid!\n\n"
                            f"Both A and B cannot be zero."
                        )
                        return
                    else:
                        messagebox.showerror(
                            "Invalid Input",
                            f"Error in Line {i+1}. Please enter valid numbers."
                        )
                        return
            
            # Удаляем старый canvas если есть
            if self.canvas_widget:
                self.canvas_widget.get_tk_widget().destroy()
            
            # Скрываем placeholder
            self.graph_placeholder.pack_forget()
            
            # Создаем график
            fig, ax = plt.subplots(figsize=(6, 5), dpi=100)
            
            # Определяем диапазон для графика
            x_range = np.linspace(-10, 10, 400)
            
            # Цвета для линий
            colors = plt.cm.tab10(np.linspace(0, 1, len(lines)))
            
            # Рисуем каждую линию
            for idx, line in enumerate(lines):
                if line.B != 0:
                    # Обычная линия: y = -(A*x + C) / B
                    y = -(line.A * x_range + line.C) / line.B
                    ax.plot(x_range, y, label=f'Line {idx+1}: {line}', 
                           color=colors[idx], linewidth=2)
                else:
                    # Вертикальная линия: x = -C/A
                    x_val = -line.C / line.A
                    ax.axvline(x=x_val, label=f'Line {idx+1}: {line}', 
                              color=colors[idx], linewidth=2)
            
            # Находим и отмечаем точки пересечения
            from line_geometry import find_intersection, get_line_relation
            for i in range(len(lines)):
                for j in range(i+1, len(lines)):
                    relation = get_line_relation(lines[i], lines[j])
                    if relation == "intersect":
                        point = find_intersection(lines[i], lines[j])
                        if point:
                            x, y = point
                            # Проверяем что точка в видимом диапазоне
                            if -10 <= x <= 10 and -10 <= y <= 10:
                                ax.plot(x, y, 'ro', markersize=8, zorder=5)
                                ax.annotate(f'({x:.1f}, {y:.1f})', 
                                          xy=(x, y), xytext=(5, 5),
                                          textcoords='offset points',
                                          fontsize=8,
                                          bbox=dict(boxstyle='round,pad=0.3', 
                                                  facecolor='yellow', alpha=0.7))
            
            # Настройки графика
            ax.set_xlim(-10, 10)
            ax.set_ylim(-10, 10)
            ax.grid(True, alpha=0.3)
            ax.axhline(y=0, color='k', linewidth=0.5)
            ax.axvline(x=0, color='k', linewidth=0.5)
            ax.set_xlabel('X', fontsize=10)
            ax.set_ylabel('Y', fontsize=10)
            ax.set_title('Line Visualization', fontsize=12, fontweight='bold')
            ax.legend(loc='upper right', fontsize=8)
            
            # Встраиваем график в tkinter
            self.canvas_widget = FigureCanvasTkAgg(fig, master=self.graph_frame)
            self.canvas_widget.draw()
            self.canvas_widget.get_tk_widget().pack(fill="both", expand=True)
            
            self.update_status(f"Visualized {len(lines)} lines")
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"An error occurred during visualization:\n\n{str(e)}"
            )
    
    def clear_all(self):
        """Очищает все поля и результаты"""
        # Очищаем поля ввода
        for entry_dict in self.line_entries:
            entry_dict['A'].delete(0, 'end')
            entry_dict['B'].delete(0, 'end')
            entry_dict['C'].delete(0, 'end')
        
        # Очищаем результаты
        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", "end")
        self.results_text.configure(state="disabled")
        
        self.update_status("Cleared all inputs and results")
    
    def fill_random_values(self):
        """Заполняет пустые поля случайными значениями"""
        if not self.line_entries:
            messagebox.showwarning(
                "No Input Fields",
                "Please generate input fields first!"
            )
            return
        
        filled_count = 0
        
        for entry_dict in self.line_entries:
            # Заполняем A если пусто
            if not entry_dict['A'].get():
                entry_dict['A'].delete(0, 'end')
                entry_dict['A'].insert(0, str(random.randint(-10, 10)))
                filled_count += 1
            
            # Заполняем B если пусто
            if not entry_dict['B'].get():
                entry_dict['B'].delete(0, 'end')
                entry_dict['B'].insert(0, str(random.randint(-10, 10)))
                filled_count += 1
            
            # Заполняем C если пусто
            if not entry_dict['C'].get():
                entry_dict['C'].delete(0, 'end')
                entry_dict['C'].insert(0, str(random.randint(-10, 10)))
                filled_count += 1
        
        if filled_count > 0:
            self.update_status(f"Filled {filled_count} empty fields with random values")
        else:
            self.update_status("All fields are already filled")
    
    def view_source_code(self):
        """Открывает окно с информацией об исходном коде"""
        import os
        import webbrowser
        
        # Получаем путь к текущему файлу
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Создаем информационное окно
        info_window = ctk.CTkToplevel(self)
        info_window.title("Source Code Information")
        info_window.geometry("600x400")
        info_window.transient(self)
        info_window.grab_set()
        
        # Заголовок
        title_label = ctk.CTkLabel(
            info_window,
            text="📄 Source Code Information",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Информация
        info_text = ctk.CTkTextbox(
            info_window,
            font=ctk.CTkFont(family="Consolas", size=11),
            wrap="word"
        )
        info_text.pack(fill="both", expand=True, padx=20, pady=10)
        
        info_content = f"""
╔══════════════════════════════════════════════════════════╗
║             LINE ANALYZER - SOURCE CODE INFO            ║
╚══════════════════════════════════════════════════════════╝

Project: Analytic Geometry - Line Relationship Analyzer
Author: Nurdaulet Sovetkhan
Course: Analytic Geometry, Astana IT University
Date: October 2025

═══════════════════════════════════════════════════════════

📁 PROJECT STRUCTURE:

Main Modules:
  • main.py           - Application entry point
  • gui_app.py        - GUI interface (CustomTkinter)
  • line_geometry.py  - Mathematical engine
  • test_line_geometry.py - Unit tests (25 tests)

Build & Documentation:
  • build_exe.py      - PyInstaller build script
  • requirements.txt  - Dependencies
  • README.md         - Full documentation
  • PROJECT_SUMMARY.md - Project report

═══════════════════════════════════════════════════════════

🔧 TECHNOLOGY STACK:

• Python 3.12
• CustomTkinter 5.2.0+ (Modern GUI)
• Matplotlib 3.7.0+ (Visualization)
• NumPy 1.24.0+ (Numerical computations)
• PyInstaller 6.0.0+ (Executable builder)

═══════════════════════════════════════════════════════════

📂 SOURCE CODE LOCATION:

{current_dir}

═══════════════════════════════════════════════════════════

🌐 GITHUB REPOSITORY:

Repository: Analytic-Geometry-Midterm
Owner: NurdauletSovetkhan
Link: github.com/NurdauletSovetkhan/Analytic-Geometry-Midterm

═══════════════════════════════════════════════════════════

📊 STATISTICS:

• Total Lines of Code: ~2000+
• Number of Functions: 30+
• Files: 7 main modules

═══════════════════════════════════════════════════════════
"""
        
        info_text.insert("1.0", info_content)
        info_text.configure(state="disabled")
        
        # Кнопки
        buttons_frame = ctk.CTkFrame(info_window, fg_color="transparent")
        buttons_frame.pack(pady=10)
        
        def open_folder():
            try:
                if sys.platform == 'win32':
                    os.startfile(current_dir)
                elif sys.platform == 'darwin':  # macOS
                    os.system(f'open "{current_dir}"')
                else:  # Linux
                    os.system(f'xdg-open "{current_dir}"')
                self.update_status("Opened source code folder")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open folder:\n{e}")
        
        def open_github():
            try:
                webbrowser.open("https://github.com/NurdauletSovetkhan/Analytic-Geometry-Midterm")
                self.update_status("Opened GitHub repository")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open browser:\n{e}")
        
        folder_btn = ctk.CTkButton(
            buttons_frame,
            text="📁 Open Source Folder",
            command=open_folder,
            width=180
        )
        folder_btn.pack(side="left", padx=5)
        
        github_btn = ctk.CTkButton(
            buttons_frame,
            text="🌐 Open GitHub Repo",
            command=open_github,
            width=180,
            fg_color="#24292e"
        )
        github_btn.pack(side="left", padx=5)
        
        close_btn = ctk.CTkButton(
            buttons_frame,
            text="Close",
            command=info_window.destroy,
            width=100,
            fg_color="#E74C3C"
        )
        close_btn.pack(side="left", padx=5)
    
    def update_status(self, message: str):
        """Обновляет статус бар"""
        self.status_label.configure(text=message)


def main():
    """Точка входа в GUI приложение"""
    app = LineAnalyzerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
