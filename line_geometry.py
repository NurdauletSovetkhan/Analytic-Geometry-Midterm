"""
Line Geometry Module
===================
Модуль для работы с линиями в общем виде: Ax + By + C = 0

Основные функции:
- Проверка валидности линии
- Определение типа отношения между линиями (пересечение/параллель/совпадение)
- Вычисление точки пересечения
- Вычисление угла между линиями
"""

import math
from typing import Tuple, Optional, Dict, Any
from enum import Enum


class LineRelation(Enum):
    """Типы отношений между линиями"""
    INTERSECT = "intersect"
    PARALLEL = "parallel"
    COINCIDENT = "coincident"


class Line:
    """
    Класс для представления линии в общем виде: Ax + By + C = 0
    """
    
    def __init__(self, A: float, B: float, C: float):
        """
        Инициализация линии
        
        Args:
            A: коэффициент при x
            B: коэффициент при y
            C: свободный член
        
        Raises:
            ValueError: если линия невалидна (A = B = 0)
        """
        self.A = float(A)
        self.B = float(B)
        self.C = float(C)
        
        if not self.is_valid():
            raise ValueError(f"Invalid line: A and B cannot both be zero (A={A}, B={B})")
    
    def is_valid(self) -> bool:
        """
        Проверяет валидность линии
        Линия валидна если хотя бы один из коэффициентов A или B не равен нулю
        
        Returns:
            True если линия валидна, иначе False
        """
        return not (abs(self.A) < 1e-10 and abs(self.B) < 1e-10)
    
    def is_vertical(self) -> bool:
        """
        Проверяет, является ли линия вертикальной (B = 0)
        
        Returns:
            True если линия вертикальная, иначе False
        """
        return abs(self.B) < 1e-10
    
    def is_horizontal(self) -> bool:
        """
        Проверяет, является ли линия горизонтальной (A = 0)
        
        Returns:
            True если линия горизонтальная, иначе False
        """
        return abs(self.A) < 1e-10
    
    def get_slope(self) -> Optional[float]:
        """
        Вычисляет наклон линии (m = -A/B)
        
        Returns:
            Наклон линии или None для вертикальных линий
        """
        if self.is_vertical():
            return None  # Вертикальная линия - наклон бесконечен
        return -self.A / self.B
    
    def __repr__(self) -> str:
        """Строковое представление линии"""
        return f"Line({self.A}x + {self.B}y + {self.C} = 0)"
    
    def __str__(self) -> str:
        """Красивое строковое представление"""
        def format_coef(val, var):
            if abs(val) < 1e-10:
                return ""
            sign = "+" if val > 0 else "-"
            abs_val = abs(val)
            if abs(abs_val - 1) < 1e-10:
                return f"{sign} {var}"
            return f"{sign} {abs_val}{var}"
        
        parts = []
        # A term
        if abs(self.A) > 1e-10:
            if abs(abs(self.A) - 1) < 1e-10:
                parts.append("x" if self.A > 0 else "-x")
            else:
                parts.append(f"{self.A}x")
        
        # B term
        b_part = format_coef(self.B, "y")
        if b_part:
            parts.append(b_part)
        
        # C term
        if abs(self.C) > 1e-10:
            sign = "+" if self.C > 0 else "-"
            parts.append(f"{sign} {abs(self.C)}")
        
        if not parts:
            return "0 = 0"
        
        equation = " ".join(parts)
        if equation.startswith("+ "):
            equation = equation[2:]
        
        return f"{equation} = 0"


