#!/usr/bin/env python3
"""Generate 15 Pacman-style maze maps for Easter Egg game.

Each map is 30x20 chars with # border.
Maps are written to assets/maps/11-*.txt through 25-*.txt

Tile legend:
  # = bush (wall, impassable for everyone)
  . = grass (walkable)
  E = egg (10pts)
  G = golden egg (50pts)
  S = special egg (25pts)
  R = player spawn
  X = exit (opens when all eggs collected)
  D = dog enemy
  T = tractor start (becomes path intersection)
  = = horizontal tractor path
  | = vertical tractor path
  + = tractor path intersection
  F = fence (blocks dogs, not player)
  M = mud (slows player, blocks dogs)
  H = hole (blocks dogs, not player)
  C = chicken enemy
"""

import os
import random

W, H = 30, 20  # map dimensions

def empty_map():
    """Create a map filled with walls."""
    return [['#'] * W for _ in range(H)]

def set_border(m):
    """Ensure border is all walls."""
    for x in range(W):
        m[0][x] = '#'
        m[H-1][x] = '#'
    for y in range(H):
        m[y][0] = '#'
        m[y][W-1] = '#'

def carve_h(m, y, x1, x2):
    """Carve horizontal corridor."""
    for x in range(x1, x2+1):
        if 0 < x < W-1 and 0 < y < H-1:
            if m[y][x] == '#':
                m[y][x] = '.'

def carve_v(m, x, y1, y2):
    """Carve vertical corridor."""
    for y in range(y1, y2+1):
        if 0 < x < W-1 and 0 < y < H-1:
            if m[y][x] == '#':
                m[y][x] = '.'

def place_eggs_on_grass(m, count, egg_type='E', avoid=None):
    """Place eggs on random grass tiles."""
    if avoid is None:
        avoid = set()
    positions = []
    for y in range(1, H-1):
        for x in range(1, W-1):
            if m[y][x] == '.' and (x, y) not in avoid:
                positions.append((x, y))
    random.shuffle(positions)
    placed = 0
    for x, y in positions:
        if placed >= count:
            break
        m[y][x] = egg_type
        avoid.add((x, y))
        placed += 1
    return avoid

def place_eggs_along_corridors(m, count, egg_type='E', spacing=3, avoid=None):
    """Place eggs evenly along corridors with minimum spacing."""
    if avoid is None:
        avoid = set()
    # Collect all grass positions
    grass = []
    for y in range(1, H-1):
        for x in range(1, W-1):
            if m[y][x] == '.' and (x, y) not in avoid:
                grass.append((x, y))

    placed = []
    for x, y in grass:
        if len(placed) >= count:
            break
        # Check spacing from other placed eggs
        too_close = False
        for px, py in placed:
            if abs(px - x) + abs(py - y) < spacing:
                too_close = True
                break
        if not too_close:
            m[y][x] = egg_type
            placed.append((x, y))
            avoid.add((x, y))
    return avoid

def validate_map(m, name):
    """Validate map dimensions and content."""
    assert len(m) == H, f"{name}: height {len(m)} != {H}"
    for i, row in enumerate(m):
        assert len(row) == W, f"{name}: row {i} width {len(row)} != {W}"
    # Count special tiles
    r_count = sum(row.count('R') for row in m)
    x_count = sum(row.count('X') for row in m)
    egg_count = sum(row.count('E') + row.count('G') + row.count('S') for row in m)
    assert r_count == 1, f"{name}: R count = {r_count}"
    assert x_count == 1, f"{name}: X count = {x_count}"
    assert egg_count >= 1, f"{name}: no eggs!"
    print(f"  {name}: OK ({egg_count} eggs, {sum(row.count('D') for row in m)} dogs, "
          f"{sum(row.count('T') for row in m)} tractors, {sum(row.count('C') for row in m)} chickens)")

def save_map(m, filename):
    """Save map to file."""
    validate_map(m, filename)
    path = os.path.join("assets", "maps", filename)
    with open(path, 'w') as f:
        for row in m:
            f.write(''.join(row) + '\n')
    print(f"  Written: {path}")

