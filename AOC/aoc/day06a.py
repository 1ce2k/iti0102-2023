"""AOC DAY 6 part A."""


with open('example.txt', 'r') as file:
    data = file.readlines()

times = data[0][6:].split()
distances = data[1][9:].split()
games = []
for x, y in zip(times, distances):
    games.append((int(x), int(y)))
total = 0
for i in range(len(games)):
    # GAME 1
    game = games[i]
    count = 0
    for x in range(1, game[0]):
        speed = x * 1
        time_left = game[0] - x
        if speed * time_left > game[1]:
            count += 1
    print(f"Game {i} result is {count}")

    if total == 0:
        total = count
    else:
        total *= count

print(f"Total number: {total}")
