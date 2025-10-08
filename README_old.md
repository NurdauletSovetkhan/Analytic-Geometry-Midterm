# 📐 Line Relationship Analyzer

> A modern, interactive tool for analyzing geometric relationships between lines in 2D space

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GUI: CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-green.svg)](https://github.com/TomSchimansky/CustomTkinter)

**Created for Analytic Geometry Course**  
Astana IT University | October 2025

---

## 🎯 What Does This Tool Do?

Ever wondered whether two lines intersect, run parallel, or are actually the same line? This application does exactly that! 

Given lines in the general form `Ax + By + C = 0`, the analyzer will:
- 🔍 Determine if they **intersect**, are **parallel**, or **coincide**
- 📍 Calculate exact **intersection points** (when applicable)
- 📐 Measure the **angle** between intersecting lines
- 📊 Show a beautiful **visual graph** of your lines

Perfect for students, teachers, and anyone working with linear equations!

---

## ✨ Features

### Core Functionality
- ✅ **Relationship Detection**: Instantly identifies whether lines intersect, are parallel, or coincide
- ✅ **Intersection Points**: Calculates exact coordinates using Cramer's Rule
- ✅ **Angle Calculation**: Measures angles between lines (0° to 90°)
- ✅ **Special Cases**: Handles vertical lines (B = 0) and horizontal lines (A = 0)

### User Experience
- 🎨 **Modern GUI**: Built with CustomTkinter for a sleek, professional look
- 📊 **Live Visualization**: See your lines plotted in real-time with matplotlib
- 🎲 **Random Generation**: Quickly fill coefficients with random values for testing
- 📝 **Detailed Steps**: View complete mathematical solutions with step-by-step breakdowns
- 🌐 **Source Code Access**: Built-in button to view project source and documentation

### Developer Friendly
- 🧪 **25 Unit Tests**: Comprehensive test coverage ensures accuracy
- 📦 **One-Click Build**: Create standalone `.exe` files with PyInstaller
- 🔧 **Well Documented**: Clear code comments and full documentation

---

## 🚀 Quick Start

### Option 1: Run from Source (Recommended for Development)

**1. Install Dependencies:**
```bash
pip install -r requirements.txt
   ```

2. Найдите готовый файл:
   ```
   dist/LineAnalyzer.exe
   ```

3. Просто двойным кликом запустите `LineAnalyzer.exe`

---

## 📖 Инструкция по использованию

### Шаг 1: Введите количество линий
- Минимум 2 линии
- Программа проанализирует все пары

### Шаг 2: Введите коэффициенты
Для каждой линии введите три коэффициента A, B, C:
- **A** - коэффициент при x
- **B** - коэффициент при y  
- **C** - свободный член

**Важно:** Хотя бы один из коэффициентов A или B должен быть ненулевым!

### Шаг 3: Анализ
Нажмите кнопку **"Analyze Lines"** для получения результатов:
- Тип отношения для каждой пары
- Точки пересечения (если есть)
- Углы между линиями (в градусах)

### Шаг 4: Визуализация (опционально)
Нажмите **"Visualize"** для графического отображения линий и точек пересечения.

---

## 💡 Примеры использования

### Пример 1: Три пересекающиеся линии

```
Количество линий: 3

Line 1: A=1, B=1, C=-2     →  x + y - 2 = 0
Line 2: A=1, B=-1, C=0     →  x - y = 0
Line 3: A=2, B=-3, C=5     →  2x - 3y + 5 = 0
```

**Результат:**
- L1 и L2: Пересекаются в точке (1, 1), угол = 90°
- L1 и L3: Пересекаются
- L2 и L3: Пересекаются

### Пример 2: Параллельные линии

```
Количество линий: 2

Line 1: A=1, B=1, C=-2     →  x + y = 2
Line 2: A=1, B=1, C=-4     →  x + y = 4
```

**Результат:**
- L1 и L2: Параллельны (не пересекаются)

### Пример 3: Вертикальная и горизонтальная линии

```
Количество линий: 2

Line 1: A=1, B=0, C=-3     →  x = 3 (вертикальная)
Line 2: A=0, B=1, C=-2     →  y = 2 (горизонтальная)
```

**Результат:**
- L1 и L2: Пересекаются в точке (3, 2), угол = 90°

---

## 🏗️ Структура проекта

```
Midterm/
├── line_geometry.py      # Математические вычисления
├── gui_app.py           # GUI интерфейс (CustomTkinter)
├── visualization.py     # Визуализация (Matplotlib)
├── main.py             # Точка входа приложения
├── test_line_geometry.py # Unit-тесты (25 тестов)
├── build_exe.py        # Скрипт сборки .exe
└── README.md           # Эта документация
```

---

## 🛠️ Технический стек

### Backend (Вычисления)
- **Python 3.8+** - основной язык
- **math** - математические функции
- **numpy** - численные вычисления

### Frontend (GUI)
- **CustomTkinter** - современный UI фреймворк
- **tkinter** - базовая библиотека GUI

### Визуализация
- **Matplotlib** - графики и визуализации
- **Pillow (PIL)** - обработка изображений

### Сборка
- **PyInstaller** - создание standalone .exe

---

## 🧮 Математические формулы

### 1. Наклон линии
Для линии `Ax + By + C = 0`:
```
m = -A/B  (если B ≠ 0)
```
Вертикальные линии (B = 0) имеют бесконечный наклон.

### 2. Определение отношения

**Совпадение:** Коэффициенты пропорциональны
```
A1/A2 = B1/B2 = C1/C2
```

**Параллельность:** Направления пропорциональны, но C нет
```
A1/A2 = B1/B2 ≠ C1/C2
```

**Пересечение:** Направления не пропорциональны
```
A1*B2 ≠ A2*B1
```

### 3. Точка пересечения (Правило Крамера)

Для системы:
```
A1*x + B1*y + C1 = 0
A2*x + B2*y + C2 = 0
```

Решение:
```
x = (B1*C2 - B2*C1) / (A1*B2 - A2*B1)
y = (A2*C1 - A1*C2) / (A1*B2 - A2*B1)
```

### 4. Угол между линиями

Для линий с наклонами m₁ и m₂:
```
tan(θ) = |m₂ - m₁| / (1 + m₁*m₂)
```

Результат всегда в диапазоне [0°, 90°].

---

## ✅ Тестирование

Проект включает 25 unit-тестов для проверки всех математических функций.

**Запуск тестов:**
```bash
python test_line_geometry.py
```

**Покрытие тестами:**
- ✅ Валидация линий
- ✅ Вертикальные/горизонтальные линии
- ✅ Пересечения
- ✅ Параллельность
- ✅ Совпадение
- ✅ Углы (45°, 90°, острые)
- ✅ Примеры из задания

---

## 📦 Сборка .exe файла

### Требования
- Python 3.8+
- PyInstaller (устанавливается автоматически)

### Процесс сборки

1. **Запустите скрипт сборки:**
   ```bash
   python build_exe.py
   ```

2. **Дождитесь завершения** (обычно 1-2 минуты)

3. **Найдите готовый .exe:**
   ```
   dist/LineAnalyzer.exe
   ```

### Что входит в .exe?
- ✅ Все необходимые библиотеки
- ✅ Python runtime
- ✅ Графические ресурсы
- ✅ Все зависимости

**Размер:** ~50-70 MB (полностью автономный)

### Распространение
Готовый `.exe` файл можно:
- Отправить по email
- Загрузить на облако (Google Drive, OneDrive)
- Скопировать на USB
- **Не требует установки Python у конечного пользователя!**

---

## 🎨 Интерфейс

### Основные элементы

1. **Поле ввода количества линий** - сверху
2. **Динамические поля коэффициентов** - появляются после генерации
3. **Кнопки действий:**
   - 🔍 **Analyze** - выполнить анализ
   - 🗑️ **Clear** - очистить все поля
   - 📊 **Visualize** - показать график
4. **Область результатов** - снизу (с прокруткой)

### Темы оформления
- 🌙 **Dark Mode** (по умолчанию)
- ☀️ **Light Mode** (можно изменить в коде)

---

## ⚠️ Известные ограничения

1. **Количество линий:** Рекомендуется не более 10 линий одновременно
   - Причина: n линий создают n*(n-1)/2 пар для анализа
   - 10 линий = 45 пар

2. **Очень большие числа:** Могут быть проблемы с отображением
   - Решение: используйте разумные значения коэффициентов

3. **Точность:** Используется tolerance = 1e-10 для сравнения чисел
   - Учитывается погрешность вычислений с плавающей точкой

---

## 🐛 Устранение неполадок

### Проблема: Приложение не запускается

**Решение:**
1. Проверьте установку зависимостей:
   ```bash
   pip install customtkinter matplotlib pillow
   ```
2. Убедитесь, что используете Python 3.8+:
   ```bash
   python --version
   ```

### Проблема: "Invalid line" ошибка

**Причина:** Оба коэффициента A и B равны нулю

**Решение:** Убедитесь, что хотя бы один из A или B ненулевой

### Проблема: Визуализация не открывается

**Решение:**
1. Убедитесь, что matplotlib установлен:
   ```bash
   pip install matplotlib
   ```
2. Попробуйте закрыть другие окна matplotlib

### Проблема: .exe не собирается

**Решение:**
1. Установите PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Убедитесь в наличии свободного места (>500 MB)
3. Отключите антивирус временно

---

## 📝 Задание (из PDF)

### Формулировка задачи

Рассматриваются линии в плоскости в общем виде:
```
li : Aix + Biy + Ci = 0,    Ai, Bi, Ci ∈ ℝ
```

### Требования

Написать программу на Python, которая:

1. Запрашивает у пользователя:
   - Целое число n ≥ 2 (количество линий)
   - Для каждой линии: коэффициенты Ai, Bi, Ci

2. Для каждой **упорядоченной пары** (li, lj) где i ≠ j:
   - Определяет тип отношения:
     - **Пересекаются** (intersect)
     - **Параллельны, но различны** (parallel)
     - **Совпадают** (coincident)
   
   - Если пересекаются:
     - Вычисляет точку пересечения (x, y)
     - Если не перпендикулярны: вычисляет угол в градусах

### Реализация

✅ **Все требования выполнены!**
- GUI для ввода данных
- Валидация входных данных
- Анализ всех пар
- Вычисление точек и углов
- Визуализация (бонус)

---

## 👨‍💻 Разработка

### Установка для разработки

```bash
# Клонируйте репозиторий
git clone <repository-url>
cd Midterm

# Установите зависимости
pip install -r requirements.txt
```

### Создание requirements.txt

```bash
pip freeze > requirements.txt
```

### Структура кода

- **Модульность:** Каждый модуль отвечает за свою функцию
- **Типизация:** Используются type hints
- **Документация:** Все функции документированы
- **Тесты:** Полное покрытие тестами

---

## 📄 Лицензия

Этот проект создан в учебных целях для курса Аналитической Геометрии.

---

## 🙏 Благодарности

- **CustomTkinter** - за современный UI framework
- **Matplotlib** - за отличную библиотеку визуализации
- **Python Community** - за поддержку и инструменты

---

## 📞 Поддержка

Если у вас возникли вопросы или проблемы:

1. Проверьте раздел "Устранение неполадок"
2. Убедитесь, что все зависимости установлены
3. Проверьте формат входных данных
4. Свяжитесь с преподавателем

---

**Разработано с ❤️ для Analytic Geometry Course**  
**Astana IT University, October 2025**
