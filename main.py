"""
Program for analyzing relationships between lines.
Performs analytical geometry assignment.
"""

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import tkinter as tk
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

from geometry_calc import input_lines, analyze_all_pairs
if MATPLOTLIB_AVAILABLE:
    from visualization import plot_lines


def run_console():
    """
    Runs the console version of the program.
    """
    print("=" * 60)
    print("LINE RELATIONSHIP ANALYSIS (Console Mode)")
    print("=" * 60)
    
    # Input data and analyze
    lines = input_lines()
    results = analyze_all_pairs(lines)
    
    # Offer to show plot if matplotlib is available
    if MATPLOTLIB_AVAILABLE:
        print("\\n" + "=" * 40)
        try:
            show_plot = input("Show graphical representation? (y/n): ").lower() == 'y'
            if show_plot:
                print("Building plot...")
                plot_lines(lines, results)
        except:
            pass  # If user interrupted input
    else:
        print("\\nTo enable graphical representation, install matplotlib:")
        print("pip install matplotlib")
    
    print("\\nAnalysis complete!")


def run_gui():
    """
    Runs the GUI version of the program.
    """
    if not TKINTER_AVAILABLE:
        print("Error: tkinter not available!")
        print("Running console version...")
        run_console()
        return
    
    try:
        from gui import LineAnalyzerGUI
        root = tk.Tk()
        app = LineAnalyzerGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"Error starting GUI: {e}")
        print("Running console version...")
        run_console()


def run_example():
    """
    Runs the program with the example from the assignment.
    """
    print("=" * 60)
    print("ASSIGNMENT EXAMPLE")
    print("=" * 60)
    print("Using data from example:")
    print("3 lines:")
    print("l1: 1x + 1y - 2 = 0")
    print("l2: 1x - 1y + 0 = 0") 
    print("l3: 2x - 3y + 5 = 0")
    print()
    
    lines = [(1, 1, -2), (1, -1, 0), (2, -3, 5)]
    results = analyze_all_pairs(lines)
    
    if MATPLOTLIB_AVAILABLE:
        try:
            show_plot = input("\\nShow plot? (y/n): ").lower() == 'y'
            if show_plot:
                plot_lines(lines, results)
        except:
            pass


def main():
    """
    Main function - mode selection.
    """
    print("=" * 60)
    print("LINE RELATIONSHIP ANALYSIS")
    print("=" * 60)
    print("Select working mode:")
    print("1. GUI (graphical interface) - recommended")
    print("2. Console mode")
    print("3. Show assignment example")
    print()
    
    if not TKINTER_AVAILABLE:
        print("Note: GUI not available, tkinter not found")
    if not MATPLOTLIB_AVAILABLE:
        print("Note: Plots not available, matplotlib not found")
    
    try:
        choice = input("Choose (1, 2, 3 or Enter for GUI): ").strip()
        
        if choice == "2":
            run_console()
        elif choice == "3":
            run_example()
        else:  # Default or "1"
            run_gui()
            
    except KeyboardInterrupt:
        print("\\nProgram interrupted.")
    except Exception as e:
        print(f"Error: {e}")
        print("Running console version...")
        run_console()


if __name__ == "__main__":
    # Can run regular program or example
    print("1. Run program")
    print("2. Show assignment example")
    try:
        choice = input("Choose (1 or 2, or just Enter for program): ").strip()
        if choice == "2":
            run_example()
        else:
            main()
    except KeyboardInterrupt:
        print("\\nProgram interrupted.")
    except Exception as e:
        print(f"Error: {e}")
        print("Running main program...")
        main()