def fix_width(m):
    """Fix all rows to exactly W=30 chars. Pads short rows, trims long ones."""
    for i, row in enumerate(m):
        if len(row) < W:
            # Insert '.' before the closing '#' wall
            diff = W - len(row)
            # Find last '#' (right wall) and insert padding before it
            if row[-1] == '#':
                m[i] = row[:-1] + ['.'] * diff + ['#']
            else:
                m[i] = row + ['.'] * diff
        elif len(row) > W:
            # Remove extra '.' chars from interior (find removable positions)
            diff = len(row) - W
            removed = 0
            # Work from right side, skip border
            for j in range(len(row) - 2, 0, -1):
                if removed >= diff:
                    break
                if row[j] == '.':
                    row.pop(j)
                    removed += 1
            m[i] = row[:W]  # safety trim
    return m

def fix_connectivity(m):
    """Ensure all eggs and exit are reachable from player. Punch holes in walls if needed."""
    from collections import deque
    wall_tiles = {'#'}
    player = None
    targets = []

    for y in range(H):
        for x in range(W):
            if m[y][x] == 'R':
                player = (x, y)
            elif m[y][x] in ('E', 'G', 'S', 'X'):
                targets.append((x, y))

    if not player:
        return m

    def bfs_reachable(start):
        visited = set()
        queue = deque([start])
        visited.add(start)
        while queue:
            cx, cy = queue.popleft()
            for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                nx, ny = cx+dx, cy+dy
                if 0 <= nx < W and 0 <= ny < H and (nx,ny) not in visited:
                    if m[ny][nx] not in wall_tiles:
                        visited.add((nx,ny))
                        queue.append((nx,ny))
        return visited

    for _ in range(50):
        reachable = bfs_reachable(player)
        unreachable = [t for t in targets if t not in reachable]
        if not unreachable:
            break

        target = unreachable[0]
        target_area = bfs_reachable(target)

        # Find wall between reachable and target area
        best_wall = None
        for y in range(1, H-1):
            for x in range(1, W-1):
                if m[y][x] in wall_tiles:
                    near_r = any((x+dx,y+dy) in reachable for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)])
                    near_t = any((x+dx,y+dy) in target_area for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)])
                    if near_r and near_t:
                        best_wall = (x, y)
                        break
            if best_wall:
                break

        if best_wall:
            m[best_wall[1]][best_wall[0]] = '.'
        else:
            break
    return m

def to_list(s):
    """Convert multiline string to map grid."""
    lines = s.strip().split('\n')
    result = []
    for line in lines:
        result.append(list(line))
    result = fix_width(result)
    result = fix_connectivity(result)
    return result


# ============================================================
# MAP DEFINITIONS — hand-crafted Pacman-style mazes
# ============================================================

def map_11():
    """Maze-Intro: Simple maze, no enemies, lots of eggs."""
    return to_list(
        "##############################\n"
        "#R...E....#.....#....E......E#\n"
        "#.########.###.##.########.#.#\n"
        "#.#......#.......#......#..#.#\n"
        "#.#.####.#.#####.#.####.#..#.#\n"
        "#.E.#..#...#...#...#..#.E..#.#\n"
        "#.#.#..#.###.#.###.#..#.#..#.#\n"
        "#.#.#..#.........#.#..#.#....#\n"
        "#.#.#..#####.#####.#..#.####.#\n"
        "#.#.E........E........E.#..#.#\n"
        "#.#.#..#####.#.#####.#.#...#.#\n"
        "#.#.#..#.....#.....#.#.#...#.#\n"
        "#.#.#..#.#########.#.#..#..#.#\n"
        "#.E.#..#...........#..#.E..#.#\n"
        "#.#.####.####.####.####.#..#.#\n"
        "#.#......#...E..#......#..#.#\n"
        "#.########.###.##.########.#.#\n"
        "#..E.......#.....#.......E.#.#\n"
        "#..........#.....#..........X#\n"
        "##############################"
    )