def are_proportional(A1: float, B1: float, C1: float,
                     A2: float, B2: float, C2: float) -> Tuple[bool, bool]:
    """
    Проверяет пропорциональность коэффициентов линий
    
    Две линии:
    - Совпадают если (A1, B1, C1) пропорциональны (A2, B2, C2)
    - Параллельны если (A1, B1) пропорциональны (A2, B2), но не пропорциональны с C
    
    Args:
        A1, B1, C1: коэффициенты первой линии
        A2, B2, C2: коэффициенты второй линии
    
    Returns:
        Tuple[bool, bool]: (направления_пропорциональны, все_пропорциональны)
    """
    # Проверяем пропорциональность направлений (A, B)
    # Используем кросс-произведение: A1*B2 - A2*B1 == 0
    cross_product = A1 * B2 - A2 * B1
    directions_proportional = abs(cross_product) < 1e-10
    
    if not directions_proportional:
        return False, False
    
    # Если направления пропорциональны, проверяем C
    # Находим коэффициент пропорциональности
    k = None
    if abs(A2) > 1e-10:
        k = A1 / A2
    elif abs(B2) > 1e-10:
        k = B1 / B2
    else:
        # Обе линии вырождены (не должно произойти)
        return False, False
    
    # Проверяем C
    expected_C = k * C2
    all_proportional = abs(C1 - expected_C) < 1e-10
    
    return True, all_proportional


def get_line_relation(line1: Line, line2: Line) -> LineRelation:
    """
    Определяет тип отношения между двумя линиями
    
    Args:
        line1: первая линия
        line2: вторая линия
    
    Returns:
        LineRelation: тип отношения (INTERSECT, PARALLEL, COINCIDENT)
    """
    directions_prop, all_prop = are_proportional(
        line1.A, line1.B, line1.C,
        line2.A, line2.B, line2.C
    )
    
    if all_prop:
        return LineRelation.COINCIDENT
    elif directions_prop:
        return LineRelation.PARALLEL
    else:
        return LineRelation.INTERSECT


def find_intersection(line1: Line, line2: Line) -> Optional[Tuple[float, float]]:
    """
    Находит точку пересечения двух линий
    
    Решает систему линейных уравнений:
    A1*x + B1*y + C1 = 0
    A2*x + B2*y + C2 = 0
    
    Используя правило Крамера:
    x = (B1*C2 - B2*C1) / (A1*B2 - A2*B1)
    y = (A2*C1 - A1*C2) / (A1*B2 - A2*B1)
    
    Args:
        line1: первая линия
        line2: вторая линия
    
    Returns:
        Tuple[float, float]: координаты точки пересечения (x, y) или None
    """
    relation = get_line_relation(line1, line2)
    
    if relation != LineRelation.INTERSECT:
        return None
    
    # Вычисляем определитель
    det = line1.A * line2.B - line2.A * line1.B
    
    if abs(det) < 1e-10:
        return None  # Линии параллельны или совпадают
    
    # Правило Крамера
    x = (line1.B * line2.C - line2.B * line1.C) / det
    y = (line2.A * line1.C - line1.A * line2.C) / det
    
    return (x, y)


def calculate_angle(line1: Line, line2: Line) -> Optional[float]:
    """
    Вычисляет угол между двумя пересекающимися линиями
    
    Использует формулу: tan(θ) = |m2 - m1| / (1 + m1*m2)
    где m1 и m2 - наклоны линий
    
    Угол возвращается в градусах, всегда положительный и не превышает 90°
    
    Args:
        line1: первая линия
        line2: вторая линия
    
    Returns:
        float: угол в градусах (0-90°) или None если линии не пересекаются
    """
    relation = get_line_relation(line1, line2)
    
    if relation != LineRelation.INTERSECT:
        return None
    
    m1 = line1.get_slope()
    m2 = line2.get_slope()
    
    # Случай 1: Обе линии вертикальные (не должно быть, т.к. они параллельны)
    if m1 is None and m2 is None:
        return None
    
    # Случай 2: Одна линия вертикальная
    if m1 is None:
        # line1 вертикальная, угол с line2
        angle_rad = math.atan(abs(m2))
        angle_deg = math.degrees(angle_rad)
        return 90.0 - angle_deg
    
    if m2 is None:
        # line2 вертикальная, угол с line1
        angle_rad = math.atan(abs(m1))
        angle_deg = math.degrees(angle_rad)
        return 90.0 - angle_deg
    
    # Случай 3: Обе линии невертикальные
    # Проверяем перпендикулярность: m1 * m2 = -1
    product = m1 * m2
    if abs(product + 1) < 1e-10:
        return 90.0
    
    # Вычисляем угол по формуле
    numerator = abs(m2 - m1)
    denominator = abs(1 + m1 * m2)
    
    if denominator < 1e-10:
        return 90.0  # Перпендикулярны
    
    tan_theta = numerator / denominator
    angle_rad = math.atan(tan_theta)
    angle_deg = math.degrees(angle_rad)
    
    # Возвращаем наименьший положительный угол (0-90°)
    return min(angle_deg, 180 - angle_deg) if angle_deg <= 90 else angle_deg


