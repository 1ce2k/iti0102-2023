"""AOC DAY 6 part A."""


with open('example.txt', 'r') as file:
    data = file.readlines()

times = data[0][6:].split()
distances = data[1][9:].split()
game = int(''.join(times)), int(''.join(distances))
count = 0
for x in range(1, game[0]):
    speed = x * 1
    time_left = game[0] - x
    if speed * time_left > game[1]:
        count += 1
print(f"Game result is {count}")
