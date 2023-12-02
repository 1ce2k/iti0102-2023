"""EX 13."""

class Spaceship:
    def __init__(self):
        self.crewmate_list = []
        self.impostor_list = []
        self.dead_players = []

    def add_crewmate(self, crewmate):
        if isinstance(crewmate, Crewmate) and crewmate not in self.crewmate_list and crewmate not in self.impostor_list:
            self.crewmate_list.append(crewmate)

    def add_impostor(self, impostor):
        if isinstance(impostor, Impostor) and impostor not in self.impostor_list and impostor not in self.crewmate_list:
            self.impostor_list.append(impostor)

    def kill_crewmate(self, killer, target_name):
        target = next((crewmate for crewmate in self.crewmate_list if crewmate.name == target_name.upper()), None)
        if target:
            if isinstance(killer, Impostor) and target not in self.dead_players:
                target.id_dead = True
                self.dead_players.append(target)
                killer.kills += 1

    def protect_crewmate(self, guardian_angel, target):
        if guardian_angel in self.dead_players and isinstance(target, Crewmate):
            target.protected = True

    def revive_crewmate(self, reviver, target):
        if reviver in self.crewmate_list and isinstance(target, Crewmate) and target in self.dead_players:
            target.is_dead = False
            self.dead_players.remove(target)

    def get_crewmate_list(self):
        return self.crewmate_list

    def get_impostor_list(self):
        return self.impostor_list

    def get_dead_players(self):
        return self.dead_players

    def sort_crewmates_by_tasks(self):
        return sorted(self.crewmate_list, key=lambda x: x.tasks_left)

    def get_regular_crewmates(self):
        return [x for x in self.crewmate_list if x.role == "Crewmate"]

    def get_impostor_with_most_kills(self):
        return sorted(self.impostor_list, key=lambda x: -x.kills)[0]

    def get_crewmate_with_most_tasks_done(self):
        return sorted(self.crewmate_list, key=lambda x: x.tasks_left)[0]

    def sort_impostors_by_kills(self):
        return sorted(self.impostor_list, key=lambda x: -x.kills)


class Crewmate:
    def __init__(self, name, role, tasks=10):
        self.name = name.capitalize()
        self.role = role.title() if role.title() != 'Impostor' else 'Crewmate'
        self.tasks_left = tasks
        self.is_dead = False
        self.protected = False

    def complete_task(self):
        if not self.is_dead and self.tasks_left > 0:
            self.tasks_left -= 1

    def __str__(self):
        return f"{self.name}, role: {self.role}, tasks left: {self.tasks_left}."


class Impostor:
    def __init__(self, name):
        self.name = name.capitalize()
        self.kills = 0

    def __str__(self):
        return f"Impostor {self.name}, kills: {self.kills}."


if __name__ == "__main__":
    print("Spaceship.")

    spaceship = Spaceship()
    print("Check for dead players")
    print(spaceship.get_dead_players())  # -> []
    print()

    print("Let's add some crewmates.")
    red = Crewmate("Red", "Crewmate")
    white = Crewmate("White", "Impostor")
    yellow = Crewmate("Yellow", "Guardian Angel", tasks=5)
    green = Crewmate("green", "Altruist")
    blue = Crewmate("BLUE", "Sheriff", tasks=0)

    print(red)  # -> Red, role: Crewmate, tasks left: 10.
    print(white)  # -> White, role: Crewmate, tasks left: 10.
    print(yellow)  # -> Yellow, role: Guardian Angel, tasks left: 5.
    print(blue)  # -> Blue, role: Sheriff, tasks left: 0.
    print()

    print("Let's make Yellow complete a task.")
    yellow.complete_task()
    yellow.complete_task()
    yellow.complete_task()
    yellow.complete_task()
    yellow.complete_task()
    yellow.complete_task()
    yellow.complete_task()
    yellow.complete_task()
    yellow.complete_task()
    print(yellow)  # ->  Yellow, role: Guardian Angel, tasks left: 4.
    print()

    print("Adding crewmates to Spaceship:")
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(white)
    spaceship.add_crewmate(yellow)
    spaceship.add_crewmate(green)
    print([x.color for x in spaceship.get_crewmate_list()])  # -> Red, White, Yellow and Green

    spaceship.add_impostor(blue)  # Blue cannot be an Impostor.
    print([x.color for x in spaceship.get_impostor_list()])  # -> []
    spaceship.add_crewmate(blue)
    print([x.color for x in spaceship.get_crewmate_list()])  # -> []

    print()
    print("Now let's add impostors.")
    orange = Impostor("orANge")
    black = Impostor("black")
    purple = Impostor("Purple")
    spaceship.add_impostor(orange)
    spaceship.add_impostor(black)

    spaceship.add_impostor(Impostor("Blue"))  # Blue player already exists in Spaceship.
    spaceship.add_impostor(purple)
    spaceship.add_impostor(Impostor("Pink"))  # No more than three impostors can be on Spaceship.
    print(spaceship.get_impostor_list())  # -> Orange, Black and Purple
    print()

    print("The game has begun! Orange goes for the kill.")
    spaceship.kill_crewmate(orange, "yellow")
    print(orange)  # -> Impostor Orange, kills: 1.
    spaceship.kill_crewmate(black, "purple")  # You can't kill another Impostor, silly!
    print(spaceship.get_impostor_list())
    print(spaceship.get_dead_players())  # -> Yellow
    print()

    print("Yellow is a Guardian angel, and can protect their allies when dead.")
    spaceship.protect_crewmate(yellow, green)
    print(green.protected)  # -> True
    spaceship.kill_crewmate(orange, "green")
    print(green in spaceship.dead_players)  # -> False
    print(green.protected)  # -> False
    print()

    print("Green revives their ally.")
    spaceship.kill_crewmate(purple, "RED")
    spaceship.revive_crewmate(green, red)
    print(red in spaceship.dead_players)  # -> False
    print()

    print("Let's check if the sorting and filtering works correctly.")

    red.complete_task()
    print(spaceship.get_role_of_player("white"))  # -> Sheriff
    spaceship.kill_crewmate(purple, "blue")
    print(spaceship.sort_crewmates_by_tasks())  # -> Red, White
    print(spaceship.sort_impostors_by_kills())  # -> Purple, Orange, Black
    print(spaceship.get_regular_crewmates())  # -> White, Red