def map_12():
    """First-Chase: Simple maze, 1 dog."""
    return to_list(
        "##############################\n"
        "#R..E.....#........#...E....E#\n"
        "#.##.####.#.######.#.####.##.#\n"
        "#.#..#....#........#....#..#.#\n"
        "#.#..#.####.######.####.#..#.#\n"
        "#.E..#....E........E...E#..E.#\n"
        "#.####.##.########.##.####.#.#\n"
        "#......#......D.......#....#.#\n"
        "#.######.####.#.####.######.#\n"
        "#.#......#..........#......#.#\n"
        "#.#.####.#.########.#.####.#.#\n"
        "#.#.#..E.#....##....#.E..#.#.#\n"
        "#.#.#.##.####.##.####.##.#.#.#\n"
        "#.E.#.#................#.#.E.#\n"
        "#.#.#.####.######.####.#.#.#.#\n"
        "#.#.#......#......#......#.#.#\n"
        "#.#.########.####.########.#.#\n"
        "#.#..........#..#..........#.#\n"
        "#.E..........#..#.........EX.#\n"
        "##############################"
    )

def map_13():
    """Shortcut-Maze: Fence shortcuts (player-only)."""
    return to_list(
        "##############################\n"
        "#R..E..#.......E.......#.E..E#\n"
        "#.####.#.#####F#####.#.####.##\n"
        "#......#.#...........#.#....##\n"
        "#.######.#.#########.#.###..##\n"
        "#.E....#.#.#.......#.#...E..##\n"
        "#.####.#.#F#.#####.#F#.####.##\n"
        "#......#.#...#...#...#......##\n"
        "#.####.#.#####.#.#####.####.##\n"
        "#.#..E.#...........#....E.#.##\n"
        "#.#.####.####F####.####.#.#.##\n"
        "#.#....#.#.........#..#.#.D.##\n"
        "#.####.#.#.#######.#..#.####.#\n"
        "#......#.#.#.....#.#..#.....E#\n"
        "#.######.#.#.###.#.#..######.#\n"
        "#.E....#.#.#.E.#.#.#...E....#\n"
        "#.####.#.#.#####.#.#.####.#..#\n"
        "#......#.#.........#......#..#\n"
        "#.E....#.....E.....#.....E#.X#\n"
        "##############################"
    )

