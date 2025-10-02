"""
Module for geometric calculations with lines.
Contains functions for analyzing relationships between straight lines on a plane.
"""

import math


def is_valid_line(A, B, C):
    """
    Checks if the line is correctly defined.
    Line Ax + By + C = 0 is correct if (A, B) != (0, 0)
    
    Args:
        A, B, C (float): Coefficients of line Ax + By + C = 0
        
    Returns:
        bool: True if line is correct, False otherwise
    """
    return A != 0 or B != 0


def get_slope(A, B):
    """
    Returns the slope of line Ax + By + C = 0.
    If B != 0, then slope m = -A/B
    If B = 0, then the line is vertical (slope = infinity)
    
    Args:
        A, B (float): Coefficients A and B of the line
        
    Returns:
        float or None: Slope of the line or None if vertical
    """
    if B == 0:
        return None  # Vertical line
    return -A / B


def are_parallel(A1, B1, C1, A2, B2, C2):
    """
    Checks if two lines are parallel.
    Two lines are parallel if their direction vectors are proportional.
    
    Args:
        A1, B1, C1 (float): Coefficients of first line
        A2, B2, C2 (float): Coefficients of second line
        
    Returns:
        bool: True if lines are parallel, False otherwise
    """
    # Check if direction vectors (A1, B1) and (A2, B2) are proportional
    # This happens when A1*B2 - A2*B1 = 0
    return abs(A1 * B2 - A2 * B1) < 1e-10


def are_coincident(A1, B1, C1, A2, B2, C2):
    """
    Checks if two lines are coincident (same line).
    Two lines are coincident if they are parallel and have a common point.
    
    Args:
        A1, B1, C1 (float): Coefficients of first line
        A2, B2, C2 (float): Coefficients of second line
        
    Returns:
        bool: True if lines are coincident, False otherwise
    """
    # First check if they are parallel
    if not are_parallel(A1, B1, C1, A2, B2, C2):
        return False
    
    # If parallel, check if coefficients are proportional
    # This means the lines are the same
    if abs(A1) > 1e-10:
        k = A2 / A1
        return abs(B2 - k * B1) < 1e-10 and abs(C2 - k * C1) < 1e-10
    elif abs(B1) > 1e-10:
        k = B2 / B1
        return abs(A2 - k * A1) < 1e-10 and abs(C2 - k * C1) < 1e-10
    else:
        return False


def find_intersection(A1, B1, C1, A2, B2, C2):
    """
    Finds intersection point of two lines.
    Solves the system:
    A1*x + B1*y + C1 = 0
    A2*x + B2*y + C2 = 0
    
    Args:
        A1, B1, C1 (float): Coefficients of first line
        A2, B2, C2 (float): Coefficients of second line
        
    Returns:
        tuple or None: (x, y) coordinates of intersection or None if no intersection
    """
    # Calculate determinant
    det = A1 * B2 - A2 * B1
    
    if abs(det) < 1e-10:
        return None  # Lines are parallel or coincident
    
    # Solve using Cramer's rule
    x = (-C1 * B2 + C2 * B1) / det
    y = (-A1 * C2 + A2 * C1) / det
    
    return (x, y)


def calculate_angle(A1, B1, A2, B2):
    """
    Calculates the angle between two lines in degrees.
    Uses direction vectors (A1, B1) and (A2, B2).
    
    Args:
        A1, B1 (float): Coefficients of first line
        A2, B2 (float): Coefficients of second line
        
    Returns:
        float: Angle between lines in degrees (0 to 90)
    """
    # Direction vectors
    v1 = (A1, B1)
    v2 = (A2, B2)
    
    # Calculate dot product
    dot_product = v1[0] * v2[0] + v1[1] * v2[1]
    
    # Calculate magnitudes
    mag1 = math.sqrt(v1[0]**2 + v1[1]**2)
    mag2 = math.sqrt(v2[0]**2 + v2[1]**2)
    
    # Calculate cosine of angle
    cos_angle = abs(dot_product) / (mag1 * mag2)
    
    # Ensure cosine is in valid range [-1, 1]
    cos_angle = max(-1, min(1, cos_angle))
    
    # Calculate angle in radians and convert to degrees
    angle_rad = math.acos(cos_angle)
    angle_deg = math.degrees(angle_rad)
    
    # Return acute angle (0 to 90 degrees)
    return min(angle_deg, 180 - angle_deg)


def are_perpendicular(A1, B1, A2, B2):
    """
    Checks if two lines are perpendicular.
    Two lines are perpendicular if their direction vectors are orthogonal.
    
    Args:
        A1, B1 (float): Direction vector of first line
        A2, B2 (float): Direction vector of second line
        
    Returns:
        bool: True if lines are perpendicular, False otherwise
    """
    # Lines are perpendicular if A1*A2 + B1*B2 = 0
    return abs(A1 * A2 + B1 * B2) < 1e-10


