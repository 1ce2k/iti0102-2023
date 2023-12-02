"""EX 13."""


class Spaceship:
    """Spaceship class."""

    def __init__(self):
        """Init spaceship."""
        self.crewmate_list = []
        self.impostor_list = []
        self.dead_players = []
        self.is_anyone_protected = False

    def add_crewmate(self, crewmate):
        """Add new crewmate."""
        if isinstance(crewmate, Crewmate) and crewmate.name not in [x.name for x in self.crewmate_list] and crewmate.name not in [x.name for x in self.impostor_list]:
            self.crewmate_list.append(crewmate)

    def add_impostor(self, impostor):
        """Add new impostor."""
        if isinstance(impostor, Impostor) and impostor.name not in [x.name for x in self.crewmate_list] and impostor.name not in [x.name for x in self.impostor_list] and len(self.impostor_list) < 3:
            self.impostor_list.append(impostor)

    def kill_crewmate(self, killer, target_name):
        """Kill crewmate."""
        target = next((crewmate for crewmate in self.crewmate_list if crewmate.name == target_name.capitalize()), None)
        if target and killer in self.impostor_list and target not in self.dead_players:
            if not target.protected:
                target.is_dead = True
                self.dead_players.append(target)
                killer.kills += 1
            else:
                target.protected = False
                self.is_anyone_protected = False

    def kill_impostor(self, killer, target_name):
        """Kill impostor."""
        target = next((impostor for impostor in self.impostor_list if impostor.name == target_name.capitalize()), None)
        if target and killer in self.crewmate_list and killer.role == 'Sheriff' and target.role == 'Impostor' and target not in self.dead_players:
            if not target.protected:
                self.dead_players.append(target)
            else:
                target.protected = False

    def protect_crewmate(self, guardian_angel, target):
        """Protect someone."""
        if guardian_angel in self.dead_players and guardian_angel.role == 'Guardian Angel' and not self.is_anyone_protected and target not in self.dead_players:
            target.protected = True
            self.is_anyone_protected = True

    def revive_crewmate(self, reviver, target):
        """Revive someone."""
        if reviver in self.crewmate_list and reviver.role == 'Altruist' and not reviver.is_dead and target in self.dead_players:
            target.is_dead = False
            self.dead_players.remove(target)

    def get_crewmate_list(self):
        """Return crewmate list."""
        return self.crewmate_list

    def get_impostor_list(self):
        """Return impostor list."""
        return self.impostor_list

    def get_dead_players(self):
        """Return dead players list."""
        return self.dead_players

    def sort_crewmates_by_tasks(self):
        """Sort crewmates by tasks."""
        return sorted(self.crewmate_list, key=lambda x: x.tasks_left)

    def get_regular_crewmates(self):
        """Return list of crewmates with role 'Crewmate'."""
        return [x for x in self.crewmate_list if x.role == "Crewmate"]

    def get_impostor_with_most_kills(self):
        """Return impostor with most kills."""
        return sorted(self.impostor_list, key=lambda x: -x.kills)[0]

    def get_crewmate_with_most_tasks_done(self):
        """Return crewmate with most tasks done."""
        return sorted(self.crewmate_list, key=lambda x: x.tasks_left)[0]

    def sort_impostors_by_kills(self):
        """Sort impostors by kills."""
        return sorted(self.impostor_list, key=lambda x: -x.kills)

    def get_role_of_player(self, name):
        """Return role of player."""
        for player in (self.impostor_list + self.crewmate_list):
            if player.name == name.capitalize():
                return player.role


class Crewmate:
    """Crewmate class."""

    def __init__(self, name, role, tasks=10):
        """Init crewmate."""
        self.name = name.capitalize()
        self.role = role.title() if role.title() != 'Impostor' else 'Crewmate'
        self.tasks_left = tasks
        self.is_dead = False
        self.protected = False

    def complete_task(self):
        """Complete task."""
        if not self.is_dead and self.tasks_left > 0:
            self.tasks_left -= 1

    def __repr__(self):
        """Return str."""
        return f"{self.name}, role: {self.role}, tasks left: {self.tasks_left}."


class Impostor:
    """Impostor class."""

    def __init__(self, name):
        """Init impostor."""
        self.name = name.capitalize()
        self.role = "Impostor"
        self.kills = 0
        self.protected = False

    def __repr__(self):
        """Return str."""
        return f"Impostor {self.name}, kills: {self.kills}."


if __name__ == "__main__":
    # print("Spaceship.")

    spaceship = Spaceship()
    # print("Check for dead players")
    # print(spaceship.get_dead_players())  # -> []
    # print()

    # print("Let's add some crewmates.")
    red = Crewmate("Red", "Crewmate")
    white = Crewmate("White", "Impostor")
    yellow = Crewmate("Yellow", "Guardian Angel", tasks=5)
    green = Crewmate("green", "Altruist")
    blue = Crewmate("BLUE", "Sheriff", tasks=0)

    print(red)  # -> Red, role: Crewmate, tasks left: 10.
    print(white)  # -> White, role: Crewmate, tasks left: 10.
    print(yellow)  # -> Yellow, role: Guardian Angel, tasks left: 5.
    print(blue)  # -> Blue, role: Sheriff, tasks left: 0.
    # print()

    # print("Let's make Yellow complete a task.")
    yellow.complete_task()
    # print(yellow)  # ->  Yellow, role: Guardian Angel, tasks left: 4.
    print()

    print("Adding crewmates to Spaceship:")
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(white)
    spaceship.add_crewmate(yellow)
    spaceship.add_crewmate(green)

    spaceship.add_impostor(blue)  # Blue cannot be an Impostor.
    spaceship.add_crewmate(blue)
    print(spaceship.get_crewmate_list())  # -> Red, White, Yellow and Green

    print("Now let's add impostors.")
    orange = Impostor("orANge")
    black = Impostor("black")
    purple = Impostor("Purple")
    spaceship.add_impostor(orange)
    # spaceship.add_impostor(black)

    # spaceship.add_impostor(Impostor("Blue"))  # Blue player already exists in Spaceship.
    spaceship.add_impostor(purple)
    # spaceship.add_impostor(Impostor("Pink"))  # No more than three impostors can be on Spaceship.
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
    spaceship.protect_crewmate(yellow, red)
    print(red.protected)
    spaceship.kill_crewmate(orange, "green")
    print(green in spaceship.dead_players)  # -> False
    print(green.protected)  # -> False
    print()

    print("Green revives their ally.")
    spaceship.kill_crewmate(purple, "Green")
    print(spaceship.get_dead_players())
    spaceship.revive_crewmate(green, green)
    print(spaceship.get_dead_players())
    print(red in spaceship.dead_players)  # -> False
    print()

    spaceship.kill_impostor(blue, 'black')
    print(spaceship.get_dead_players())