def analyze_line_pair(line1: Line, line2: Line) -> Dict[str, Any]:
    """
    Полный анализ пары линий
    
    Args:
        line1: первая линия
        line2: вторая линия
    
    Returns:
        Dict: словарь с результатами анализа:
            - relation: тип отношения (str)
            - intersection: точка пересечения или None
            - angle: угол между линиями в градусах или None
    """
    relation = get_line_relation(line1, line2)
    intersection = find_intersection(line1, line2)
    angle = calculate_angle(line1, line2)
    
    return {
        'relation': relation.value,
        'intersection': intersection,
        'angle': angle
    }


def analyze_all_lines(lines: list[Line]) -> list[Dict[str, Any]]:
    """
    Анализирует все пары линий
    
    Args:
        lines: список линий для анализа
    
    Returns:
        list: список словарей с результатами для каждой пары
    """
    results = []
    n = len(lines)
    
    for i in range(n):
        for j in range(i + 1, n):
            result = analyze_line_pair(lines[i], lines[j])
            result['pair'] = (i + 1, j + 1)  # 1-indexed для пользователя
            result['line1'] = lines[i]
            result['line2'] = lines[j]
            results.append(result)
    
    return results


if __name__ == "__main__":
    # Тестирование модуля
    print("=== Line Geometry Module Test ===\n")
    
    # Пример 1: Пересекающиеся линии
    print("Example 1: Intersecting lines")
    l1 = Line(1, 1, -2)  # x + y - 2 = 0
    l2 = Line(1, -1, 0)  # x - y = 0
    print(f"Line 1: {l1}")
    print(f"Line 2: {l2}")
    result = analyze_line_pair(l1, l2)
    print(f"Relation: {result['relation']}")
    print(f"Intersection: {result['intersection']}")
    print(f"Angle: {result['angle']:.2f}°" if result['angle'] else "Angle: N/A")
    print()
    
    # Пример 2: Параллельные линии
    print("Example 2: Parallel lines")
    l3 = Line(1, 1, -2)  # x + y - 2 = 0
    l4 = Line(1, 1, -4)  # x + y - 4 = 0
    print(f"Line 3: {l3}")
    print(f"Line 4: {l4}")
    result = analyze_line_pair(l3, l4)
    print(f"Relation: {result['relation']}")
    print(f"Intersection: {result['intersection']}")
    print()
    
    # Пример 3: Совпадающие линии
    print("Example 3: Coincident lines")
    l5 = Line(2, -3, 5)  # 2x - 3y + 5 = 0
    l6 = Line(4, -6, 10)  # 4x - 6y + 10 = 0 (то же самое)
    print(f"Line 5: {l5}")
    print(f"Line 6: {l6}")
    result = analyze_line_pair(l5, l6)
    print(f"Relation: {result['relation']}")
    print()
    
    # Пример 4: Вертикальная и невертикальная линии
    print("Example 4: Vertical and non-vertical lines")
    l7 = Line(1, 0, -3)  # x - 3 = 0 (вертикальная)
    l8 = Line(0, 1, -2)  # y - 2 = 0 (горизонтальная)
    print(f"Line 7: {l7} (vertical)")
    print(f"Line 8: {l8} (horizontal)")
    result = analyze_line_pair(l7, l8)
    print(f"Relation: {result['relation']}")
    print(f"Intersection: {result['intersection']}")
    print(f"Angle: {result['angle']:.2f}°" if result['angle'] else "Angle: N/A")
