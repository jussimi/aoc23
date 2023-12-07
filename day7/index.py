values = {
  "A": 14,
  "K": 13,
  "Q": 12,
  "J": 11,
  "T": 10,
}

values2 = {
  "A": 13,
  "K": 12,
  "Q": 11,
  "T": 10,
  "J": 1,
}

scores = {
  "00001": 7,
  "10010": 6,
  "01100": 5,
  "20100": 4,
  "12000": 3,
  "31000": 2,
  "50000": 1
}

scores_with_jokers = {
  "00001": [7, -1, -1, -1, -1,  7],
  "10010": [6,  7, -1, -1,  7, -1],
  "01100": [5, -1,  7,  7, -1, -1],
  "20100": [4,  6, -1,  6, -1, -1],
  "12000": [3,  5,  6, -1, -1, -1],
  "31000": [2,  4,  4, -1, -1, -1],
  "50000": [1,  2, -1, -1, -1, -1]
}

def parse_hand(line, vals):
  hand, bid = line.split()
  bid = int(bid)

  card_counts = { k: 0 for k in range(1, 15) }
  parsed = []
  for c in hand:
    n = int(c) if c.isdigit() else vals.get(c)
    parsed.append(n)
    card_counts[n] += 1

  stack_counts = [0]*5
  for count in card_counts.values():
    if count > 0:
      stack_counts[count-1] += 1

  key = "".join(map(str, stack_counts))

  return {
    "key": key,
    "counts": card_counts,
    "hand": parsed,
    "bid": bid,
  }

def parse_line(line):
  data = parse_hand(line, values)
  
  # First item is score, following 5 are the cards.
  data["hand"].insert(0, scores[data["key"]])

  return { "score": tuple(data["hand"]), "bid": data["bid"] }

def parse_line_jokers(line):
  data = parse_hand(line, values2)
  
  score = scores_with_jokers[data["key"]][data["counts"][1]]

  # First item is score, following 5 are the cards.
  data["hand"].insert(0, score)

  return { "score": tuple(data["hand"]), "bid": data["bid"] }

def get_score(hands):
  sorted_hands = sorted(hands, key=lambda x: x["score"])
  winnings = sum([ (i+1) * x["bid"] for i,x in enumerate(sorted_hands) ])
  return winnings

def run(file):
  lines = open(file).read().split("\n")

  return get_score([parse_line(l) for l in lines]), get_score([parse_line_jokers(l) for l in lines])

print(run("./day7/test.txt"))
print(run("./day7/data.txt"))


