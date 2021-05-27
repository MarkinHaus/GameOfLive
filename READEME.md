# John Conway's Game of Life

## Dependencies

- python 3.7+ 

- pygame ``pip install pygame`` | ``conda install -c cogsci pygame``

- numpy ``pip install numpy`` | ``conda install -c anaconda numpy``

## How to Use

Starting Game:
```
python gameOfLive.py 
```

Configfile

- World_xy -> Pixels times 10 in x and y
- Mov_fps_div_cell_size -> Movement speed inverted
- World_fps_cap -> Update each x Frames  
- BG_color -> Background Color
- Cell_color -> Cell Color
- Mov_border_color -> Movement Border Color
- Mov_border_offset -> Space between Window border and mouse Movement aria
- Border_color -> Border Color
- Init_cell_size -> Cell size
- Map_data -> File to load and save Map data

## Controls

- Movement with mouse 
- Scroll mousewheel
- set Cell mouse button left 
- remove Cell mouse button right
- "E" reset scaling
- "Q" reset Cell size to Init size
- "L" Load world from (Map_data) file
- "S" Save world to (Map_data) file
- "D" Delete world
- "W" start and stop simulation