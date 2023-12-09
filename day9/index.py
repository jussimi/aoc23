
def is_zeroes(row):
  for item in row:
    if item != 0: return False
  return True

def extrapolate(line):
  history = [[int(x) for x in line.split()]]

  latest = history[0]
  while not is_zeroes(latest):
    latest = [latest[i] - latest[i-1] for i in range(1, len(latest))]
    history.append(latest)

  history[-1].extend([0, 0])
  for i in range(len(history) - 2, -1, -1):
    history[i].append(history[i][-1] + history[i+1][-1])
    history[i].insert(0, history[i][0] - history[i+1][0])

  return (history[0][0], history[0][-1])

def run(file):
  return [sum(x) for x in zip(*[extrapolate(l) for l in open(file).read().split("\n")])]

print(run("./day9/test.txt"))
print(run("./day9/data.txt"))
