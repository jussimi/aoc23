
import re

numbers = {
  "one": "1",
  "two": "2",
  "three": "3",
  "four": "4",
  "five": "5",
  "six": "6",
  "seven": "7",
  "eight": "8",
  "nine": "9",
}

def handle_match(m):
  for group in m.groups():
    if group != None:
      return numbers[group]

def replace_and_calc(file, repl_words = False):
  content = open(file).read()
  print(len(content.split("\n")))

  if repl_words:
    num_re = re.compile(f"(?={'|'.join(map(lambda x: f'({x})', numbers.keys()))})")
    content = num_re.sub(handle_match, content)
  content = "".join(re.findall("\d|\n",content))

  sum = 0
  print(len(content.split("\n")))
  for line in content.split("\n"):
    sum += int(line[0]+line[len(line)-1])

  return sum

# Step 1
# print("Test", replace_and_calc("./day1/test.txt"))
# print("Data", replace_and_calc("./day1/data.txt"))

# # Step 2
print("Test", replace_and_calc("./day1/test2.txt", True))
print("Data", replace_and_calc("./day1/data.txt", True))
