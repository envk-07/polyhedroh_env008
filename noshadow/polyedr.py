from math import pi, sqrt
from common.r3 import R3
from common.tk_drawer import TkDrawer


class Edge:
    """ Ребро полиэдра """
    # Параметры конструктора: начало и конец ребра (точки в R3)

    def __init__(self, beg, fin):
        self.beg, self.fin = beg, fin


class Facet:
    """ Грань полиэдра """
    # Параметры конструктора: список вершин

    def __init__(self, vertexes):
        self.vertexes = vertexes


class Polyedr:
    """ Полиэдр """
    # Параметры конструктора: файл, задающий полиэдр

    def __init__(self, file):

        # списки вершин, рёбер и граней полиэдра
        self.vertexes, self.edges, self.facets = [], [], []
        # списки для расчёта характеристики (без гомотетии и поворотов)
        self.raw_vertexes = []
        self.raw_edges = []

        # список строк файла
        with open(file) as f:
            for i, line in enumerate(f):
                if i == 0:
                    # обрабатываем первую строку; buf - вспомогательный массив
                    buf = line.split()
                    # коэффициент гомотетии
                    c = float(buf.pop(0))
                    # углы Эйлера, определяющие вращение
                    alpha, beta, gamma = (float(x) * pi / 180.0 for x in buf)
                elif i == 1:
                    # во второй строке число вершин, граней и рёбер полиэдра
                    nv, nf, ne = (int(x) for x in line.split())
                elif i < nv + 2:
                    # задание всех вершин полиэдра
                    x, y, z = (float(x) for x in line.split())
                    # сохраняем исходную вершину (для расчёта характеристики)
                    raw_v = R3(x, y, z)
                    self.raw_vertexes.append(raw_v)
                    # сохраняем преобразованную вершину (для отрисовки)
                    self.vertexes.append(R3(x, y, z).rz(
                        alpha).ry(beta).rz(gamma) * c)
                else:
                                   
                    # вспомогательный массив
                    buf = line.split()
                    # количество вершин очередной грани
                    size = int(buf.pop(0))
                    # массив вершин этой грани (преобразованные, для отрисовки)
                    vertexes = [self.vertexes[int(n) - 1] for n in buf]
                    # массив исходных вершин этой грани (для расчёта)
                    raw_vertexes = [self.raw_vertexes[int(n) - 1] for n in buf]
                    # задание рёбер грани
                    for n in range(size):
                        # ребро для отрисовки (преобразованное)
                        self.edges.append(Edge(vertexes[n - 1], vertexes[n]))
                        # ребро для расчёта (исходное)
                        self.raw_edges.append(Edge(raw_vertexes[n - 1], raw_vertexes[n]))
                    # задание самой грани
                    self.facets.append(Facet(vertexes))

    # Метод изображения полиэдра
    def draw(self, tk):
        tk.clean()
        for e in self.edges:
            tk.draw_line(e.beg, e.fin)


    def _is_good(self, v):
        """Точка «хорошая», если её проекция строго внутри квадрата [-1,1]×[-1,1]"""
        return -1 < v.x < 1 and -1 < v.y < 1

    def _proj_len(self, e):
        """Длина проекции ребра на плоскость XY"""
        dx = e.fin.x - e.beg.x
        dy = e.fin.y - e.beg.y
        return sqrt(dx * dx + dy * dy)

    def good_edges_sum(self):
        """Сумма длин проекций рёбер, у которых оба конца — «хорошие» точки"""
        s = 0.0
        for e in self.edges:
            if self._is_good(e.beg) and self._is_good(e.fin):
                s += self._proj_len(e)
        return s





    def _is_good(self, v):
        return -1 < v.x < 1 and -1 < v.y < 1

    def _proj_len(self, e):
        dx = e.fin.x - e.beg.x
        dy = e.fin.y - e.beg.y
        return sqrt(dx * dx + dy * dy)

    def good_edges_sum(self):
        return sum(self._proj_len(e) for e in self.raw_edges 
                   if self._is_good(e.beg) and self._is_good(e.fin))
