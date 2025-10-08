"""
Unit Tests for Line Geometry Module
===================================
Тесты для проверки корректности геометрических вычислений
"""

import unittest
import math
from line_geometry import (
    Line, LineRelation, 
    get_line_relation, 
    find_intersection, 
    calculate_angle,
    are_proportional,
    analyze_line_pair
)


class TestLine(unittest.TestCase):
    """Тесты для класса Line"""
    
    def test_valid_line(self):
        """Тест создания валидной линии"""
        line = Line(1, 2, 3)
        self.assertEqual(line.A, 1.0)
        self.assertEqual(line.B, 2.0)
        self.assertEqual(line.C, 3.0)
    
    def test_invalid_line(self):
        """Тест создания невалидной линии (A=B=0)"""
        with self.assertRaises(ValueError):
            Line(0, 0, 5)
    
    def test_vertical_line(self):
        """Тест вертикальной линии (B=0)"""
        line = Line(1, 0, -3)  # x = 3
        self.assertTrue(line.is_vertical())
        self.assertFalse(line.is_horizontal())
        self.assertIsNone(line.get_slope())
    
    def test_horizontal_line(self):
        """Тест горизонтальной линии (A=0)"""
        line = Line(0, 1, -2)  # y = 2
        self.assertTrue(line.is_horizontal())
        self.assertFalse(line.is_vertical())
        self.assertEqual(line.get_slope(), 0.0)
    
    def test_regular_line_slope(self):
        """Тест наклона обычной линии"""
        line = Line(2, 4, 1)  # 2x + 4y + 1 = 0
        slope = line.get_slope()
        self.assertAlmostEqual(slope, -0.5)


class TestProportionality(unittest.TestCase):
    """Тесты для проверки пропорциональности"""
    
    def test_coincident_lines(self):
        """Тест совпадающих линий"""
        dir_prop, all_prop = are_proportional(2, 3, 4, 4, 6, 8)
        self.assertTrue(dir_prop)
        self.assertTrue(all_prop)
    
    def test_parallel_lines(self):
        """Тест параллельных линий"""
        dir_prop, all_prop = are_proportional(1, 1, -2, 1, 1, -4)
        self.assertTrue(dir_prop)
        self.assertFalse(all_prop)
    
    def test_intersecting_lines(self):
        """Тест пересекающихся линий"""
        dir_prop, all_prop = are_proportional(1, 1, -2, 1, -1, 0)
        self.assertFalse(dir_prop)
        self.assertFalse(all_prop)


class TestLineRelation(unittest.TestCase):
    """Тесты для определения типа отношения между линиями"""
    
    def test_intersecting_lines(self):
        """Тест пересекающихся линий"""
        l1 = Line(1, 1, -2)  # x + y - 2 = 0
        l2 = Line(1, -1, 0)  # x - y = 0
        relation = get_line_relation(l1, l2)
        self.assertEqual(relation, LineRelation.INTERSECT)
    
    def test_parallel_lines(self):
        """Тест параллельных линий"""
        l1 = Line(1, 1, -2)  # x + y - 2 = 0
        l2 = Line(1, 1, -4)  # x + y - 4 = 0
        relation = get_line_relation(l1, l2)
        self.assertEqual(relation, LineRelation.PARALLEL)
    
    def test_coincident_lines(self):
        """Тест совпадающих линий"""
        l1 = Line(2, -3, 5)
        l2 = Line(4, -6, 10)
        relation = get_line_relation(l1, l2)
        self.assertEqual(relation, LineRelation.COINCIDENT)
    
    def test_vertical_parallel_lines(self):
        """Тест параллельных вертикальных линий"""
        l1 = Line(1, 0, -2)  # x = 2
        l2 = Line(1, 0, -5)  # x = 5
        relation = get_line_relation(l1, l2)
        self.assertEqual(relation, LineRelation.PARALLEL)


class TestIntersection(unittest.TestCase):
    """Тесты для нахождения точек пересечения"""
    
    def test_simple_intersection(self):
        """Тест простого пересечения"""
        l1 = Line(1, 1, -2)  # x + y = 2
        l2 = Line(1, -1, 0)  # x - y = 0
        point = find_intersection(l1, l2)
        self.assertIsNotNone(point)
        self.assertAlmostEqual(point[0], 1.0)
        self.assertAlmostEqual(point[1], 1.0)
    
    def test_vertical_horizontal_intersection(self):
        """Тест пересечения вертикальной и горизонтальной линий"""
        l1 = Line(1, 0, -3)  # x = 3
        l2 = Line(0, 1, -2)  # y = 2
        point = find_intersection(l1, l2)
        self.assertIsNotNone(point)
        self.assertAlmostEqual(point[0], 3.0)
        self.assertAlmostEqual(point[1], 2.0)
    
    def test_parallel_no_intersection(self):
        """Тест отсутствия пересечения для параллельных линий"""
        l1 = Line(1, 1, -2)
        l2 = Line(1, 1, -4)
        point = find_intersection(l1, l2)
        self.assertIsNone(point)
    
    def test_coincident_no_intersection(self):
        """Тест отсутствия единственной точки для совпадающих линий"""
        l1 = Line(2, -3, 5)
        l2 = Line(4, -6, 10)
        point = find_intersection(l1, l2)
        self.assertIsNone(point)