def map_14():
    """Tractor-Corridor: Tractor patrols maze corridors."""
    # Build with explicit coordinates to keep tractor path aligned
    m = empty_map()
    # Horizontal corridors
    for x in range(1,29): m[1][x] = '.'   # top
    for x in range(1,29): m[18][x] = '.'  # bottom
    for x in range(1,29): m[5][x] = '.'   # mid-upper
    for x in range(1,29): m[9][x] = '.'   # center
    for x in range(1,29): m[13][x] = '.'  # mid-lower
    for x in range(1,29): m[17][x] = '.'  # near-bottom
    # Vertical corridors
    for y in range(1,19): m[y][1] = '.'
    for y in range(1,19): m[y][7] = '.'
    for y in range(1,19): m[y][14] = '.'
    for y in range(1,19): m[y][21] = '.'
    for y in range(1,19): m[y][28] = '.'
    # Extra verticals
    for y in range(1,19): m[y][4] = '.'
    for y in range(1,19): m[y][11] = '.'
    for y in range(1,19): m[y][18] = '.'
    for y in range(1,19): m[y][25] = '.'
    # Add internal walls to create maze corridors
    for y in [2,3,4]:
        for x in [2,3]: m[y][x] = '#'
    for y in [2,3,4]:
        for x in [5,6]: m[y][x] = '#'
    for y in [2,3,4]:
        for x in [8,9,10]: m[y][x] = '#'
    for y in [2,3,4]:
        for x in [12,13]: m[y][x] = '#'
    for y in [2,3,4]:
        for x in [15,16,17]: m[y][x] = '#'
    for y in [2,3,4]:
        for x in [19,20]: m[y][x] = '#'
    for y in [2,3,4]:
        for x in [22,23,24]: m[y][x] = '#'
    for y in [2,3,4]:
        for x in [26,27]: m[y][x] = '#'
    # Similar wall blocks for lower sections
    for y in [6,7,8]:
        for x in [2,3]: m[y][x] = '#'
        for x in [5,6]: m[y][x] = '#'
        for x in [8,9,10]: m[y][x] = '#'
        for x in [15,16,17]: m[y][x] = '#'
        for x in [19,20]: m[y][x] = '#'
        for x in [22,23,24]: m[y][x] = '#'
        for x in [26,27]: m[y][x] = '#'
    for y in [10,11,12]:
        for x in [2,3]: m[y][x] = '#'
        for x in [5,6]: m[y][x] = '#'
        for x in [8,9,10]: m[y][x] = '#'
        for x in [12,13]: m[y][x] = '#'
        for x in [19,20]: m[y][x] = '#'
        for x in [22,23,24]: m[y][x] = '#'
        for x in [26,27]: m[y][x] = '#'
    for y in [14,15,16]:
        for x in [2,3]: m[y][x] = '#'
        for x in [5,6]: m[y][x] = '#'
        for x in [8,9,10]: m[y][x] = '#'
        for x in [15,16,17]: m[y][x] = '#'
        for x in [19,20]: m[y][x] = '#'
        for x in [22,23,24]: m[y][x] = '#'
        for x in [26,27]: m[y][x] = '#'
    # Tractor path: horizontal at row 3, vertical down col 14, horizontal at row 15
    # Row 3 (inside wall block, carve path): horizontal T=== from x=11 to x=18
    for x in range(11,19): m[3][x] = '='
    m[3][14] = 'T'  # tractor at x=14
    # Vertical path down from (14,4) to (14,14)
    for y in range(4,15):
        if m[y][14] == '#': m[y][14] = '|'
        elif m[y][14] == '.': m[y][14] = '|'
    m[3][14] = 'T'  # keep T
    m[9][14] = '+'  # intersection with horizontal corridor
    m[5][14] = '+'  # intersection
    m[13][14] = '+' # intersection
    # Horizontal segment at row 15: x=14 to x=22
    for x in range(14,23): m[15][x] = '='
    m[15][14] = '+'  # connect to vertical
    # Player and exit
    m[1][1] = 'R'
    m[18][28] = 'X'
    # Eggs
    eggs = [(3,1),(8,1),(16,1),(24,1),(1,5),(8,5),(20,5),(27,5),
            (1,9),(8,9),(20,9),(27,9),(1,13),(8,13),(20,13),(27,13),
            (4,17),(11,17),(20,17),(25,17)]
    for ex,ey in eggs:
        if m[ey][ex] == '.': m[ey][ex] = 'E'
    set_border(m)
    return m

def map_15():
    """Twin-Patrol: 2 dogs, more complex maze."""
    return to_list(
        "##############################\n"
        "#R..E..#.E.........E.#..E...E#\n"
        "#.####.#.###.####.###.#.####.#\n"
        "#.#....#.#..........#.#....#.#\n"
        "#.#.####.#.########.#.####.#.#\n"
        "#.E....#...#......#...#..E.#.#\n"
        "#.####.###.#.####.#.###.####.#\n"
        "#......#D..#.#..#.#..D#.....E#\n"
        "#.########.#.#..#.#.########.#\n"
        "#.E........#.#..#.#........E.#\n"
        "#.##.####.##.#..#.##.####.##.#\n"
        "#.#..#..#.#..#..#..#.#..#..#.#\n"
        "#.#..#..#.#..####..#.#..#..#.#\n"
        "#.E..#..#.#........#.#..#..E.#\n"
        "#.####..#.########.#..####.#.#\n"
        "#.#..E..#..........#..E..#.#.#\n"
        "#.#..####.###.####.###.###.#.#\n"
        "#.#......E#........#E.....#.#\n"
        "#.########.........########X.#\n"
        "##############################"
    )

