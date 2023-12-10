import math

chars = {
  "|": "┃",
  "-": "━",
  "L": "┗",
  "J": "┛",
  "7": "┓",
  "F": "┏",
  "S": "S",
}

UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)

possible_neighbors = {
  "┃": [UP, DOWN],
  "━": [LEFT, RIGHT],
  "┗":[UP, RIGHT],
  "┛": [UP, LEFT],
  "┓": [DOWN, LEFT],
  "┏": [DOWN, RIGHT],
  "S": [UP, RIGHT, DOWN, LEFT],
}

padding = {
  "┃": [".┃.", ".┃.", ".┃."],
  "━": ["...", "━━━", "..."],
  "┗": [".┃.", ".┗━", "..."],
  "┛": [".┃.", "━┛.", "..."],
  "┓": ["...", "━┓.", ".┃."],
  "┏": ["...", ".┏━", ".┃."],
  ".": ["...", ".x.", "..."],
  "S": [".┃.", "━S━", ".┃."],
}

class Grid:
  def __init__(self, file):
    content = "".join([chars.get(x, x) for x in file])
    lines = content.split("\n")

    self.content = content
    self.nodes = {}
    self.edges = {}
    self.main_loop = {}
    self.start = None

    edge_candidates = {}
    for i, line in enumerate(lines):
      for j, char in enumerate(line):
        id = self.id(i, j)
        self.nodes[id] = char
        if char == "S": self.start = id

        for di, dj in possible_neighbors.get(char, []):
          neigh = self.id(i + di, j + dj)
          edge_candidates[self.id(id, neigh, "%")] = True

    # Accept only bidirectional edges.
    for edge in edge_candidates.keys():
      start, end = edge.split("%")
      reverse = self.id(end, start, "%")
      self.edges.setdefault(start, {})
      if reverse in edge_candidates:
        self.edges[start][end] = True
    
  def id(self, i, j, sep = "#"):
    return f"{i}{sep}{j}"
  
  def pretty_print(self, include):
    content = ""
    for i, line in enumerate(self.content.split("\n")):
      row = ""
      for j, char in enumerate(line):
        row += char if self.id(i,j) in include else "."
      content += f"{row}\n"
    print(content)

  def pad(self, include):
    all_rows = []
    for i, line in enumerate(self.content.split("\n")):
      rows = [""] * 3
      for j, char in enumerate(line):
        padded = padding[char] if self.id(i,j) in include else padding["."]
        for k, r in enumerate(padded):
          rows[k] += r
      all_rows += rows
    content = "\n".join(all_rows)
    return content
      
  def bfs(self, start, generate_neighbors):
    visited = {}
    visited[start] = self.nodes[start]

    queue = [start]

    while len(queue) > 0:
      next = []
      for node in queue:
        neighbors = generate_neighbors(self, node)
        for neigh in neighbors:
          if not neigh in visited:
            visited[neigh] = self.nodes[neigh]
            next.append(neigh)
      queue = next
    
    return visited

def get_connected(grid, node):
  return grid.edges[node].keys()

def get_adjacent_tiles(grid, node):
  i, j = [int(x) for x in node.split("#")]
  adjacent = []
  for x in [UP, DOWN, RIGHT, LEFT]:
    neigh = grid.id(i + x[0], j + x[1])
    char = grid.nodes.get(neigh)
    if char == "." or char == "x":
      adjacent.append(neigh)

  return adjacent


def countX(dict):
  return sum([1 if x == "x" else 0 for x in dict.values()])

def run(file, write = False):
  grid = Grid(open(file).read())

  grid.main_loop = grid.bfs(grid.start, get_connected)
  grid.pretty_print(grid.main_loop)

  grid2 = Grid(grid.pad(grid.main_loop))
  outside = grid2.bfs(grid2.id(0,0), get_adjacent_tiles)
  inside = countX(grid2.nodes) - countX(outside)

  if write:
    f = open("./day10/res.txt", "w")
    f.write(grid2.content)
    f.close()

  return math.ceil(len(grid.main_loop) / 2), inside

print(run("./day10/test.txt"))
print(run("./day10/test2.txt"))
print(run("./day10/test3.txt"))
print(run("./day10/data.txt"))