class TestAngleCalculation(unittest.TestCase):
    """Тесты для вычисления углов"""
    
    def test_perpendicular_lines(self):
        """Тест перпендикулярных линий (90°)"""
        l1 = Line(1, 1, -2)   # x + y = 2 (slope = -1)
        l2 = Line(1, -1, 0)   # x - y = 0 (slope = 1)
        angle = calculate_angle(l1, l2)
        self.assertIsNotNone(angle)
        self.assertAlmostEqual(angle, 90.0, places=5)
    
    def test_vertical_horizontal_angle(self):
        """Тест угла между вертикальной и горизонтальной линиями"""
        l1 = Line(1, 0, -3)  # x = 3 (вертикальная)
        l2 = Line(0, 1, -2)  # y = 2 (горизонтальная)
        angle = calculate_angle(l1, l2)
        self.assertIsNotNone(angle)
        self.assertAlmostEqual(angle, 90.0, places=5)
    
    def test_45_degree_angle(self):
        """Тест угла 45°"""
        l1 = Line(1, 0, 0)    # x = 0 (вертикальная)
        l2 = Line(1, -1, 0)   # x - y = 0 (slope = 1, 45° от горизонтали)
        angle = calculate_angle(l1, l2)
        self.assertIsNotNone(angle)
        self.assertAlmostEqual(angle, 45.0, places=5)
    
    def test_parallel_no_angle(self):
        """Тест отсутствия угла для параллельных линий"""
        l1 = Line(1, 1, -2)
        l2 = Line(1, 1, -4)
        angle = calculate_angle(l1, l2)
        self.assertIsNone(angle)
    
    def test_acute_angle(self):
        """Тест острого угла"""
        l1 = Line(1, 0, 0)    # x = 0 (вертикальная)
        l2 = Line(1, -2, 0)   # x - 2y = 0 (slope = 0.5)
        angle = calculate_angle(l1, l2)
        self.assertIsNotNone(angle)
        # Угол должен быть между 0 и 90
        self.assertGreater(angle, 0)
        self.assertLess(angle, 90)


class TestAnalyzePair(unittest.TestCase):
    """Тесты для полного анализа пары линий"""
    
    def test_analyze_intersecting(self):
        """Тест анализа пересекающихся линий"""
        l1 = Line(1, 1, -2)
        l2 = Line(1, -1, 0)
        result = analyze_line_pair(l1, l2)
        
        self.assertEqual(result['relation'], 'intersect')
        self.assertIsNotNone(result['intersection'])
        self.assertIsNotNone(result['angle'])
        self.assertAlmostEqual(result['intersection'][0], 1.0)
        self.assertAlmostEqual(result['intersection'][1], 1.0)
        self.assertAlmostEqual(result['angle'], 90.0)
    
    def test_analyze_parallel(self):
        """Тест анализа параллельных линий"""
        l1 = Line(1, 1, -2)
        l2 = Line(1, 1, -4)
        result = analyze_line_pair(l1, l2)
        
        self.assertEqual(result['relation'], 'parallel')
        self.assertIsNone(result['intersection'])
        self.assertIsNone(result['angle'])
    
    def test_analyze_coincident(self):
        """Тест анализа совпадающих линий"""
        l1 = Line(2, -3, 5)
        l2 = Line(4, -6, 10)
        result = analyze_line_pair(l1, l2)
        
        self.assertEqual(result['relation'], 'coincident')
        self.assertIsNone(result['intersection'])
        self.assertIsNone(result['angle'])


class TestFromTaskExample(unittest.TestCase):
    """Тесты из примера задания"""
    
    def test_task_example(self):
        """Тест из примера задания: 3 линии"""
        # Enter coefficients A1 B1 C1: 1 1 -2
        # Enter coefficients A2 B2 C2: 1 -1 0
        # Enter coefficients A3 B3 C3: 2 -3 5
        
        lines = [
            Line(1, 1, -2),   # L1: x + y - 2 = 0
            Line(1, -1, 0),   # L2: x - y = 0
            Line(2, -3, 5)    # L3: 2x - 3y + 5 = 0
        ]
        
        # L1 и L2 должны пересекаться
        result_12 = analyze_line_pair(lines[0], lines[1])
        self.assertEqual(result_12['relation'], 'intersect')
        self.assertIsNotNone(result_12['intersection'])
        
        # L1 и L3 должны пересекаться
        result_13 = analyze_line_pair(lines[0], lines[2])
        self.assertEqual(result_13['relation'], 'intersect')
        
        # L2 и L3 должны пересекаться
        result_23 = analyze_line_pair(lines[1], lines[2])
        self.assertEqual(result_23['relation'], 'intersect')


if __name__ == '__main__':
    # Запускаем тесты с подробным выводом
    unittest.main(verbosity=2)
