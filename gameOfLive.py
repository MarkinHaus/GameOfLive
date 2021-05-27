from typing import List

import numpy as np
import pickle
import pygame

Conf_default = {"World_xy": (120, 90),
                "Mov_fps_div_cell_size": 50,
                "World_fps_cap": 2,
                "BG_color": (20, 20, 30),
                "Cell_color": (255, 255, 255),
                "Mov_border_color": (180, 50, 180),
                "Mov_border_offset": 30,
                "Border_color": (50, 50, 80),
                "Init_cell_size": 8,
                "Map_data": "Maps/map"
                }


def getCond(x: int, y: int, Area: np.array) -> [int, int, int]:
    cell = [Area[x - 1][y + 1], Area[x][y + 1], Area[x + 1][y + 1],
            Area[x - 1][y], 0, Area[x + 1][y],
            Area[x - 1][y - 1], Area[x][y - 1], Area[x + 1][y - 1]]
    sCell = sum(cell)
    # 1
    # 2
    if (sCell < 2 and Area[x][y]) or (sCell > 3 and Area[x][y]) or (sCell == 3 and not Area[x][y]):
        return [x, y, 1], 1
    return [0, 0, 0], 0


def setNewState(x: int, y: int, Area: np.array) -> List:
    sto = []
    for nx in range(1, x - 1):
        for ny in range(1, y - 1):
            data, toSve = getCond(nx, ny, Area)
            if toSve:
                sto.append(data)
    for ix, iy, bitFlip in sto:
        Area[ix][iy] = Area[ix][iy] ^ bitFlip
    return Area


def genArea(x: int, y: int) -> np.array:
    return np.zeros((x, y), dtype=int)


def drawGrid(surface: pygame.display, maxSz: [int, int], sz: int):
    for ix in range(0, maxSz[0], sz):
        pygame.draw.line(surface, Conf["Border_color"], (ix, 0), (ix, maxSz[1]))

    pygame.draw.line(surface, Conf["Mov_border_color"], (Conf["Mov_border_offset"], 0),
                     (Conf["Mov_border_offset"], maxSz[1]))
    pygame.draw.line(surface, Conf["Mov_border_color"], (maxSz[0] - Conf["Mov_border_offset"], 0),
                     (maxSz[0] - Conf["Mov_border_offset"], maxSz[1]))

    for iy in range(0, maxSz[1], sz):
        pygame.draw.line(surface, Conf["Border_color"], (0, iy), (maxSz[0], iy))

    pygame.draw.line(surface, Conf["Mov_border_color"], (0, Conf["Mov_border_offset"]),
                     (maxSz[0], Conf["Mov_border_offset"]))
    pygame.draw.line(surface, Conf["Mov_border_color"], (0, maxSz[1] - Conf["Mov_border_offset"]),
                     (maxSz[0], maxSz[1] - Conf["Mov_border_offset"]))


def pixOnGrid(surface: pygame.display, p: [int, int], sz: int, org: [int, int], maxSz: [int, int], col: [int, int, int]):
    px = p[0]
    py = p[1]
    if (px + org[0]) * sz > maxSz[0] or org[0] + px < 0:
        return
    if (py + org[1]) * sz > maxSz[1] or org[1] + py < 0:
        return
    pygame.draw.rect(surface, col, ((px + org[0]) * sz, (py + org[1]) * sz, sz - 1, sz - 1))


def drawAriea(aria, surface, cellsize, orgM, maxSz, ux, uy):
    for x in range(ux):
        for y in range(uy):
            try:
                if aria[x, y]:
                    pixOnGrid(surface, (x, y), cellsize, orgM, maxSz, Conf["Cell_color"])
            except:
                pass


