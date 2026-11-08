import math

COLORES = [
    (1.0, 0.2, 0.2, 1), (1.0, 0.6, 0.0, 1), (1.0, 1.0, 0.0, 1),
    (0.2, 1.0, 0.2, 1), (0.2, 0.8, 1.0, 1), (0.8, 0.3, 1.0, 1),
]

def trayectoria(origen, objetivo, rect, rebotes=5):
    """Segmentos ((x1,y1),(x2,y2)) desde 'origen' hacia 'objetivo' con
    'rebotes' rebotes en las bandas del rectangulo (xmin, ymin, xmax, ymax)."""
    xmin, ymin, xmax, ymax = rect
    x, y = origen
    dx, dy = objetivo[0] - x, objetivo[1] - y
    norma = math.hypot(dx, dy)
    if norma == 0:
        return []
    dx, dy = dx / norma, dy / norma

    segmentos = []
    for _ in range(rebotes + 1):
        ts = []
        if dx > 0: ts.append(((xmax - x) / dx, 'x'))
        if dx < 0: ts.append(((xmin - x) / dx, 'x'))
        if dy > 0: ts.append(((ymax - y) / dy, 'y'))
        if dy < 0: ts.append(((ymin - y) / dy, 'y'))
        if not ts:
            break
        t, eje = min(ts)
        nx, ny = x + dx * t, y + dy * t
        segmentos.append(((x, y), (nx, ny)))
        if eje == 'x':
            dx = -dx
        else:
            dy = -dy
        x, y = nx, ny
    return segmentos