def map_16():
    """Muddy-Maze: Mud sections slow player but block dogs."""
    return to_list(
        "##############################\n"
        "#R..E..#.....E.....#....E...E#\n"
        "#.####.#.###.##.###.#.####.#.#\n"
        "#.#..M.#.#........#.#.M..#.#.#\n"
        "#.#..M.#.#.######.#.#.M..#.#.#\n"
        "#.E..M.#.E.#....#.E.#.M.E#.#.#\n"
        "#.####M#.####.#.####.#M###.#.#\n"
        "#.#..MM..............MM..#..E.#\n"
        "#.#.####.####.####.####.#.##.#\n"
        "#.#.E..#.#........#.#.E.#.#..#\n"
        "#.####.#.#.######.#.#.####.#.#\n"
        "#......#.#..D...#.#.#.....#..#\n"
        "#.####.#.######.#.#.####.####.#\n"
        "#.E..#.#........#.#.#..E.#...#\n"
        "#.##.#.####.##.####.#.##.#.#.#\n"
        "#.#..#.....E##E.....#..#.#.#.#\n"
        "#.#..######.##.######..#.#.#.#\n"
        "#.#........MMMM........#.#.#.#\n"
        "#.E........MMMM.......E#...X.#\n"
        "##############################"
    )

def map_17():
    """Dog-and-Machine: 2 dogs + 1 tractor."""
    return to_list(
        "##############################\n"
        "#R.E..#........E.......#..E.E#\n"
        "#.###.#.####.####.####.#.###.#\n"
        "#.#...#.#.===T====.#..#..#...#\n"
        "#.#.###.#.|.####.|.#.###.#.#.#\n"
        "#.E.....#.|.#..#.|.#.....E.#.#\n"
        "#.#####.#.|.#..#.|.#.#####.#.#\n"
        "#.....#.#.|.#D.#.|.#.#.....#.#\n"
        "#.###.#.#.|.####.|.#.#.###.#.#\n"
        "#.#.E.#.#.+======+.#.#.E.#.#.#\n"
        "#.#.###.#..........#.###.#.#.#\n"
        "#.#.....#.########.#.....#.E.#\n"
        "#.#####.#....##....#.#####.#.#\n"
        "#.E...#.####.##.####.#...E.#.#\n"
        "#.###.#......##......#.###.#.#\n"
        "#.#...#.####.##.####.#...#.#.#\n"
        "#.#.###.#..........#.###.#.#.#\n"
        "#.#.....#..E..D.E..#.....#.#.#\n"
        "#.#####.#..........#.#####.#X#\n"
        "##############################"
    )

def map_18():
    """Golden-Passages: Golden eggs in risky dead-ends."""
    return to_list(
        "##############################\n"
        "#R..E..#...........#.E.....#G#\n"
        "#.####.#.#########.#.####..#.#\n"
        "#.#..#.#.#.......#.#.#..#..#.#\n"
        "#.#..#.#.#.#####.#.#.#..#..#.#\n"
        "#.E..#.#.#.#.G.#.#.#.#..E..#.#\n"
        "#.####.#.#.#...#.#.#.####..#.#\n"
        "#......#.#.#####.#.#......D#.#\n"
        "#.####.#.#.......#.#.######.##\n"
        "#.#..E.#...........#..E..#...#\n"
        "#.#.####.####.####.####.####.#\n"
        "#.#........=T=====#........#.#\n"
        "#.#.####.#.|.####.|.####.#.#.#\n"
        "#.E.#..#.#.|.#G.#.|.#..#.E.#.#\n"
        "#.#.#..#.#.|.####.|.#..#.#.#.#\n"
        "#.#.#..#.#.+======+.#..#.#.#.#\n"
        "#.#.####.#..........#.####.#.#\n"
        "#.#......#..E....E..#......#.#\n"
        "#.########..........########X#\n"
        "##############################"
    )

