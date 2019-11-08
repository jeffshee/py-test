import random

# float 0~1
r1 = random.random()
# float uniform a<= n <= b
r2 = random.uniform(100, 200)
# int start, end, step
r3 = random.randrange(1, 7)
# int start, end
# randint(start, end) == randrange(start, end+1)
r4 = random.randint(1, 6)
print(r1, r2, r3, r4)