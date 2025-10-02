"""
Module for visualizing lines and their relationships.
Uses matplotlib for plotting graphs.
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from geometry_calc import get_line_relationship, get_line_points


def setup_plot_style():
    """
    Sets up the plot style.
    """
    plt.style.use('default')
    plt.rcParams['figure.figsize'] = (12, 10)
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.grid'] = True


def calculate_plot_bounds(lines, margin=2):
    """
    Calculates plot boundaries based on intersection points and line slopes.
    
    Args:
        lines (list): List of tuples (A, B, C) with line coefficients
        margin (float): Margin from extreme points
        
    Returns:
        tuple: (x_min, x_max, y_min, y_max)
    """
    # Find all intersection points
    intersection_points = []
    n = len(lines)
    
    for i in range(n):
        for j in range(i + 1, n):
            A1, B1, C1 = lines[i]
            A2, B2, C2 = lines[j]
            rel = get_line_relationship(A1, B1, C1, A2, B2, C2)
            if rel['relationship'] == 'intersecting' and rel['intersection']:
                intersection_points.append(rel['intersection'])
    
    if intersection_points:
        x_coords = [point[0] for point in intersection_points]
        y_coords = [point[1] for point in intersection_points]
        
        x_min = min(x_coords) - margin
        x_max = max(x_coords) + margin
        y_min = min(y_coords) - margin
        y_max = max(y_coords) + margin
    else:
        # Default bounds if no intersections
        x_min, x_max = -10, 10
        y_min, y_max = -10, 10
    
    # Ensure minimum size
    if x_max - x_min < 4:
        center_x = (x_min + x_max) / 2
        x_min = center_x - 2
        x_max = center_x + 2
    
    if y_max - y_min < 4:
        center_y = (y_min + y_max) / 2
        y_min = center_y - 2
        y_max = center_y + 2
    
    return x_min, x_max, y_min, y_max


def get_line_color_and_style(index):
    """
    Returns color and line style for a given line index.
    
    Args:
        index (int): Line index
        
    Returns:
        tuple: (color, linestyle, linewidth)
    """
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
    styles = ['-', '--', '-.', ':']
    
    color = colors[index % len(colors)]
    style = styles[index % len(styles)]
    
    return color, style, 2


def plot_lines(lines, results=None, show_plot=True, save_path=None):
    """
    Plots multiple lines and their relationships.
    
    Args:
        lines (list): List of tuples (A, B, C) with line coefficients
        results (list): List of analysis results (optional)
        show_plot (bool): Whether to display the plot
        save_path (str): Path to save the plot (optional)
    """
    setup_plot_style()
    
    # Calculate plot bounds
    x_min, x_max, y_min, y_max = calculate_plot_bounds(lines)
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Plot each line
    for i, (A, B, C) in enumerate(lines):
        color, style, width = get_line_color_and_style(i)
        
        # Get points for plotting
        x_points, y_points = get_line_points(A, B, C, (x_min, x_max))
        
        if len(x_points) > 0:
            # Filter points within plot bounds
            valid_indices = (y_points >= y_min) & (y_points <= y_max)
            
            if np.any(valid_indices):
                ax.plot(x_points[valid_indices], y_points[valid_indices], 
                       color=color, linestyle=style, linewidth=width,
                       label=f'L{i+1}: {A}x + {B}y + {C} = 0')
            else:
                # For lines that don't intersect the visible area
                ax.plot(x_points, y_points, color=color, linestyle=style, 
                       linewidth=width, label=f'L{i+1}: {A}x + {B}y + {C} = 0')
    
    # Mark intersection points
    n = len(lines)
    for i in range(n):
        for j in range(i + 1, n):
            A1, B1, C1 = lines[i]
            A2, B2, C2 = lines[j]
            rel = get_line_relationship(A1, B1, C1, A2, B2, C2)
            
            if rel['relationship'] == 'intersecting' and rel['intersection']:
                x, y = rel['intersection']
                if x_min <= x <= x_max and y_min <= y <= y_max:
                    ax.plot(x, y, 'ko', markersize=8, markerfacecolor='yellow', 
                           markeredgecolor='black', markeredgewidth=2)
                    ax.annotate(f'({x:.2f}, {y:.2f})', 
                              (x, y), xytext=(5, 5), textcoords='offset points',
                              fontsize=10, bbox=dict(boxstyle='round,pad=0.3', 
                              facecolor='yellow', alpha=0.7))
    
    # Set plot properties
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Line Relationship Analysis\nGraphical Representation')
    ax.legend()
    
    # Add analysis summary as text
    if results:
        summary_text = create_analysis_summary(lines, results)
        ax.text(0.02, 0.98, summary_text, transform=ax.transAxes, 
               fontsize=9, verticalalignment='top',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.8))
    
    plt.tight_layout()
    
    # Save plot if path provided
    if save_path:
        # Ensure images directory exists
        images_dir = os.path.join(os.path.dirname(__file__), 'images')
        os.makedirs(images_dir, exist_ok=True)
        
        # Create full path in images directory
        if not os.path.dirname(save_path):
            save_path = os.path.join(images_dir, save_path)
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")
    
    if show_plot:
        plt.show()
    
    return fig, ax


def create_analysis_summary(lines, results):
    """
    Creates a text summary of the analysis results.
    
    Args:
        lines (list): List of line coefficients
        results (list): List of analysis results
        
    Returns:
        str: Formatted summary text
    """
    summary = f"Analysis of {len(lines)} lines:\n"
    
    pair_count = 0
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            rel = get_line_relationship(*lines[i], *lines[j])
            
            if rel['relationship'] == 'coincident':
                summary += f"L{i+1} & L{j+1}: Coincident\n"
            elif rel['relationship'] == 'parallel':
                summary += f"L{i+1} & L{j+1}: Parallel\n"
            elif rel['relationship'] == 'intersecting':
                x, y = rel['intersection']
                summary += f"L{i+1} & L{j+1}: Intersect at ({x:.2f}, {y:.2f})\n"
                if rel['perpendicular']:
                    summary += f"  (Perpendicular)\n"
            
            pair_count += 1
            if pair_count >= 5:  # Limit summary length
                summary += "..."
                break
        if pair_count >= 5:
            break
    
    return summary


def plot_line_pair(line1, line2, show_details=True, save_path=None):
    """
    Plots two lines and analyzes their relationship.
    
    Args:
        line1 (tuple): (A1, B1, C1) coefficients of first line
        line2 (tuple): (A2, B2, C2) coefficients of second line
        show_details (bool): Whether to show detailed analysis
        save_path (str): Path to save the plot (optional)
    """
    A1, B1, C1 = line1
    A2, B2, C2 = line2
    
    # Analyze relationship
    rel = get_line_relationship(A1, B1, C1, A2, B2, C2)
    
    # Calculate plot bounds
    lines = [line1, line2]
    x_min, x_max, y_min, y_max = calculate_plot_bounds(lines)
    
    # Create plot
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Plot first line
    x1_points, y1_points = get_line_points(A1, B1, C1, (x_min, x_max))
    ax.plot(x1_points, y1_points, 'r-', linewidth=2, label=f'L1: {A1}x + {B1}y + {C1} = 0')
    
    # Plot second line  
    x2_points, y2_points = get_line_points(A2, B2, C2, (x_min, x_max))
    ax.plot(x2_points, y2_points, 'b--', linewidth=2, label=f'L2: {A2}x + {B2}y + {C2} = 0')
    
    # Mark intersection if exists
    if rel['relationship'] == 'intersecting' and rel['intersection']:
        x, y = rel['intersection']
        ax.plot(x, y, 'go', markersize=10, label=f'Intersection ({x:.3f}, {y:.3f})')
        
        if show_details:
            ax.annotate(f'Intersection\n({x:.3f}, {y:.3f})\nAngle: {rel["angle"]:.1f}°', 
                       (x, y), xytext=(10, 10), textcoords='offset points',
                       fontsize=10, bbox=dict(boxstyle='round,pad=0.5', 
                       facecolor='lightgreen', alpha=0.8))
    
    # Set plot properties
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    
    # Title based on relationship
    if rel['relationship'] == 'coincident':
        title = 'Lines are Coincident (Same Line)'
    elif rel['relationship'] == 'parallel':
        title = 'Lines are Parallel'
    else:
        title = f'Lines Intersect - Angle: {rel["angle"]:.1f}°'
        if rel['perpendicular']:
            title += ' (Perpendicular)'
    
    ax.set_title(title)
    ax.legend()
    
    plt.tight_layout()
    
    # Save plot if path provided
    if save_path:
        # Ensure images directory exists
        images_dir = os.path.join(os.path.dirname(__file__), 'images')
        os.makedirs(images_dir, exist_ok=True)
        
        # Create full path in images directory
        if not os.path.dirname(save_path):
            save_path = os.path.join(images_dir, save_path)
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")
    
    plt.show()
    return fig, ax


def save_plot_to_images(filename, figure=None):
    """
    Saves the current or specified plot to the images directory.
    
    Args:
        filename (str): Name of the file to save (with extension)
        figure: Matplotlib figure object (uses current figure if None)
    """
    # Ensure images directory exists
    images_dir = os.path.join(os.path.dirname(__file__), 'images')
    os.makedirs(images_dir, exist_ok=True)
    
    # Create full path
    file_path = os.path.join(images_dir, filename)
    
    if figure:
        figure.savefig(file_path, dpi=300, bbox_inches='tight')
    else:
        plt.savefig(file_path, dpi=300, bbox_inches='tight')
    
    print(f"Plot saved to: {file_path}")
    return file_path


def main():
    """
    Example usage of the visualization module.
    """
    # Example lines from the assignment
    lines = [
        (1, 1, -2),   # x + y - 2 = 0
        (1, -1, 0),   # x - y = 0
        (2, -3, 5)    # 2x - 3y + 5 = 0
    ]
    
    print("Visualizing example lines...")
    plot_lines(lines, save_path="example_lines.png")


if __name__ == "__main__":
    main()