def map_19():
    """Chicken-Maze: 2 chickens + 1 dog blocking corridors."""
    return to_list(
        "##############################\n"
        "#R..E..#.....E.....#....E...E#\n"
        "#.####.#.###.##.###.#.####.#.#\n"
        "#.#....#.#........#.#....#.#.#\n"
        "#.#.####.#.######.#.####.#.#.#\n"
        "#.E....#.#.#....#.#.#..E.#.#.#\n"
        "#.####.#.#.#.##.#.#.#.####.#.#\n"
        "#......#.#.#.C#.#.#.#.....E#.#\n"
        "#.####.#.#.####.#.#.#.####.#.#\n"
        "#.#..E.#.#......#.#.#.E..#.#.#\n"
        "#.#.####.########.####.#.#.#.#\n"
        "#.#..............D......#.#.#.#\n"
        "#.####.########.########.#.#.#\n"
        "#.E..#.#.......C......#..E.#.#\n"
        "#.##.#.#.####.####.##.#.##.#.#\n"
        "#.#..#.#.#........#.#.#..#.#.#\n"
        "#.#..#.#.#.######.#.#.#..#.#.#\n"
        "#.#..#.E.#........#.E.#..#.#.#\n"
        "#.#..#...#........#...#..#..X#\n"
        "##############################"
    )

def map_20():
    """Crossing-Paths: Complex tractor path + 2 dogs."""
    return to_list(
        "##############################\n"
        "#R..E.#..........E...#..E...E#\n"
        "#.###.#.####.####.##.#.####.##\n"
        "#.#.=+========T====+=#..#...##\n"
        "#.#.|.####.####.###.|.#.#.#.##\n"
        "#.E.|.#.E...........|.#.E.#.##\n"
        "#.#.|.#.####.####.#.|.####.#.#\n"
        "#.#.|.#.#..D...#..#.|.....#.#\n"
        "#.#.|.#.#.####.#..#.|.###.#.#\n"
        "#.#.+====#......#==+=#.E..#.#\n"
        "#.#.####.#.####.#.####.#.##.#\n"
        "#.#.E..#.#......#.#..E.#..#.#\n"
        "#.####.#.########.#.####..#.#\n"
        "#.E....#...........#...E..#.#\n"
        "#.####.###.######.###.###.#.#\n"
        "#.#..#.....#.D..#.....#.#.#.#\n"
        "#.#..####..#.##.#..####.#.#.#\n"
        "#.#......E.#....#.E.....#.#.#\n"
        "#.########.#....#.########.X#\n"
        "##############################"
    )

def map_21():
    """Dog-Pack: 3 dogs, many dead ends."""
    return to_list(
        "##############################\n"
        "#R.E.#.....E...E.....#.E...E##\n"
        "#.##.#.###.####.###.##.###.###\n"
        "#.#..#.#.E...##...E.#..#.....#\n"
        "#.#.##.####.####.####.##.###.#\n"
        "#.E..#.....#....#.....#..E.#.#\n"
        "#.####.###.#.##.#.###.####.#.#\n"
        "#......#D..#.##.#..D#......#.#\n"
        "#.####.#.###.##.###.#.####.#.#\n"
        "#.#..E.#...........#.#..E..#.#\n"
        "#.#.####.####.####.####.####.#\n"
        "#.#......#..........#......#.#\n"
        "#.########.########.########.#\n"
        "#.E........#..D...#........E.#\n"
        "#.####.###.#.####.#.###.####.#\n"
        "#.#..#.#.E.#....#.E.#.#..#.#.#\n"
        "#.#..#.#.###.##.###.#.#..#.#.#\n"
        "#.#..#.#.............#.#..#.#.#\n"
        "#.E..#.#.....E.......#.#.E..X#\n"
        "##############################"
    )

