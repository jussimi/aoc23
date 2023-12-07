
def line_score(line):
  _, numbers = line.split(": ")
  wins, guesses = numbers.split(" | ")

  win_map = {k: True for k in wins.split()}

  return sum([1 if guess in win_map else 0 for guess in guesses.split()])


def calc_points(file):
  scores = [line_score(line) for line in open(file).read().split("\n")]
  cards = [1] * len(scores)

  points = sum([0 if x == 0 else 2**(x-1) for x in scores])

  for i, count in enumerate(cards):
    for _ in range(count):
      for j in range(scores[i]):
        next = i + j + 1
        if next < len(scores):
          cards[next] += 1

  return points, sum(cards)


print(calc_points("./day4/test.txt"))
print(calc_points("./day4/data.txt"))
