"""
Graphical User Interface for the line analysis program.
Uses tkinter to create a user-friendly interface.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os

from geometry_calc import is_valid_line, get_line_relationship, calculate_angle
from visualization import calculate_plot_bounds, save_plot_to_images


class LineAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Line Relationship Analysis")
        self.root.geometry("1200x800")
        
        # Variables for storing data
        self.line_entries = []
        
        self.setup_gui()
        self.load_example()
    
    def setup_gui(self):
        """Creates the graphical user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left and right panels
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(left_frame, text="Line Relationship Analysis", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Line input area
        input_frame = ttk.LabelFrame(left_frame, text="Enter Lines (Ax + By + C = 0)", padding=10)
        input_frame.pack(fill=tk.X, pady=5)
        
        # Control buttons for managing lines
        control_frame = ttk.Frame(input_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(control_frame, text="Add Line", 
                  command=self.add_line_input).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="Remove Line", 
                  command=self.remove_line_input).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="Load Example", 
                  command=self.load_example).pack(side=tk.LEFT, padx=(0, 5))
        
        # Scrollable area for lines
        canvas_frame = ttk.Frame(input_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, height=150)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Action buttons
        action_frame = ttk.Frame(left_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(action_frame, text="Analyze", 
                  command=self.analyze_lines).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(action_frame, text="Clear", 
                  command=self.clear_results).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(action_frame, text="Save Results", 
                  command=self.save_results).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(action_frame, text="Save Plot", 
                  command=self.save_plot).pack(side=tk.LEFT)
        
        # Results output area
        results_frame = ttk.LabelFrame(left_frame, text="Analysis Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.results_text = scrolledtext.ScrolledText(
            results_frame, 
            height=15, 
            width=50, 
            wrap=tk.WORD,
            font=("Consolas", 10)
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Plot area
        plot_frame = ttk.LabelFrame(right_frame, text="Graphical Representation", padding=10)
        plot_frame.pack(fill=tk.BOTH, expand=True)
        
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.plot_canvas = FigureCanvasTkAgg(self.fig, plot_frame)
        self.plot_canvas.draw()
        self.plot_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initially add 3 line input fields
        for _ in range(3):
            self.add_line_input()
    
    def add_line_input(self):
        """Adds an input field for a new line."""
        line_frame = ttk.Frame(self.scrollable_frame)
        line_frame.pack(fill=tk.X, pady=2)
        
        line_num = len(self.line_entries) + 1
        ttk.Label(line_frame, text=f"Line {line_num}:", width=10).pack(side=tk.LEFT)
        
        # Fields for coefficients A, B, C
        ttk.Label(line_frame, text="A:").pack(side=tk.LEFT, padx=(10, 2))
        entry_a = ttk.Entry(line_frame, width=8)
        entry_a.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Label(line_frame, text="B:").pack(side=tk.LEFT, padx=(0, 2))
        entry_b = ttk.Entry(line_frame, width=8)
        entry_b.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Label(line_frame, text="C:").pack(side=tk.LEFT, padx=(0, 2))
        entry_c = ttk.Entry(line_frame, width=8)
        entry_c.pack(side=tk.LEFT)
        
        self.line_entries.append((line_frame, entry_a, entry_b, entry_c))
        
        # Update scroll area
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def remove_line_input(self):
        """Removes the last line input field."""
        if self.line_entries:
            line_frame, _, _, _ = self.line_entries.pop()
            line_frame.destroy()
            
            # Update numbering
            for i, (frame, _, _, _) in enumerate(self.line_entries):
                label = frame.winfo_children()[0]
                label.config(text=f"Line {i+1}:")
            
            # Update scroll area
            self.scrollable_frame.update_idletasks()
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def load_example(self):
        """Loads the example from the assignment."""
        # Clear existing fields
        while len(self.line_entries) > 3:
            self.remove_line_input()
        while len(self.line_entries) < 3:
            self.add_line_input()
        
        # Example from assignment
        examples = [(1, 1, -2), (1, -1, 0), (2, -3, 5)]
        
        for i, (a, b, c) in enumerate(examples):
            if i < len(self.line_entries):
                _, entry_a, entry_b, entry_c = self.line_entries[i]
                entry_a.delete(0, tk.END)
                entry_a.insert(0, str(a))
                entry_b.delete(0, tk.END)
                entry_b.insert(0, str(b))
                entry_c.delete(0, tk.END)
                entry_c.insert(0, str(c))
    
    def get_lines_from_input(self):
        """Gets lines from input fields."""
        lines = []
        for i, (_, entry_a, entry_b, entry_c) in enumerate(self.line_entries):
            try:
                a = float(entry_a.get().strip())
                b = float(entry_b.get().strip())
                c = float(entry_c.get().strip())
                
                if not is_valid_line(a, b, c):
                    messagebox.showerror("Error", 
                                       f"Line {i+1}: A and B cannot both be zero!")
                    return None
                
                lines.append((a, b, c))
            except ValueError:
                messagebox.showerror("Error", 
                                   f"Line {i+1}: Please enter valid numeric values!")
                return None
        
        if len(lines) < 2:
            messagebox.showwarning("Warning", 
                                 "Please enter at least 2 lines for analysis!")
            return None
        
        return lines
    
    def analyze_lines(self):
        """Performs analysis of entered lines."""
        # Clear previous results
        self.results_text.delete('1.0', tk.END)
        
        # Get data
        lines = self.get_lines_from_input()
        if not lines:
            return
        
        # Analyze
        try:
            # Create text results for GUI
            results_text = self.analyze_lines_for_gui(lines)
            
            # Display results
            self.results_text.insert(tk.END, results_text)
            
            # Plot graph
            self.plot_lines_on_canvas(lines)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error during analysis: {str(e)}")
    
    def analyze_lines_for_gui(self, lines):
        """Analyzes lines and returns text results for GUI."""
        n = len(lines)
        results = []
        
        results.append(f"Analysis of {n} lines:")
        results.append("=" * 50)
        
        # Display entered lines
        results.append("\nEntered lines:")
        for i, (a, b, c) in enumerate(lines):
            results.append(f"L{i+1}: {a}x + {b}y + {c} = 0")
        
        results.append("\nAnalysis of all pairs:")
        results.append("-" * 30)
        
        # Analyze all pairs
        for i in range(n):
            for j in range(i + 1, n):
                a1, b1, c1 = lines[i]
                a2, b2, c2 = lines[j]
                
                results.append(f"\nPair L{i+1} and L{j+1}:")
                
                rel = get_line_relationship(a1, b1, c1, a2, b2, c2)
                
                if rel['relationship'] == 'coincident':
                    results.append("  Relationship: Lines are coincident (same line)")
                elif rel['relationship'] == 'parallel':
                    results.append("  Relationship: Lines are parallel but distinct")
                elif rel['relationship'] == 'intersecting':
                    x, y = rel['intersection']
                    results.append("  Relationship: Lines intersect")
                    results.append(f"  Intersection point: ({x:.3f}, {y:.3f})")
                    
                    # Calculate angle
                    angle = calculate_angle(a1, b1, a2, b2)
                    results.append(f"  Angle between lines: {angle:.3f}°")
                    
                    if rel['perpendicular']:
                        results.append("  Lines are perpendicular")
        
        return "\n".join(results)
    
    def plot_lines_on_canvas(self, lines):
        """Plots lines on the embedded canvas."""
        self.ax.clear()
        
        # Determine plot boundaries
        x_min, x_max, y_min, y_max = calculate_plot_bounds(lines)
        
        x_range = x_max - x_min
        y_range = y_max - y_min
        margin = max(x_range, y_range) * 0.1
        
        plot_x_min = x_min - margin
        plot_x_max = x_max + margin
        plot_y_min = y_min - margin
        plot_y_max = y_max + margin
        
        # Plot lines
        colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
        styles = ['-', '--', '-.', ':']
        
        import numpy as np
        x_vals = np.linspace(plot_x_min, plot_x_max, 1000)
        
        for i, (a, b, c) in enumerate(lines):
            color = colors[i % len(colors)]
            style = styles[i % len(styles)]
            
            if abs(b) > 1e-10:  # Not a vertical line
                y_vals = -(a * x_vals + c) / b
                self.ax.plot(x_vals, y_vals, color=color, linestyle=style, 
                           linewidth=2, label=f'L{i+1}: {a}x + {b}y + {c} = 0')
            else:  # Vertical line
                x_vert = -c / a
                self.ax.axvline(x=x_vert, color=color, linestyle=style, 
                              linewidth=2, label=f'L{i+1}: {a}x + {b}y + {c} = 0')
        
        # Mark intersection points
        for i in range(len(lines)):
            for j in range(i + 1, len(lines)):
                rel = get_line_relationship(*lines[i], *lines[j])
                if rel['relationship'] == 'intersecting':
                    x_int, y_int = rel['intersection']
                    self.ax.plot(x_int, y_int, 'ko', markersize=8, markerfacecolor='yellow', 
                               markeredgecolor='black', markeredgewidth=2)
                    self.ax.annotate(f'({x_int:.2f}, {y_int:.2f})', 
                                   (x_int, y_int), xytext=(5, 5), 
                                   textcoords='offset points', fontsize=10,
                                   bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
        
        # Configure plot
        self.ax.set_xlim(plot_x_min, plot_x_max)
        self.ax.set_ylim(plot_y_min, plot_y_max)
        self.ax.grid(True, alpha=0.3)
        self.ax.axhline(y=0, color='k', linewidth=0.5)
        self.ax.axvline(x=0, color='k', linewidth=0.5)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_title('Graphical Representation of Lines')
        self.ax.legend()
        
        self.plot_canvas.draw()
    
    def clear_results(self):
        """Clears analysis results."""
        self.results_text.delete('1.0', tk.END)
        self.ax.clear()
        self.plot_canvas.draw()
    
    def save_results(self):
        """Saves results to a file."""
        content = self.results_text.get('1.0', tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "No results to save!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Success", f"Results saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving file: {str(e)}")
    
    def save_plot(self):
        """Saves the plot to the images directory."""
        try:
            # Get current timestamp for unique filename
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"line_analysis_{timestamp}.png"
            
            # Save to images directory
            saved_path = save_plot_to_images(filename, self.fig)
            messagebox.showinfo("Success", f"Plot saved to:\n{saved_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving plot: {str(e)}")


def main():
    """Launches the GUI application."""
    root = tk.Tk()
    app = LineAnalyzerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()