def map_22():
    """The-Gauntlet: Long narrow corridors, tractor + 2 dogs, mud."""
    return to_list(
        "##############################\n"
        "#R.E.......E...........E....E#\n"
        "#.##########.########.######.#\n"
        "#.#..........#......#........#\n"
        "#.#.########.#.####.########.#\n"
        "#.E.#.=T=====#.#E.#.........E#\n"
        "#.#.#.|.######.####.########.#\n"
        "#.#.#.|......D.............#.#\n"
        "#.#.#.|.######.####.######.#.#\n"
        "#.#.#.+=======#.E..#......#.#\n"
        "#.#.#.########.####.####.##.#\n"
        "#.E.#..........#........#..E.#\n"
        "#.#.##########.#.######.####.#\n"
        "#.#.MMMMM..E..#.#....#......#\n"
        "#.#.#########..#.#.##.######.#\n"
        "#.E.#..........#.#.#........E#\n"
        "#.#.#.##########.#.########.##\n"
        "#.#.#.......E..D.#.........E##\n"
        "#.#.#..........#.#..........X#\n"
        "##############################"
    )

def map_23():
    """Escape-Routes: All enemy types, fence/hole escape shortcuts."""
    return to_list(
        "##############################\n"
        "#R.E..#..E.........E..#..E..E#\n"
        "#.###.#.####.####.####.#.###.#\n"
        "#.#...#.#..........#..#...#..#\n"
        "#.#.###.#.########.#.###.####\n"
        "#.E...#.#.#..D...#.#.#..E...#\n"
        "#.###F#.#.#.####.#.#.#F###..#\n"
        "#...#..H#.#.C...#.#H..#...E.#\n"
        "#.#.####.#.######.#.####.#..#\n"
        "#.#.E..#.#........#.#..E.#..#\n"
        "#.####.#.####.####.#.####.#.#\n"
        "#......#..=T=======#.....#..#\n"
        "#.####.#..|.######.#.####.#.#\n"
        "#.E..#.#..|.#.E..#.#.#..E.#.#\n"
        "#.##.#.#..|.####.#.#.#.##.#.#\n"
        "#.#..#.#..+=======#.#..#..#.#\n"
        "#.#..#.#..........#.#..#.C#.#\n"
        "#.#..#.#E..D......#E#..#..#.#\n"
        "#.#..#.#..........#.#..#..#X#\n"
        "##############################"
    )

def map_24():
    """Dark-Labyrinth: Very complex maze, 3 dogs + tractor."""
    # Build programmatically for precise tractor path alignment
    m = empty_map()
    # Main horizontal corridors
    for x in range(1,29): m[1][x] = '.'
    for x in range(1,29): m[5][x] = '.'
    for x in range(1,29): m[9][x] = '.'
    for x in range(1,29): m[13][x] = '.'
    for x in range(1,29): m[18][x] = '.'
    # Vertical corridors
    for y in range(1,19): m[y][1] = '.'
    for y in range(1,19): m[y][5] = '.'
    for y in range(1,19): m[y][9] = '.'
    for y in range(1,19): m[y][14] = '.'
    for y in range(1,19): m[y][19] = '.'
    for y in range(1,19): m[y][23] = '.'
    for y in range(1,19): m[y][28] = '.'
    # Extra corridors for complexity
    for x in range(1,29): m[17][x] = '.'
    for y in range(1,19): m[y][12] = '.'
    for y in range(1,19): m[y][16] = '.'
    # Add wall blocks (2x2 or 2x3)
    wall_blocks = [
        (2,2,3,4), (6,2,8,4), (10,2,11,4), (15,2,16,4), (20,2,22,4), (24,2,27,4),
        (2,6,4,8), (6,6,8,8), (10,6,11,8), (15,6,16,8), (20,6,22,8), (24,6,27,8),
        (2,10,4,12), (6,10,8,12), (10,10,11,12), (15,10,16,12), (20,10,22,12), (24,10,27,12),
        (2,14,4,16), (6,14,8,16), (10,14,11,16), (17,14,18,16), (20,14,22,16), (24,14,27,16),
    ]
    for x1,y1,x2,y2 in wall_blocks:
        for y in range(y1,y2+1):
            for x in range(x1,x2+1):
                if 0 < x < 29 and 0 < y < 19:
                    m[y][x] = '#'
    # Tractor path: Z-shape at column 14 and 19
    # Horizontal top: x=9 to x=19 at row 7
    for x in range(9,20): m[7][x] = '='
    m[7][14] = 'T'
    # Vertical: x=19, row 7 down to row 11
    for y in range(7,12): m[y][19] = '|'
    m[7][19] = '+'  # junction
    # Horizontal bottom: x=14 to x=19 at row 11
    for x in range(14,20): m[11][x] = '='
    m[11][19] = '+'  # junction
    m[11][14] = '+'  # junction
    # Vertical: x=14, row 11 down to row 15
    for y in range(11,16): m[y][14] = '|'
    m[11][14] = '+'  # already set
    m[13][14] = '+'  # intersection with corridor
    # Player, exit, dogs
    m[1][1] = 'R'
    m[18][28] = 'X'
    m[5][8] = 'D'
    m[9][5] = 'D'
    m[13][23] = 'D'
    # Eggs (normal + golden + special)
    egg_pos = [(4,1),(12,1),(20,1),(27,1),(1,5),(14,5),(23,5),
               (1,9),(12,9),(23,9),(28,9),(1,13),(9,13),(19,13),(28,13),
               (5,17),(12,17),(19,17),(25,17)]
    for ex,ey in egg_pos:
        if m[ey][ex] in '.':
            m[ey][ex] = 'E'
    m[1][28] = 'G'  # golden egg top-right
    m[17][28] = 'G'  # golden egg bottom-right
    m[5][1] = 'S'   # special egg
    set_border(m)
    return m

