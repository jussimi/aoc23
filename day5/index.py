import sys

def get_overlap(range1, range2):
  if range1[0] > range2[1] or range2[0] > range1[1]: return None
  return (max(range1[0], range2[0]), min(range1[1], range2[1]))

def merge_ranges(ranges):
  sorted_ranges = sorted(ranges)
  results = [ranges[0]]
  for i in range(1, len(ranges)):
    lastI = len(results) - 1
    overlap = get_overlap(sorted_ranges[i], results[lastI])
    if overlap != None:
      results[lastI] = (min(sorted_ranges[i][0], results[lastI][0]), max(sorted_ranges[i][1], results[lastI][1]))
    else:
      results.append(sorted_ranges[i])
  return results

def augment_ranges(ranges):
  augmented = []
  curr_end = 0
  for i in range(len(ranges)):
    next = ranges[i]
    if curr_end < next[0]:
      augmented.append((curr_end, curr_end, next[0] - curr_end - 1))
    augmented.append(next)
    curr_end = next[0] + next[2]
  augmented.append((curr_end, curr_end, sys.maxsize))
  return augmented


class Mapping:
  def __init__(self, input):
    lines = input.strip().split("\n")
    self.ranges = sorted([tuple((int(x) for x in line.split())) for line in lines])

    self.ranges = augment_ranges(self.ranges)
  
  def compute(self, value):
    for dest, source, count in self.ranges:
      if source <= value < source + count:
        return dest + value - source
    raise Exception("Should not be here!")
  
  def compute_ranges(self, target):
    ranges = []
    for dest_min, source, count in self.ranges:
      dest_max = dest_min + count
      overlap = get_overlap([dest_min, dest_max], target)
      if overlap != None:
        source_min = source + overlap[0] - dest_min
        source_max = source + count - (dest_max - overlap[1])
        ranges.append((source_min, source_max))
    return ranges
    
  def get_acceptable_ranges(self, targets):
    ranges = []
    for t in targets:
      ranges += self.compute_ranges(t)
    return sorted(ranges)
  
class MappingList:
  def __init__(self, input):
    self.mappings = [Mapping(x) for x in input]

  def compute(self, value):
    pointer = value
    for map in self.mappings:
      pointer = map.compute(pointer)
    return pointer
  
  def get_min_ranges(self, targets = [], index = 0):
    count = len(self.mappings)
    if index == count:
      return targets
    current_map = self.mappings[count - index - 1]
    ranges = []
    if index == 0:
      ranges = [(start, start+count) for start, _, count in current_map.ranges]
    else:
      ranges = current_map.get_acceptable_ranges(targets)
    return self.get_min_ranges(ranges, index + 1)

def run(file):
  seeds, *maps = [x.split(":")[1] for x in open(file).read().split("\n\n")]
  seeds = [int(seed) for seed in seeds.strip().split()]
  mappingList = MappingList(maps)

  locations = [mappingList.compute(seed) for seed in seeds]

  ranges = mappingList.get_min_ranges()

  seeds2 = [tuple(seeds[i * 2:(i + 1) * 2]) for i in range((len(seeds) + 2 - 1) // 2 )]
  minimum = float("inf")
  for seed in seeds2:
    for r in ranges:
      overlap = get_overlap(r, (seed[0], seed[0]+seed[1]))
      if overlap != None:
        val = mappingList.compute(overlap[0])
        if val < minimum:
          minimum = val


  return min(locations), minimum


print("Test", run("./day5/test.txt"))
print("Data", run("./day5/data.txt"))
