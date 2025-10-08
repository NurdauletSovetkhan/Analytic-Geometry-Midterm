# Line Relationship Analyzer

> A modern, interactive tool for analyzing geometric relationships between lines in 2D space

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GUI: CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-green.svg)](https://github.com/TomSchimansky/CustomTkinter)

**Created for Analytic Geometry Course**  
Astana IT University | October 2025

---

## What Does This Tool Do?

Ever wondered whether two lines intersect, run parallel, or are actually the same line? This application does exactly that! 

Given lines in the general form `Ax + By + C = 0`, the analyzer will:
-  Determine if they **intersect**, are **parallel**, or **coincide**
-  Calculate exact **intersection points** (when applicable)
-  Measure the **angle** between intersecting lines
-  Show a beautiful **visual graph** of your lines

Perfect for students, teachers, and anyone working with linear equations!

---

## Features

### Core Functionality
-  **Relationship Detection**: Instantly identifies whether lines intersect, are parallel, or coincide
-  **Intersection Points**: Calculates exact coordinates using Cramer's Rule
-  **Angle Calculation**: Measures angles between lines (0° to 90°)
-  **Special Cases**: Handles vertical lines (B = 0) and horizontal lines (A = 0)

### User Experience
-  **Modern GUI**: Built with CustomTkinter for a sleek, professional look
-  **Live Visualization**: See your lines plotted in real-time with matplotlib
-  **Random Generation**: Quickly fill coefficients with random values for testing
-  **Detailed Steps**: View complete mathematical solutions with step-by-step breakdowns
-  **Source Code Access**: Built-in button to view project source and documentation

### Developer Friendly
-  **25 Unit Tests**: Comprehensive test coverage ensures accuracy
-  **One-Click Build**: Create standalone `.exe` files with PyInstaller
-  **Well Documented**: Clear code comments and full documentation

---

## Quick Start

### Option 1: Run from Source (Recommended for Developers)

**1. Clone the repository:**
```bash
git clone https://github.com/NurdauletSovetkhan/Analytic-Geometry-Midterm.git
cd Analytic-Geometry-Midterm
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Launch the application:**
```bash
python main.py
```

That's it! The GUI will open and you're ready to analyze lines. 🎉

### Option 2: Use Standalone Executable (For End Users)

**1. Build the .exe file:**
```bash
python build_exe.py
```

**2. Find your executable:**
```
dist/LineAnalyzer.exe
```

**3. Double-click to run!**

No Python installation required for end users. Just distribute the `.exe` file.

---

## How to Use

### Step 1: Enter Number of Lines
- Minimum: 2 lines
- The program will analyze all possible pairs

### Step 2: Enter Coefficients
For each line, provide three coefficients `A`, `B`, `C` where:
- **A** - coefficient of x
- **B** - coefficient of y
- **C** - constant term

**Important:** At least one of A or B must be non-zero (otherwise it's not a valid line)!

**Tip**: Use the **"Random"** button to auto-fill empty fields for quick testing!

### Step 3: Analyze
Click **"Analyze Lines"** to get:
- Relationship type for each pair (intersect/parallel/coincide)
- Detailed step-by-step mathematical solution
- Intersection points (with coordinates)
- Angles between lines (in degrees)

### Step 4: Visualize (Optional)
Click **"Visualize"** to see:
- All lines plotted on a coordinate system
- Intersection points marked in red
- Automatic scaling and legend

### Additional Actions
- **" Clear"**: Reset all inputs and results
- **" View Source Code"**: Access project information and source files

---

## Example Usage

### Example 1: Three Intersecting Lines

**Input:**
```
Number of lines: 3

Line 1: A = 1,  B = 1,   C = -2    →  x + y - 2 = 0
Line 2: A = 1,  B = -1,  C = 0     →  x - y = 0
Line 3: A = 2,  B = -3,  C = 5     →  2x - 3y + 5 = 0
```

**Output:**
```
✓ Pair 1 (Line 1 & Line 2): INTERSECT at (1.00, 1.00), angle = 90.00°
✓ Pair 2 (Line 1 & Line 3): INTERSECT at (-1.00, 3.00), angle = 33.69°
✓ Pair 3 (Line 2 & Line 3): INTERSECT at (-5.00, -5.00), angle = 56.31°
```

### Example 2: Parallel Lines

**Input:**
```
Number of lines: 2

Line 1: A = 1,  B = 1,  C = -2    →  x + y = 2
Line 2: A = 1,  B = 1,  C = -4    →  x + y = 4
```

**Output:**
```
║ Pair 1 (Line 1 & Line 2): PARALLEL (distinct lines, never intersect)
```

### Example 3: Coincident Lines

**Input:**
```
Number of lines: 2

Line 1: A = 2,  B = -3,  C = 5     →  2x - 3y + 5 = 0
Line 2: A = 4,  B = -6,  C = 10    →  4x - 6y + 10 = 0
```

**Output:**
```
≡ Pair 1 (Line 1 & Line 2): COINCIDENT (same line)
```

---

## Project Structure

```
Analytic-Geometry-Midterm/
│
├── main.py                  # Application entry point
├── gui_app.py              # GUI interface (CustomTkinter)
├── line_geometry.py        # Core mathematical engine
├── test_line_geometry.py   # Unit tests (25 tests)
│
├── build_exe.py            # PyInstaller build script
├── requirements.txt        # Python dependencies
│
├── README.md               # This file
├── PROJECT_SUMMARY.md      # Detailed project report
└── .gitignore             # Git ignore rules
```

---

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Language** | Python | 3.12+ |
| **GUI Framework** | CustomTkinter | 5.2.0+ |
| **Visualization** | Matplotlib | 3.7.0+ |
| **Numerical Computing** | NumPy | 1.24.0+ |
| **Image Processing** | Pillow | 10.0.0+ |
| **Executable Builder** | PyInstaller | 6.0.0+ |
| **Testing** | unittest | Built-in |

---

## Mathematical Algorithms

### Relationship Detection
Uses proportionality of coefficients:
- **Coincident**: `A₁/A₂ = B₁/B₂ = C₁/C₂`
- **Parallel**: `A₁/A₂ = B₁/B₂ ≠ C₁/C₂`
- **Intersect**: `A₁/A₂ ≠ B₁/B₂`

### Intersection Points
Uses **Cramer's Rule** to solve the system:
```
A₁x + B₁y = -C₁
A₂x + B₂y = -C₂

x = Dₓ/D,  y = Dᵧ/D

where:
D  = A₁B₂ - A₂B₁
Dₓ = (-C₁)B₂ - (-C₂)B₁
Dᵧ = A₁(-C₂) - A₂(-C₁)
```

### 3. Angle Calculation
For non-vertical lines with slopes m₁ and m₂:
```
tan(θ) = |m₂ - m₁| / |1 + m₁·m₂|

where:
m = -A/B (slope)
θ ∈ [0°, 90°]
```

Special case: If `m₁·m₂ = -1`, lines are perpendicular (θ = 90°)

---

## Testing

The project includes comprehensive unit tests covering all functionality:

**Run tests:**
```bash
python test_line_geometry.py
```

**Test Coverage:**
-  Line validation and creation
-  Vertical and horizontal line detection
-  Slope calculations
-  Proportionality checking
-  Relationship determination
-  Intersection point accuracy
-  Angle calculations (including edge cases)
-  Task specification examples

**Results:**
```
Ran 25 tests in 0.022s
OK
```

---

## Building for Distribution

### Create Standalone Executable

**1. Run the build script:**
```bash
python build_exe.py
```

**2. What happens:**
-  Checks/installs PyInstaller
-  Cleans old build files
-  Compiles all dependencies into one `.exe`
-  Creates user documentation

**3. Output:**
```
dist/
├── LineAnalyzer.exe    (~50-70 MB)
└── README.txt          (User guide)
```

**4. Distribution:**
- Share only the `dist/` folder
- No Python installation needed on target machines
- Works on Windows 7+

---

## Troubleshooting

### Common Issues

**Issue**: Application won't start
- **Solution**: Make sure Python 3.12+ is installed
- **Check**: `python --version`

**Issue**: "Module not found" errors
- **Solution**: Install dependencies: `pip install -r requirements.txt`

**Issue**: .exe file won't run
- **Solution**: Check antivirus settings (may block unsigned executables)
- **Workaround**: Run as administrator or add to whitelist

**Issue**: Graph not displaying
- **Solution**: Ensure matplotlib is installed: `pip install matplotlib`

**Issue**: Invalid line error
- **Solution**: Make sure at least one of A or B is non-zero

---

## Author

**Nurdaulet Sovetkhan**  
Student, Astana IT University  
Analytic Geometry Course | Midterm Project

---

## License

This project is created for educational purposes as part of the Analytic Geometry course at Astana IT University.

---

## Acknowledgments

- **Course**: Analytic Geometry
- **Institution**: Astana IT University
- **Date**: October 2025
- **Frameworks**: CustomTkinter, Matplotlib, NumPy

---

<div align="center">

**Made with ❤️ for Analytic Geometry**

</div>
