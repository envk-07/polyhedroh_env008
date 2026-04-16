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
                    self.vertexes.append(R3(x, y, z).rz(
                        alpha).ry(beta).rz(gamma) * c)
                else:
                    # вспомогательный массив
                    buf = line.split()
                    # количество вершин очередной грани
                    size = int(buf.pop(0))
                    # массив вершин этой грани
                    vertexes = [self.vertexes[int(n) - 1] for n in buf]
                    # задание рёбер грани
                    for n in range(size):
                        self.edges.append(Edge(vertexes[n - 1], vertexes[n]))
                    # задание самой грани
                    self.facets.append(Facet(vertexes))

    @staticmethod
    def is_good_point(p):
        """Точка хорошая, если её проекция строго внутри квадрата [-1,1]x[-1,1]"""
        return -1 < p.x < 1 and -1 < p.y < 1

    @staticmethod
    def projected_edge_length(edge):
        """Длина проекции ребра на плоскость XY (игнорируем Z)"""
        dx = edge.fin.x - edge.beg.x
        dy = edge.fin.y - edge.beg.y
        return sqrt(dx*dx + dy*dy)

    def sum_good_edges_projection_length(self):
        """Сумма длин проекций рёбер, оба конца которых — хорошие точки"""
        total = 0.0
        for edge in self.edges:
            if self.is_good_point(edge.beg) and self.is_good_point(edge.fin):
                total += self.projected_edge_length(edge)
        return total

    # Метод изображения полиэдра
    def draw(self, tk):
        tk.clean()
        for e in self.edges:
            tk.draw_line(e.beg, e.fin)

        result = self.sum_good_edges_projection_length()
        print(f"Сумма длин проекций рёбер с «хорошими» концами: {result:.6f}")