def game(x, y):
    pygame.init()
    x, y = x * 10, y * 10
    surface = pygame.display.set_mode((x, y))
    pygame.display.set_caption("John Conway's Game of Life || MarkinHaus")
    cellsize = Conf["Init_cell_size"]
    org = [0, 0]
    orgM = (0, 0)
    maxSz = [x, y]
    movFps = 0
    aria = genArea(int(x / 2), int(y / 2))
    tog = False
    tblr = [0, 0, 0, 0]
    mv = 30 - cellsize
    if cellsize >= 8:
        mv = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # print(event.type, '/', event)
            mx, my = pygame.mouse.get_pos()
            if event.type == pygame.WINDOWLEAVE:
                org = [0, 0]
                tblr = [0, 0, 0, 0]

            if pygame.mouse.get_pressed(3)[0]:
                aria[int(mx / cellsize) - orgM[0], int(my / cellsize) - orgM[1]] = 1
            if pygame.mouse.get_pressed(3)[2]:
                aria[int(mx / cellsize) - orgM[0], int(my / cellsize) - orgM[1]] = 0

            count = 0
            if mx <= Conf["Mov_border_offset"]:
                tblr[2] = 1
                count = 1
            if mx >= x - Conf["Mov_border_offset"]:
                tblr[3] = 1
                count = 1
            if my <= Conf["Mov_border_offset"]:
                tblr[0] = 1
                count = 1
            if my >= y - Conf["Mov_border_offset"]:
                tblr[1] = 1
                count = 1

            if not count:
                org = [0, 0]
                tblr = [0, 0, 0, 0]
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    cellsize = min(cellsize + 1, 500)
                    mv = 30 - cellsize
                    if cellsize >= 8:
                        mv = 1
                if event.button == 5:
                    cellsize = max(cellsize - 1, 2)
                    mv = 30 - cellsize
                    if cellsize >= 8:
                        mv = 1
            if event.type == pygame.KEYDOWN:

                if pygame.key.get_pressed()[pygame.K_w]:
                    tog = not tog

                if pygame.key.get_pressed()[pygame.K_d]:
                    del aria
                    aria = genArea(int(x / 2), int(y / 2))
                    print("=" * 20)
                    print("del")
                if pygame.key.get_pressed()[pygame.K_s]:
                    tog = False
                    print("=" * 20)
                    print("Saving")
                    pickle.dump(aria, open(Conf['Map_data'], "wb"))

                if pygame.key.get_pressed()[pygame.K_l]:
                    tog = False
                    print("=" * 20)
                    print("Loading")
                    aria = pickle.load(open(Conf['Map_data'], "rb"))

                if pygame.key.get_pressed()[pygame.K_q]:
                    orgM = [0, 0]
                if pygame.key.get_pressed()[pygame.K_e]:
                    cellsize = Conf["Init_cell_size"]
                    mv = int(1 / (30 - cellsize))
                    if cellsize >= 8:
                        mv = 1

        if movFps % int(Conf["Mov_fps_div_cell_size"] / mv) == 0:
            if tblr[1] == 1:
                org = [org[0], org[1] - 1]
            if tblr[3] == 1:
                org = [org[0] - 1, org[1]]
            if tblr[0] == 1:
                org = [org[0], org[1] + 1]
            if tblr[2] == 1:
                org = [org[0] + 1, org[1]]

        if movFps % (Conf["World_fps_cap"] + cellsize) == 0:
            orgM = (org[0] + orgM[0], org[1] + orgM[1])
        movFps += 1
        surface.fill(Conf["BG_color"])
        drawGrid(surface, maxSz, cellsize)
        if tog:
            aria = setNewState(int(x / cellsize), int(y / cellsize), aria)
        drawAriea(aria, surface, cellsize, orgM, maxSz, int(x / cellsize), int(y / cellsize))

        pygame.display.update()


if __name__ == "__main__":
    print("=" * 20)
    try:
        Conf = eval(open("conf", "r").read())
        print("CONF:")
        print(f"World_xy = {Conf['World_xy']} \n"
              f"Mov_fps_div_cell_size = {Conf['Mov_fps_div_cell_size']} \n"
              f"World_fps_cap = {Conf['World_fps_cap']} \n"
              f"BG_color = {Conf['BG_color']} \n"
              f"Cell_color = {Conf['Cell_color']} \n"
              f"Mov_border_color = {Conf['Mov_border_color']} \n"
              f"Mov_border_offset = {Conf['Mov_border_offset']} \n"
              f"Border_color = {Conf['Border_color']} \n"
              f"Init_cell_size = {Conf['Init_cell_size']} \n"
              f"Map_data = {Conf['Map_data']}")
    except FileExistsError and FileNotFoundError and KeyError and SyntaxError:
        Conf = Conf_default
        print("DEFAULT Wars")
    print("=" * 20)
    game(Conf["World_xy"][0], Conf["World_xy"][1])
