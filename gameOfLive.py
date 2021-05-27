from typing import List

import numpy as np
import pickle
import pygame


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
        pygame.draw.line(surface, (50, 50, 80), (ix, 0), (ix, maxSz[1]))

    pygame.draw.line(surface, (180, 50, 180), (30, 0), (30, maxSz[1]))
    pygame.draw.line(surface, (180, 50, 180), (maxSz[0]-30, 0), (maxSz[0]-30, maxSz[1]))

    for iy in range(0, maxSz[1], sz):
        pygame.draw.line(surface, (50, 50, 80), (0, iy), (maxSz[0], iy))

    pygame.draw.line(surface, (180, 50, 180), (0, 30), (maxSz[0], 30))
    pygame.draw.line(surface, (180, 50, 180), (0, maxSz[1]-30), (maxSz[0], maxSz[1]-30))



def pixOnGrid(surface, p: [int, int], sz: int, org: [int, int], maxSz: [int, int], col: [int, int, int]):
    px = p[0]
    py = p[1]
    if (px + org[0]) * sz > maxSz[0] or org[0] + px < 0:
        return
    if (py + org[1]) * sz > maxSz[1] or org[1] + py < 0:
        return
    pygame.draw.rect(surface, col, ((px + org[0]) * sz, (py + org[1]) * sz, sz - 1, sz - 1))


def absPos2rel(x: int, y: int, centerM: [int, int]) -> [int, int]:
    return centerM[0] + x, centerM[1] + y


def getPosTrans(c: [int, int]):
    def absPos2relM(x: [int, int]) -> [int, int]:
        return c[0] + x[0], c[1] + x[1]

    return absPos2relM


def getPosTrans2abs(c: [int, int]):
    def relMPos2abs(x: [int, int]) -> [int, int]:
        return c[0] - x[0], c[1] - x[1]

    return relMPos2abs


def toAria(listMap, aries):
    for x in range(len(listMap)):
        try:
            aries[listMap[x][0], listMap[x][1]] = 1
        except:
            pass


def drawAriea(aria, surface, cellsize, orgM, maxSz, ux, uy):
    for x in range(ux):
        for y in range(uy):
            try:
                if aria[x, y]:
                    pixOnGrid(surface, (x, y), cellsize, orgM, maxSz, (255, 255, 255))
            except:
                pass


def game(x, y):
    pygame.init()
    x, y = x * 10, y * 10
    surface = pygame.display.set_mode((x, y))
    pygame.display.set_caption("John Conway's Game of Life || MarkinHaus edit")
    cellsize = 8
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
            if mx <= 30:
                tblr[2] = 1
                count = 1
            if mx >= x - 30:
                tblr[3] = 1
                count = 1
            if my <= 30:
                tblr[0] = 1
                count = 1
            if my >= y - 30:
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

                if pygame.key.get_pressed()[pygame.K_w]:
                    sblock = not tog

                if pygame.key.get_pressed()[pygame.K_3]:
                    del aria
                    aria = genArea(int(x / 2), int(y / 2))
                    print("=" * 20)
                    print("del")
                if pygame.key.get_pressed()[pygame.K_2]:
                    tog = False
                    print("=" * 20)
                    print("Saving")
                    # l = [(0,0), (0,1), (0,-1)]
                    # a = str(list(map(getPosTrans(center), aria)))
                    # z = eval(str(list(map(getPosTrans2abs(center), aria))))
                    # print(l, a, z)
                    pickle.dump(aria, open("Maps/map", "wb"))

                if pygame.key.get_pressed()[pygame.K_1]:
                    tog = False
                    print("=" * 20)
                    print("Loding")
                    aria = pickle.load(open("Maps/map", "rb"))

                if pygame.key.get_pressed()[pygame.K_q]:
                    orgM = [0, 0]
                if pygame.key.get_pressed()[pygame.K_e]:
                    cellsize = 8
                    mv = int(1 / (30 - cellsize))
                    if cellsize >= 8:
                        mv = 1

        if movFps % int(50 / mv) == 0:
            if tblr[1] == 1:
                org = [org[0], org[1] - 1]
            if tblr[3] == 1:
                org = [org[0] - 1, org[1]]
            if tblr[0] == 1:
                org = [org[0], org[1] + 1]
            if tblr[2] == 1:
                org = [org[0] + 1, org[1]]

        if movFps % (2 + cellsize) == 0:
            orgM = (org[0] + orgM[0], org[1] + orgM[1])
        movFps += 1
        surface.fill((20, 20, 30))
        drawGrid(surface, maxSz, cellsize)
        if tog:
            aria = setNewState(int(x / cellsize), int(y / cellsize), aria)
        drawAriea(aria, surface, cellsize, orgM, maxSz, int(x / cellsize), int(y / cellsize))

        pygame.display.update()


if __name__ == "__main__":
    game(120, 90)