def map_25():
    """Ultimate-Maze: Maximum difficulty, all mechanics."""
    return to_list(
        "##############################\n"
        "#R.E.#.....E.......E...#.E.G##\n"
        "#.##.#.###.####.###.##.#.###.#\n"
        "#.#..#.#.D.........#.#.#...#.#\n"
        "#.#.##.####.####.###.#.###.#.#\n"
        "#.E.F#...E.#....#.E..F#..E.#.#\n"
        "#.####.###.#.##.#.###.####.#.#\n"
        "#....#.#C..#.##.#..C#.#....#.#\n"
        "#.##.#.#.###.##.###.#.#.##.#.#\n"
        "#.#.E#.#.=T=====+=#.#.#E..#.#\n"
        "#.####.#.|.######.|.#.####.#.#\n"
        "#.S....#.|..D.....+=#.....E#.#\n"
        "#.####.#.|.######.|.#.####.#.#\n"
        "#.E..#.#.+========+.#.#..E.#.#\n"
        "#.##.#.#..M........M.#.#.##.#\n"
        "#.#..#.#..M.####.#.M.#..#.D.#\n"
        "#.#..#.##.M.#..#.#.M.##.#.#.#\n"
        "#.#..#..#.M.#..#.#.M.#..#.#.#\n"
        "#.G..#..#...#..#.#...#..#.E.X#\n"
        "##############################"
    )


# ============================================================
# MAIN
# ============================================================

def main():
    random.seed(42)  # reproducible

    maps = [
        ("11-Maze-Intro.txt", map_11),
        ("12-First-Chase.txt", map_12),
        ("13-Shortcut-Maze.txt", map_13),
        ("14-Tractor-Corridor.txt", map_14),
        ("15-Twin-Patrol.txt", map_15),
        ("16-Muddy-Maze.txt", map_16),
        ("17-Dog-and-Machine.txt", map_17),
        ("18-Golden-Passages.txt", map_18),
        ("19-Chicken-Maze.txt", map_19),
        ("20-Crossing-Paths.txt", map_20),
        ("21-Dog-Pack.txt", map_21),
        ("22-The-Gauntlet.txt", map_22),
        ("23-Escape-Routes.txt", map_23),
        ("24-Dark-Labyrinth.txt", map_24),
        ("25-Ultimate-Maze.txt", map_25),
    ]

    os.makedirs(os.path.join("assets", "maps"), exist_ok=True)

    print("Generating 15 Pacman-style maze maps...\n")
    for filename, gen_func in maps:
        m = gen_func()
        save_map(m, filename)

    print(f"\nDone! Generated {len(maps)} maps.")

if __name__ == "__main__":
    main()
