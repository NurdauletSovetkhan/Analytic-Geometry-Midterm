import math

def test_cases():
    print("=== START OF TESTING ===")    
    # Import functions from main.py
    from main import (is_valid_line, get_slope, are_parallel, are_coincident, 
                     find_intersection, calculate_angle, analyze_line_pair)
    
    # Test 1: Vertical lines
    print("Test 1: Vertical lines")
    A1, B1, C1 = 1, 0, -1  # x = 1
    A2, B2, C2 = 1, 0, -2  # x = 2
    analyze_line_pair(A1, B1, C1, A2, B2, C2, 1, 2)
    
    # Test 2: Coincident lines
    print("\nTest 2: Coincident lines")
    A1, B1, C1 = 1, 1, -2  # x + y = 2
    A2, B2, C2 = 2, 2, -4  # 2x + 2y = 4 (same line)
    analyze_line_pair(A1, B1, C1, A2, B2, C2, 1, 2)
    
    # Test 3: Parallel but not coincident
    print("\nTest 3: Parallel but not coincident lines")
    A1, B1, C1 = 1, 1, -2  # x + y = 2
    A2, B2, C2 = 1, 1, -4  # x + y = 4
    analyze_line_pair(A1, B1, C1, A2, B2, C2, 1, 2)
    
    # Test 4: Horizontal and vertical (perpendicular)
    print("\nTest 4: Horizontal and vertical lines")
    A1, B1, C1 = 0, 1, -1  # y = 1
    A2, B2, C2 = 1, 0, -1  # x = 1
    analyze_line_pair(A1, B1, C1, A2, B2, C2, 1, 2)
    
    print("\n=== TESTING COMPLETED ===")

if __name__ == "__main__":
    test_cases()