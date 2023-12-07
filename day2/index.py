

class Line:
  def __init__(self, input):
    self.input = input

    id_part, results = input.split(": ")

    _,id = id_part.split(" ")

    self.id = int(id)
    
    sets = []
    for set in results.split("; "):
      colors = {
        "red": 0,
        "green": 0,
        "blue": 0,
      }
      for item in set.split(", "):
        count, color = item.split(" ")
        colors[color] += int(count)
      sets.append(colors)

    self.sets = sets

def gen_lines(file):
  lines = []
  for line in open(file).read().split("\n"):
    lines.append(Line(line))
  return lines


limits = {
  "red": 12,
  "green": 13,
  "blue": 14, 
}

def check_line(line):
  for set in line.sets:
    for color, value in limits.items():
      if set[color] > value:
        return 0
  return line.id    

def calc_id_sum(file):
  lines = gen_lines(file)

  sum = 0
  for line in lines:
    sum += check_line(line)

  return sum

def calc_power(line):
  min = line.sets[0]
  for set in line.sets:
    for color, value in min.items():
      if set[color] > value:
        min[color] = set[color]
  
  pow = 1
  for x in min.values():
    pow *= x
  return pow

def calc_power_sum(file):
  lines = gen_lines(file)
  sum = 0
  for line in lines:
    sum += calc_power(line)
  return sum


print("Test 1", calc_id_sum("./day2/test.txt"))
print("Data 1", calc_id_sum("./day2/data.txt"))

print("Test 2", calc_power_sum("./day2/test.txt"))
print("Data 2", calc_power_sum("./day2/data.txt"))