def get_line_points(A, B, C, x_range, num_points=100):
    """
    Generates points on a line for plotting.
    
    Args:
        A, B, C (float): Line coefficients Ax + By + C = 0
        x_range (tuple): (x_min, x_max) range for x values
        num_points (int): Number of points to generate
        
    Returns:
        tuple: (x_points, y_points) arrays of coordinates
    """
    import numpy as np
    
    x_min, x_max = x_range
    
    if abs(B) > 1e-10:  # Not a vertical line
        x_points = np.linspace(x_min, x_max, num_points)
        y_points = -(A * x_points + C) / B
        return x_points, y_points
    else:  # Vertical line
        if abs(A) > 1e-10:
            x_vert = -C / A
            # Return vertical line points
            y_range = x_max - x_min  # Use same range for y
            y_points = np.linspace(x_min, x_max, num_points)
            x_points = np.full(num_points, x_vert)
            return x_points, y_points
        else:
            # Invalid line
            return np.array([]), np.array([])


def get_line_relationship(A1, B1, C1, A2, B2, C2):
    """
    Determines the relationship between two lines.
    
    Args:
        A1, B1, C1 (float): Coefficients of first line
        A2, B2, C2 (float): Coefficients of second line
        
    Returns:
        dict: Dictionary with relationship type and additional info
    """
    result = {'relationship': None, 'intersection': None, 'angle': None, 'perpendicular': False}
    
    # Check if lines are coincident
    if are_coincident(A1, B1, C1, A2, B2, C2):
        result['relationship'] = 'coincident'
        return result
    
    # Check if lines are parallel
    if are_parallel(A1, B1, C1, A2, B2, C2):
        result['relationship'] = 'parallel'
        return result
    
    # Lines intersect
    result['relationship'] = 'intersecting'
    intersection = find_intersection(A1, B1, C1, A2, B2, C2)
    result['intersection'] = intersection
    
    # Calculate angle
    angle = calculate_angle(A1, B1, A2, B2)
    result['angle'] = angle
    
    # Check if perpendicular
    result['perpendicular'] = are_perpendicular(A1, B1, A2, B2)
    
    return result


def analyze_line_pair(A1, B1, C1, A2, B2, C2, i, j):
    """
    Analyzes a pair of lines and prints their relationship.
    
    Args:
        A1, B1, C1 (float): Coefficients of first line
        A2, B2, C2 (float): Coefficients of second line
        i, j (int): Line numbers for output
        
    Returns:
        dict: Analysis result
    """
    print(f"\nAnalysis of lines l{i} and l{j}:")
    
    result = get_line_relationship(A1, B1, C1, A2, B2, C2)
    
    if result['relationship'] == 'coincident':
        print("Lines are coincident (same line)")
    elif result['relationship'] == 'parallel':
        print("Lines are parallel but distinct")
    elif result['relationship'] == 'intersecting':
        x, y = result['intersection']
        print(f"Lines intersect at point ({x:.3f}, {y:.3f})")
        print(f"Angle between lines: {result['angle']:.3f}°")
        
        if result['perpendicular']:
            print("Lines are perpendicular")
        else:
            print("Lines are not perpendicular")
    
    return result


def input_lines():
    """
    Prompts user to input line coefficients.
    
    Returns:
        list: List of tuples (A, B, C) representing lines
    """
    lines = []
    
    print("Enter line coefficients in format Ax + By + C = 0")
    print("Note: A and B cannot both be zero")
    
    while True:
        try:
            n = int(input("\nEnter number of lines: "))
            if n < 2:
                print("Please enter at least 2 lines for analysis.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer.")
    
    for i in range(n):
        while True:
            try:
                print(f"\nLine {i + 1}:")
                A = float(input("Enter coefficient A: "))
                B = float(input("Enter coefficient B: "))
                C = float(input("Enter coefficient C: "))
                
                if not is_valid_line(A, B, C):
                    print("Error: A and B cannot both be zero!")
                    continue
                
                lines.append((A, B, C))
                print(f"Line l{i + 1}: {A}x + {B}y + {C} = 0")
                break
                
            except ValueError:
                print("Please enter valid numeric values.")
    
    return lines


def analyze_all_pairs(lines):
    """
    Analyzes all pairs of lines.
    
    Args:
        lines (list): List of tuples (A, B, C) with line coefficients
        
    Returns:
        list: List of analysis results for all pairs
    """
    n = len(lines)
    results = []
    
    print(f"\n{n} lines entered. Analyzing all pairs...")
    
    # Analyze all ordered pairs of lines
    for i in range(n):
        for j in range(i + 1, n):
            A1, B1, C1 = lines[i]
            A2, B2, C2 = lines[j]
            result = analyze_line_pair(A1, B1, C1, A2, B2, C2, i + 1, j + 1)
            results.append({
                'lines': ((A1, B1, C1), (A2, B2, C2)),
                'indices': (i + 1, j + 1),
                'analysis': result
            })
    
    return results


def main():
    """
    Main function to run the line analysis program.
    """
    print("=" * 60)
    print("LINE RELATIONSHIP ANALYSIS")
    print("=" * 60)
    
    # Input and analyze lines
    lines = input_lines()
    results = analyze_all_pairs(lines)
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()