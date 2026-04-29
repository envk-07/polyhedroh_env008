"""
Тесты для проверки суммы длин проекций рёбер с «хорошими» концами.
"""
import pytest
from shadow.polyedr import Polyedr


class TestGoodEdgesSum:
    """Проверка корректности определения «хороших» точек и расчёта суммы."""

    def test_all_vertices_inside(self):
        """Все вершины строго внутри [-1, 1]×[-1, 1]. Ожидается: 16.0"""
        p = Polyedr("data/test_all_good.geom")
        assert p.good_edges_sum() == pytest.approx(16.0, abs=1e-6)

    def test_all_vertices_outside(self):
        """Все вершины за пределами квадрата. Ожидается: 0.0"""
        p = Polyedr("data/test_none_good.geom")
        assert p.good_edges_sum() == pytest.approx(0.0, abs=1e-6)

    def test_mixed_vertices(self):
        """Только верхняя грань внутри квадрата. Ожидается: 6.4"""
        p = Polyedr("data/test_mixed.geom")
        assert p.good_edges_sum() == pytest.approx(6.4, abs=1e-6)

    def test_boundary_excluded(self):
        """Вершины на границе x=1 или y=1 не «хорошие». Ожидается: 0.0"""
        p = Polyedr("data/test_boundary.geom")
        assert p.good_edges_sum() == pytest.approx(0.0, abs=1e-6)
