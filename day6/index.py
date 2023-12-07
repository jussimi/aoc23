import math

def calc_roots(time, distance):
  discriminant = time**2 - 4 * distance
  if discriminant < 0: return None
  if discriminant == 0: return [time / 2, time / 2]
  sqrt = math.sqrt(discriminant)
  return sorted([(time + sqrt)/2, (time  - sqrt)/2])


def interval(time, distance):
  epsilon = 0.0001
  a, b = calc_roots(time, distance)
  return 1 + math.floor(b - epsilon) - math.ceil(a + epsilon)



def calc_ways(file):
  times, distances = [list(map(int, x.split(":")[1].strip().split())) for x in open(file).read().split("\n")]
  print(times, distances)

  prod = 0
  for i in range(len(times)):
    ways = interval(times[i], distances[i])
    if prod == 0 and ways > 0: prod = 1
    prod *= ways


  t2, d2 = [int("".join([str(s) for s in x])) for x in [times, distances]]

  return prod, interval(t2, d2)

print(calc_ways("./day6/test.txt"))
print(calc_ways("./day6/data.txt"))

