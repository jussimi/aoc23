import math


def lcm(*args):
  res = args[0]
  for x in args:
    res = (res * x) // math.gcd(res, x)
  return res

class Grid:
  def __init__(self, file):
    instructions, content = open(file).read().split("\n\n")

    instructions = [0 if c == "L" else 1 for c in instructions]

    nodes = {}
    for line in content.replace("(", "").replace(")", "").split("\n"):
      name, neighbors = line.split(" = ")
      nodes[name] = tuple(neighbors.split(", "))

    self.instructions = instructions
    self.nodes = nodes   

  def get_distance(self, start, target):
    distance = 0
    curr = start

    visited = {}

    while curr != target or distance == 0:
      next_i = distance % len(self.instructions)
      
      key = f"{curr}-{next_i}"

      if key in visited:
        return 0

      visited[key] = True

      curr = self.nodes[curr][self.instructions[next_i]]
      distance += 1
    
    return distance
  
  def has_path(self, start, target, visited):
    if start == target:
      return True
    
    for next in [self.nodes[start][0], self.nodes[start][1]]:
      edge = f"{start}-{next}"
      if edge in visited:
        continue
      visited[edge] = True

      if self.has_path(next, target, visited):
        return True

    return False

  
  def compute_distances(self):
    starts = list(filter(lambda k: k[2] == "A", self.nodes.keys()))
    ends = list(filter(lambda k: k[2] == "Z", self.nodes.keys()))

    distances = []
    for start in starts:
      for end in ends:
        if self.has_path(start, end, {}):
          distances.append(self.get_distance(start, end))
          break
    
    return lcm(*distances)

def run1(file):
  grid = Grid(file)
  d = grid.get_distance("AAA", "ZZZ")
  return d

def run2(file):
  grid = Grid(file)
  return grid.compute_distances()



print(run1("./day8/test.txt"))
print(run1("./day8/data.txt"))

print(run2("./day8/test2.txt"))
print(run2("./day8/data.txt"))