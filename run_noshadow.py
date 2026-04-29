#!/usr/bin/env -S python3 -B

from time import time
from common.tk_drawer import TkDrawer
from noshadow.polyedr import Polyedr


tk = TkDrawer()
try:
    for name in ["test_all_good", "ccc", "cube", "box", "king", "cow"]:
        print("=============================================================")
        print(f"Начало работы с полиэдром '{name}'")
        start_time = time()
        p = Polyedr(f"data/{name}.geom")
        print(f"Сумма длин: {p.good_edges_sum():.6f}")
        p.draw(tk)
        delta_time = time() - start_time
        print(f"Изображение полиэдра '{name}' заняло {delta_time} сек.")
        input("Hit 'Return' to continue -> ")
except(EOFError, KeyboardInterrupt):
    print("\nStop")
    tk.close()
