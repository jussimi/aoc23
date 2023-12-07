


directions = [[1,0], [0,1], [1,1], [1,-1]]

  
def gen_id(i,j):
  return f"{i}:{j}"

def get_coords(coord):
  split = coord.split(":")
  return [int(split[0]), int(split[1])]

class Number:
  def __init__(self,id, value, coords):
    if value < 0:
      print("NEGATIVE")
    self.id = id
    self.value = value
    self.coords = coords

    self.neighbors = {}
    for coord in self.coords.keys():
      i,j = get_coords(coord)
      for di, dj in directions:
        id_plus = gen_id(i+di, j+dj)
        id_min = gen_id(i-di, j-dj)

        for id in [id_plus, id_min]:

          if self.coords.get(id) == None:
            self.neighbors[id] = True

  def __repr__(self):
    return f"{{id: {self.id}, value: {self.value}, coords: {[k for k in self.coords]}}}, neighbors: {[k for k in self.neighbors.keys()]}"

class Grid:
  def __init__(self, file):
    lines = open(file).read().split("\n")

    self.points = []

    grid = {}
    for i, line in enumerate(lines):
      curr_number = ""
      for j, value in enumerate(line):
        if value.isdigit():
          curr_number += value
        elif curr_number != "":
          self.add_point(curr_number, i, j)
          curr_number = ""
        grid[gen_id(i,j)] = value
      if curr_number != "":
        self.add_point(curr_number, i, len(line)-1)

    self.lines = grid

  def calc_number_sum(self):
    sum = 0
    for point in self.points:
      if self.has_symbol_neighbor(point):
        sum += point.value
    return sum
  
  def has_symbol_neighbor(self, point):
    for id in point.neighbors.keys():
      val = self.lines.get(id)
      if val != None and not val.isdigit() and val != ".":
        return True
    
    # print(list(point.coords.keys())[0], point.value)
    return False

  def add_point(self, value, curr_i, curr_j):
    coords = {}
    for i in range(len(value), 0, -1):
      coords[gen_id(curr_i, curr_j-i)] = 1
    num = Number(len(self.points), int(value), coords)
    self.points.append(num)




#print(Grid("./day3/test.txt").calc_number_sum())
grid = Grid("./day3/data.txt")

points = {}
for p in grid.points:
  points[str(p.value)] = True

print(Grid("./day3/data.txt").calc_number_sum())
